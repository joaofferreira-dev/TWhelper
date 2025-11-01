import os


def get_access_token_file(filename):
    """
    Method to return the file path given a json filename.
    :param filename: The json file name
    :return: The path to the json file
    """
    return os.path.join(os.path.dirname(__file__), filename)
