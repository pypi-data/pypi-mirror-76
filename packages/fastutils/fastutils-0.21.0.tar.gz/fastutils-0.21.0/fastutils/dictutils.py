# -*- coding: utf-8 -*-

def deep_merge(target, data):
    for key2, value2 in data.items():
        value1 = target.get(key2, None)
        if isinstance(value1, dict) and isinstance(value2, dict):
            deep_merge(value1, value2)
        else:
            target[key2] = value2


def select(data, path, default_value=None):
    paths = path.split(".")
    for path in paths:
        if isinstance(data, dict) and path in data:
            data = data[path]
        elif isinstance(data, (list, tuple)) and path.isdigit() and int(path) < len(data):
            data = data[int(path)]
        else:
            return default_value
    return data


def update(data, path, value):
    paths = path.split(".")
    for index in range(0, len(paths) - 1):
        path = paths[index]
        path_next = paths[index + 1]

        if isinstance(data, dict) and path in data:
            data = data[path]
        elif isinstance(data, list) and int(path) < len(data):
            data = data[int(path)]
        else:
            if isinstance(data, list) and int(path) >= len(data):
                for _ in range(int(path) + 1 - len(data)):
                    data.append(None)
            if path_next.isdigit():
                next_value = []
            else:
                next_value = {}
            if path.isdigit():
                data[int(path)] = next_value
                data = data[int(path)]
            else:
                data[path] = next_value
                data = data[path]
    path = paths[-1]
    if path.isdigit():
        for _ in range(int(path) + 1 - len(data)):
            data.append(None)
        data[int(path)] = value
    else:
        data[path] = value

def ignore_none_item(data):
    result = {}
    for key, value in data.items():
        if value is None:
            continue
        if not value:
            if isinstance(value, (list, dict)):
                continue
        result[key] = value
    return result


class Object(dict):

    def __setitem__(self, key, value):
        result = super().__setitem__(key, value)
        self.__dict__[key] = value
        return result

    def __setattr__(self, name, value):
        self[name] = value
        result = super().__setattr__(name, value)
        return result

def to_object(data):
    result = Object()
    for key, value in data.items():
        if isinstance(value, dict):
            value = to_object(value)
        result[key] = value
        setattr(result, key, value)
    return result

def change(object_instance, data_dict : dict, object_key : str, dict_key : str = None) -> bool:
    """Update property value of object_instance, using the value from data_dict. If value changed, return True. If value is equals, return False.
    """
    dict_key = dict_key or object_key
    object_value = getattr(object_instance, object_key, None)
    dict_value = data_dict.get(dict_key, None)
    if object_value == dict_value:
        return False
    else:
        setattr(object_instance, object_key, dict_value)
        return True

def changes(object_instance, data_dict, keys) -> bool:
    """Update property values of object_instance, using the value form data_dict. If any property changed, return True. If values are equal, return False. keys is a list of string or string pair.
    """
    result = False
    for key in keys:
        if isinstance(key, (tuple, set, list)) and len(key) > 1:
            object_key = key[0]
            dict_key = key[1]
        else:
            object_key = key
            dict_key = None
        changed = change(object_instance, data_dict, object_key, dict_key)
        if changed:
            result = True
    return result
