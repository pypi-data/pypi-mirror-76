def remap_dict(orig_dict, mapper={}, const={}, passthrough=set(), transformer={}):
    new_dict = {}
    for key in passthrough:
        new_dict[key] = orig_dict[key]
    for key, val in const.items():
        new_dict[key] = val
    for key, val in mapper.items():
        new_dict[key] = orig_dict[val]
    for key, val in transformer.items():
        new_dict[key] = val(orig_dict)
    return new_dict
