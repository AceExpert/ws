import typing, inspect, asyncio
from inspect import Parameter

def enforce_type(func: typing.Union[typing.Callable, typing.Coroutine]):
    def wrapper(*args, **kwargs):
        defs, args, kwargs = get_defaults(func), list(args).copy(), kwargs.copy()
        for key, val in defs.items():
            if val[1] in [Parameter.POSITIONAL_ONLY, Parameter.VAR_POSITIONAL, Parameter.POSITIONAL_OR_KEYWORD] and len(args) > val[2] and key not in kwargs:
                args.insert(val[2], val[0])
            elif val[1] in [Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD] and key not in kwargs:
                kwargs[key] = val[0]
        annotation_vals = {list(func.__code__.co_varnames).index(key):vals for key, vals in func.__annotations__.items()}
        args = [annotation_vals[j](i) if j in list(annotation_vals.keys()) and i != None else i for i,j in zip(args, range(len(args)))]
        kwargs = {key:func.__annotations__[key](value) if key in func.__annotations__ and value != None else value for key, value in kwargs.items()}
        if inspect.iscoroutinefunction(func): return asyncio.run(func(*args, **kwargs))
        else: return func(*args, **kwargs)
    return wrapper

def get_defaults(func: typing.Union[typing.Callable, typing.Coroutine]):
    sig = inspect.signature(func)
    return {
        item[0]: [item[1].default, item[1].kind, ind] for item, ind in zip(sig.parameters.items(), range(len(sig.parameters.items()))) 
        if item[1].default is not inspect.Parameter.empty
    }