from collections import OrderedDict

def replace_specialchars(d):
    if isinstance(d, dict):
        return OrderedDict((k.replace("-", ":").replace("_", ":"), replace_specialchars(v)) for k, v in d.items())
    elif isinstance(d, list):
        return [replace_specialchars(i) for i in d]
    else:
        return d
    

