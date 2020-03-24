def first_for_key(doc, key):
    try:
        result = [x.get('value', None) for x in doc.get('data', []) if x.get('key', '') == key][0]
    except LookupError:
        result = None
    return result

def all_alerts(payload):
    return u", ".join([
        '"%s"' % (a['query']['description'],) for a in payload['alerts']])

def filter_functions():
    return {
        'poliscoops_first_for_key': first_for_key,
        'poliscoops_all_alerts': all_alerts
    }
