import requests
from json import loads, dumps


POST_METHOD = "POST"
GET_METHOD = "GET"
ENCODING_UTF8 = "utf-8"


class SwgohHelperClient:
    """
    The api.swgoh.help client, will be used to request from the exposed api.
    """

    def __init__(self, _credentials):
        """
        Builds the instance.

        :param _credentials: The credentials to sign in https://api.swgoh.help.
        """

        self.api_user = "username=" + _credentials.username
        self.api_user += "&password=" + _credentials.password
        self.api_user += "&grant_type=password"
        self.api_user += "&client_id=" + _credentials.client_id
        self.api_user += "&client_secret=" + _credentials.client_secret

        self.base_url = "https://api.swgoh.help"
        self.sign_in = "/auth/signin"

        self.data_type = {
            "guild": "/swgoh/guild/",
            "player": "/swgoh/player/",
            "data": "/swgoh/data/",
            "units": "/swgoh/units",
            "battles": "/swgoh/battles"
        }

        self.token = ""

    def __get_token(self):
        """
        Retrieves the api token needed to use the api.

        :return: An authorization token given by api.swgoh.help
        """

        sign_in_url = self.base_url + self.sign_in
        data = self.api_user

        header = {
            "Content-type": "application/x-www-form-urlencoded",
            "Content-Length": str(len(data))
        }

        request = requests.request(POST_METHOD, sign_in_url, headers=header, data=data, timeout=10)

        if request.status_code != 200:
            error_message = "Wrong credentials, please provide the correct ones."

            return {
                "status_code": request.status_code,
                "error_message": error_message
            }

        access_token = loads(request.content.decode(ENCODING_UTF8))["access_token"]

        self.token = {"Authorization": "Bearer " + access_token}

        return self.token

    def get_data(self, data_type, request_json):
        """
        For data_type specify a valid data_criteria.
        Beware that data_type 'player' and 'guild', do not require a data_criteria.

        :param data_type: Guild, Player, Units or Data
        :param request_json: The json with the request information
        :return: The response from swgoh.help to the requested data
        """

        access_token = self.__get_token()
        head = {"Method": "POST", "Content-Type": "application/json",
                "Authorization": access_token["Authorization"]}
        request_url = self.base_url + self.data_type[data_type]

        try:
            request = requests.request(POST_METHOD, url=request_url,
                                       headers=head, data=dumps(request_json))
            print(request)

            if request.status_code != 200:
                error_message = "Could not fetch the data requested. HTTP Error."

                response = {
                    "status_code": request.status_code,
                    "error_message": error_message
                }
            else:
                response = loads(request.content.decode(ENCODING_UTF8))
        except requests.exceptions.RequestException as e:
            response = {"error_message": e}

        return response


class Credentials:
    """
    Credentials to be used by the api.swgoh.help client.
    """

    def __init__(self, _username, _password, _client_id, _client_secret):
        """
        Builds the instance.

        :param _username: The username (Provided by swgoh.help team)
        :param _password: The password (Provided by swgoh.help team)
        :param _client_id: Might be needed later, for the time being use any string
        :param _client_secret: Might be needed later, for the time being use any string
        """
        self.username = _username
        self.password = _password
        self.client_id = _client_id
        self.client_secret = _client_secret
