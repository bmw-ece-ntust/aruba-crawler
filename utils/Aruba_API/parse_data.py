def parse_data(data):
    """
    Parse a string of data containing components separated by slashes.

    This function takes a string of data and splits it into components using slashes (/) as separators.
    It returns the individual components as separate values.

    Args:
        data (str): The input string containing components separated by slashes.

    Returns:
        tuple: A tuple containing the parsed components of the input data.
    """
    components = data.split('/')
    band = components[0]
    chan = components[1]
    ch_width = components[2]
    ht_type = components[3]

    return band, chan, ch_width, ht_type
