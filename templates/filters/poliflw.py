def first_for_key(doc, key):
    try:
        result = [x.get('value', None) for x in doc.get('data', []) if x.get('key', '') == key][0]
    except LookupError:
        result = None
    return result


def filter_functions():
    return {
        'poliflw_first_for_key': first_for_key,
    }
