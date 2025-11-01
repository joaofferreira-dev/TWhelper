import os


def get_csv_file(filename):
    """
    Method to return the file path given a csv filename.
    :param filename: The csv file name
    :return: The path to the csv file
    """
    return os.path.join(os.path.dirname(__file__), filename)
