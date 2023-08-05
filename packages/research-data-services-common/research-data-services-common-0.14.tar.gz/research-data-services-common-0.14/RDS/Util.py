import importlib
import json


def load_class_from_json(jsonStr: str):
    """
    Returns the class of the given json string.
    """

    if not isinstance(jsonStr, str):
        raise ValueError("Given parameter not a string.")

    data = jsonStr

    # FIX for json bug: Sometimes it returns a string.
    while not isinstance(data, dict):
        data = json.loads(data)

    return internal_load_class(data)


def load_class_from_dict(data: dict):
    """
    Returns the class of the given dict.
    """
    return internal_load_class(data)


def initialize_object_from_json(jsonStr: str):
    """
    Initialize and returns an object of the given json string.

    This is the easiest way to reverse the to_json method for objects from our lib folder.
    """
    return load_class_from_json(jsonStr).from_json(jsonStr)


def initialize_object_from_dict(jsonDict: dict):
    """
    Initialize and returns an object of the given dict.

    This is another easy way to reverse the to_json method for objects from our lib folder.
    """
    return load_class_from_dict(jsonDict).from_dict(jsonDict["data"])


def internal_load_class(data: dict):
    """
    For internal use only.
    """

    if not isinstance(data, dict):
        raise ValueError("Given parameter not a dict object.")

    if "type" in data:
        try:
            klass = None
            if data["type"].endswith("Token"):
                mod = importlib.import_module("RDS.Token")
                klass = getattr(mod, data["type"])
            elif data["type"].endswith("Service"):
                mod = importlib.import_module("RDS.Service")
                klass = getattr(mod, data["type"])
            elif data["type"].endswith("User"):
                mod = importlib.import_module("RDS.User")
                klass = getattr(mod, data["type"])

            if klass is not None:
                return klass

        except Exception:
            raise

        raise ValueError("given parameter is not a valid class.")
    raise ValueError("Type not specified in dict.")


def try_function_on_dict(func: list):
    """
    This method trys the given functions on the given dictionary. Returns the first function, which returns a value for given dict.

    Main purpose of this is the initialization of multiple Classes from json dicts.

    Usage:
    ```python
    func_list = [func1, func2, func3]
    x = Util.try_function_on_dict(func_list)
    object = x(objDict)
    ```

    equals to:
    ```python
    try:
        try:
            func1(objDict)
        except:
            pass
        try:
            func2(objDict)
        except:
            pass
        try:
            func3(objDict)
        except:
            pass
    except:
        raise Exception(...)
    ```

    Raise an `Exception` with all raised exception as strings, if no function returns a value for the given jsonDict.
    """

    def inner_func(jsonDict: dict):
        nonlocal func

        exp_list = []

        for f in func:
            try:
                return f(jsonDict)
            except Exception as e:
                exp_list.append(e)
                continue

        raise Exception(
            "The given jsonDict raise in all functions an exception: \n{}".format(
                "\n".join([f"Error: {type(e)}, Msg: {str(e)}" for e in exp_list])
            )
        )

    return inner_func


def monkeypatch(func_name: str = "to_json"):
    """ Module that monkey-patches json module when it's imported so
    JSONEncoder.default() automatically checks for a special "to_json()"
    method and uses it to encode the object if found.
    """
    from json import JSONEncoder, JSONDecoder

    def to_default(self, obj):
        return getattr(obj.__class__, func_name, to_default.default)(obj)

    to_default.default = JSONEncoder.default  # Save unmodified default.
    JSONEncoder.default = to_default  # Replace it.


# this part can only be used, if flask is installed. See: https://github.com/Sciebo-RDS/py-research-data-services-common#optional-dependencies
try:
    from flask.json import JSONEncoder
    from functools import wraps

    def get_json_encoder(func_name: str = "to_json"):
        """ Module that monkey-patches json module when it's imported so
        JSONEncoder.default() automatically checks for a special "to_json()"
        method and uses it to encode the object if found.
        """

        class RDSEncoder(JSONEncoder):
            def default(self, o):
                method = getattr(o, func_name, JSONEncoder.default)
                try:
                    return method()
                except:
                    try:
                        return method(o)
                    except:
                        return method(self, o)

        return RDSEncoder

    def wrap_monkeypatch(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = "app"
            if kwargs.get(key) is not None:
                app = kwargs[key]
                del kwargs[key]
                app.json_encoder = get_json_encoder(*args, **kwargs)
            else:
                try:
                    from flask import current_app

                    current_app.json_encoder = get_json_encoder(*args, **kwargs)
                except:
                    pass
            return fn(*args, **kwargs)

        return wrapper

    monkeypatch = wrap_monkeypatch(monkeypatch)

except:
    pass
