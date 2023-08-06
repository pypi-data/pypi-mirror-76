import six
from six import string_types
from swimbundle_utils.exceptions import SwimlaneIntegrationException, InvalidInput
from swimbundle_utils.validation import Validators, StopValidation
from swimbundle_utils.flattener import StringTypes, Flattener
from validators import ValidationFailure
import pendulum
import re
import base64

from swimbundle_utils.flattener import FunctionType, InstanceType
if six.PY2:
    from types import MethodType
    FuncTypes = (FunctionType, InstanceType, MethodType)
else:
    FuncTypes = FunctionType


def asset_parser(context_asset, host_name="host",
                 username="username", password="password", auth=None, **kwargs):
    """Take in a context asset and break it into params for an ``__init__`` call on BasicRestEndpoint
    
    Args:
        context_asset: Context asset object
        host_name: host key name to grab from asset, defaults to ``host``
        username: username key name to grab from asset, defaults to ``username``
        password: password key name to grab from asset, defaults to ``password``
        auth: optional auth argument to override username/password. Set to None to disable auth
        kwargs: optional keyword args to overwrite the parameters with
    
    Returns:
        Dictionary of key args to use with \*\*{} in the ``super().__init__()`` of a BasicRestEndpoint

    """
    host = context_asset.get(host_name)
    if host is not None:
        host = host.strip(" /")
        if 'port' in context_asset:
            host = "{}:{}".format(host, context_asset['port'])

    params = {
        "host": host,
        "verify": context_asset.get("verify_ssl", True),
        "proxy": context_asset.get("http_proxy")
    }

    if auth == "basic":  # nondefault auth
        params["auth"] = (context_asset[username], context_asset[password])
    elif auth:  # No auth, but not none (else is inferred to be no auth)
        params["auth"] = auth

    params.update(kwargs)

    return params

def create_attachment(filename, raw_data):
    """Easy way to create a single attachment. To create multiple attachments under a single key, use SwimlaneAttachment()
    
    Args:
        filename: filname of the attachment
        raw_data: raw data of the file (pre-base64)
    
    Returns:
        JSON data suitable for a key output in Swimlane

    """
    swa = SwimlaneAttachments()
    swa.add_attachment(filename, raw_data)
    return swa.get_attachments()


class SwimlaneAttachments(object):
    """Swimlane Attachment Manager Class"""
    
    def __init__(self):
        self.attachments = []

    def add_attachment(self, filename, raw_data):
        """Add an attachment to 

        Args:
            filename: Name of the file
            raw_data: Raw, pre-base64 data to encode

        """
        if isinstance(raw_data, string_types) and not isinstance(raw_data, bytes):  # Needed for python3 support
            raw_data = raw_data.encode()
        
        self.attachments.append({
            "filename": filename,
            "base64": base64.b64encode(raw_data) 
        })
        
    def get_attachments(self):
        """Get attachments fit for a key output in Swimlane

        Examples:
            All files to key "output_files"::
            
                >>>swa = SwimlaneAttachments()
                >>>swa.add_attachment("myfile.txt", "asdf")
                >>>output["output_files"] = swa.get_attachments()

        Returns:
            Attachments for output in a key in Swimlane

        """
        return self.attachments


def check_input(in_val, exp_val, flags=None, mapping=None, options=None):
    """Shorthand function for creating an InputChecker()

    Args:
        in_val: Value to check
        exp_val: Expected value(s)
        flags: Optional flags to pass to InputChecker
        mapping: Optional mapping to pass to InputChecker
        options: Optional options to pass to InputChecker

    Raises:
        SwimlaneIntegrationException: if the parsed or checked value fails

    Returns:
        Parsed and Checked Value

    """
    return InputChecker(flags=flags, mapping=mapping, options=options).check(in_val, exp_val)


def create_test_conn(base_cls, execute_func=None):
    """Create a test connection base class

    Examples:
        Create a basic integration for MyIntegration::
            >>>SwMain = create_test_conn(MyIntegration)
        Create a basic integration for MyIntegration with auth function name "auth"
            >>>SwMain = create_test_conn(MyIntegration, "auth")

    Args:
        base_cls: a Classtype of the ABCIntegration
        execute_func: the name of the function to call during execute, such as 'login'

    Returns:
        TestConnection class

    """

    class SwMain(object):
        def __init__(self, context):
            self.context = context

        def execute(self):
            try:
                c = base_cls(self.context)
                if execute_func:
                    getattr(c, execute_func)()
                return {"successful": True}
            except Exception as e:
                return {"successful": False, "errorMessage": str(e)}
    return SwMain


class InputChecker(object):
    STOP_VALIDATION = StopValidation

    def __init__(self, flags=None, mapping=None, options=None):
        """Check the validity of a given set of inputs
        Apply Order:
        1. flags
        2. mappings
        3. options

        Args:
            options: Special options to apply to given inputs, such as {"type": "int"}
            mapping: Change the inputs to another set, such as {True: "enable", False: "disable"}
            flags: Function to apply to input before any checking, like ["lower"]

        """

        self.options = options or {}  # {"type": "int"} etc
        self.mapping = mapping or {}  # {False: "disable"} etc
        self.flags = set(flags) if flags else set()  # ["lower"]
        self.validators = Validators()

        # TODO link inputs? if a and b -> good else bad
        # TODO Wait until .validate() is called to check all inputs (possibility for linked inputs?)

        self.flag_funcs = {
            "lower": lambda x: x.lower(),
            "caps": lambda x: x.upper(),
            "optional": lambda x: InputChecker.STOP_VALIDATION if x is None else x
            # Stop validation on optional if it's None
        }

        self.option_funcs = {
            "type": self.validators.get_type_validators()
        }

    def parse(self, val, flags=None, mapping=None, options=None):
        """Apply Order:
        1. flags
        2. mappings
        3. options

        All applied parameters will be merged with parameters set in __init__, taking priority
        
        Args:
            val: Value to parse
            options: Special options to apply to given inputs, such as ``{"type": "int"}``
            mapping: Change the inputs to another set, such as ``{True: "enable", False: "disable"}``
            flags: Function to apply to input before any checking, like ``["lower"]``

        Returns:
            Parsed value before checking

        """
        if not flags:
            flags = self.flags
        else:
            flags = self.flags.union(flags)

        if not options:
            options = self.options
        else:
            options.update(self.options)

        if not mapping:
            mapping = self.mapping
        else:
            mapping.update(self.mapping)

        # flags, mappings, options
        # Flags
        for flag in flags:
            if flag in self.flag_funcs:
                val = self.flag_funcs[flag](val)
            else:
                raise ValueError("Invalid flag '{}'".format(flag))

        # mappings
        if val in mapping:
            val = mapping[val]

        # options
        for option_k, option_v in six.iteritems(options):
            if option_k in self.option_funcs:
                if option_v in self.option_funcs[option_k]:
                    val = self.option_funcs[option_k][option_v](val)
                else:
                    raise ValueError("Invalid option value '{}'".format(option_v))
            else:
                raise ValueError("Invalid option '{}'".format(option_k))

        return val

    def check(self, val, expected=None, flags=None, mapping=None, options=None):
        """Check a value with given expected output, flags, mapping, and options
        
        Args:
            val: Value to check
            expected: Expected value(s) (can be a list or None if just type checking)
            flags: list of flags to apply
            mapping: dict to map values to 
            options: options to change how val is parsed

        Returns:
            Parsed and checked value

        """
        try:
            val = self.parse(val, flags=flags, mapping=mapping, options=options)
        except ValidationFailure as e:
            raise SwimlaneIntegrationException("Invalid value '{val}' Exception: {e}".format(val=val, e=str(e)))

        if val == InputChecker.STOP_VALIDATION:  # Parsed value says to stop validation, return None
            return None

        if expected is not None:  # If expected is None, the validation has been done in the .parse()
            if val not in expected:
                raise SwimlaneIntegrationException("Unexpected value '{}', must be one of '{}'".format(val, expected))

        return val

def parse_datetime(param_name, param_value):
    try:
        datetime = QueryStringParser.is_datetime(param_value)
    except SwimlaneIntegrationException as e:
        raise InvalidInput(e.message,
                           input_name=param_name,
                           input_value=param_value)
    if datetime is None:
        raise InvalidInput("Unknown datetime format",
                           input_name=param_name,
                           input_value=param_value)
    return datetime


class QueryStringParser(object):
    def __init__(self, string, delimiter=",", assigner="=", try_type=False, allow_relative_time=False):
        """
        Parse a given query string into parameters, such as 'key1=value1,key2=value2'
        Args:
            string: list of data coming in to parse
            delimiter: Entry separator character, defaults to ',' (entry1,entry2)
            assigner: Entry key-value separator, defaults to '=' (key=value)
            try_type: Try to type the incoming values to int, datetime, boolean, or string
                        if try_type is a function, it should have a definition like:
                        try_type({data_dict}) -> {new_data_dict}
                        Will overwrite the type guessed
            allow_relative_time: If True, will allow values to be passed in as {time.now():+5minute} and converted to pendulum
        """
        self.delm = delimiter
        self.asgn = assigner
        self.try_type = try_type
        self._try_isfunc = bool(isinstance(self.try_type, FuncTypes))

        self._raw_string = string
        self.data = {}

    @staticmethod
    def is_int(val):
        try:
            return int(val)
        except ValueError:
            return None

    @staticmethod
    def is_datetime(val):
        """
        :param val: A string representing a datetime.
        This can be any standard datetime format supported by pendulum or a relative datetime.
        Relative datetime format:
            {time.now():(+/-)(integer)(milliseconds|seconds|minutes|days|weeks|months|years)}
        examples:
            {time.now():+0days}
            {time.now():-1months}
            {time.now():+3days}
            {time.now():-123seconds}

        :return: a pendulum object for the datetime
        """
        if isinstance(val, StringTypes) and val.startswith("{time.now():") and val.endswith("}"):
            # allows years, months, weeks, days, minutes, seconds, milliseconds
            _, time_val = val.split(":")
            is_add = time_val.startswith("+")
            if not is_add and not time_val.startswith("-"):
                raise SwimlaneIntegrationException("Time value must contain a + or - modifier!")
            if is_add:
                fn_name = "add"
            else:
                fn_name = "subtract"

            time_val = time_val[1:]  # Chop off +/-
            time_val = time_val[:-1]  # Chop off ending '}'

            match = re.match("^(\d*)", time_val)
            if not match:
                raise SwimlaneIntegrationException("Invalid time value! must be in format <int><time value>. See README for examples.")
            timespan_name = time_val[match.end():]
            timespan_val = time_val[:match.end()]

            try:
                timespan_val = int(timespan_val)
            except ValueError:
                raise SwimlaneIntegrationException("Value provided '{}' does not typecast to int!".format(timespan_val))

            dt = pendulum.now()
            return getattr(dt, fn_name)(**{timespan_name: int(timespan_val)})
        else:
            f = Flattener()
            dt = f._try_parse_dt(val, is_number=False)
            try:
                return pendulum.parse(dt)
            except:
                return None

    def _typecast(self):
        # Take in the string values and turn them into int bool or string
        new_data = {}
        
        for k, v in self.data.items():
            if isinstance(v, StringTypes):
                if v.lower() == "true":  # Bool case
                    new_data[k] = True
                elif v.lower() == "false":  # Bool case
                    new_data[k] = False
                elif self.is_int(v) is not None:  # Int case
                    new_data[k] = int(v)
                elif self.is_datetime(v) is not None:  # Datetime case
                    new_data[k] = self.is_datetime(v)
                else:
                    new_data[k] = v  # Can't figure out what it is, must leave as a string
            else:
                new_data[k] = v  # v is already a nonstring type
        
        return new_data

    def parse(self):
        try:
            pairs = self._raw_string.split(self.delm)
            
            for pair in pairs:
                k, v = pair.split(self.asgn)
                self.data[k] = v
            
            if not self.try_type:
                return self.data
            else:
                data = self._typecast()
                if self._try_isfunc:
                    data = self.try_type(data)
                return data
        except Exception as e:
            raise SwimlaneIntegrationException("Exception parsing QueryString, most likely malformed input! Error: {}".format(str(e)))
