# from TWhelper.csv_repo.csv_files_index import get_csv_file
from TWhelper.json_repo.json_files_index import get_json_file
from TWhelper.access_repo.access_files_index import get_access_token_file
import os.path
import json


def get_file_path(filename, file_extension):
    """
    Given a file and a file extension, return the file path.
    :param filename: The file's name
    :param file_extension: The file's extension
    :return: The file's path
    """
    # if file_extension is "csv":
    # return get_csv_file(filename)
    if file_extension is "json":
        return get_json_file(filename)


def get_swgoh_access_token():
    """
    To make sure we reuse access tokens, we must save them.
    This method checks if the token exists, if it does, it uses is, otherwise
    returns -1
    :return: Either the token or -1
    """
    access_token_file = get_access_token_file("swgoh_access_token")

    if not os.path.exists(access_token_file):
        return "-1"

    with open(access_token_file, "r") as token_file:
        token = json.load(token_file)

    return token


def store_swgoh_access_token(access_token):
    """
    Saves an access token to the disk.
    :param access_token:  The access token
    """
    access_token_file = get_access_token_file("swgoh_access_token")

    with open(access_token_file, "w") as token_file:
        json.dump(access_token, token_file)


def delete_current_swgoh_access_token():
    """
    Delete an old access token.
    """
    access_token_file = get_access_token_file("swgoh_access_token")
    os.remove(access_token_file)


def file_modified_last_4_hours(file_path):
    """
    Checks if a file was modified in the last 4 hours.
    :param file_path: The path to the file
    :return: True if the file has been modified in the last 4 hours
    """
    last_modification = get_file_last_modification(file_path)

    return 0 < last_modification < 4


def get_file_last_modification(file_path):
    """
    Gets the time since last modification.
    :param file_path:  The path to the file
    :return:  The time since last modification in hours
    """

    # getmtime returns last modification in seconds
    return -1 if not os.path.exists(file_path) else os.path.getmtime(file_path)/3600
