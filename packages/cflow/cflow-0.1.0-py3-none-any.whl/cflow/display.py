def translate_status_code(status_code):
    '''
    Translates a status code (_e.g._ `COMPLETE') into a human-readable representation (_e.g._ `complete').

    Args:
        status_code (str): The status code for a process.

    Returns:
        translate_status_code (str): A human-readable representation.
    '''
    return status_code.lower()
