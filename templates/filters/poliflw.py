def first_for_key(doc, key):
    try:
        result = [x.get('value', None) for x in doc.get('data', []) if x.get('key', '') == key][0]
    except LookupError:
        result = None
    return result


def party_and_location(doc):
    party = first_for_key('parties')
    location = first_for_key('location')

    if location is not None:
        if location in party:
            return party
        else:
            return "%s %s" % (party, location,)
    else:
        return party


def filter_functions():
    return {
        'poliflw_first_for_key': first_for_key,
        'poliflw_party_and_location': party_and_location
    }
