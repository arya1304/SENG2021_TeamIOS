from collections import OrderedDict

# This code was made via ChatGPT to convert the underscore to colon

def replace_specialchars(d):
    if isinstance(d, dict):
        return OrderedDict((k.replace("-", ":").replace("_", ":"), replace_specialchars(v)) for k, v in d.items())
    elif isinstance(d, list):
        return [replace_specialchars(i) for i in d]
    else:
        return d
    

