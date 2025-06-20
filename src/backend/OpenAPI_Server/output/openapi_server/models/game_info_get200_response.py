from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class GameInfoGet200Response(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, current_game_timer=None, hider_name=None, seeker_name=None):  # noqa: E501
        """GameInfoGet200Response - a model defined in OpenAPI

        :param current_game_timer: The current_game_timer of this GameInfoGet200Response.  # noqa: E501
        :type current_game_timer: int
        :param hider_name: The hider_name of this GameInfoGet200Response.  # noqa: E501
        :type hider_name: str
        :param seeker_name: The seeker_name of this GameInfoGet200Response.  # noqa: E501
        :type seeker_name: str
        """
        self.openapi_types = {
            'current_game_timer': int,
            'hider_name': str,
            'seeker_name': str
        }

        self.attribute_map = {
            'current_game_timer': 'currentGameTimer',
            'hider_name': 'hiderName',
            'seeker_name': 'seekerName'
        }

        self._current_game_timer = current_game_timer
        self._hider_name = hider_name
        self._seeker_name = seeker_name

    @classmethod
    def from_dict(cls, dikt) -> 'GameInfoGet200Response':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _game_info_get_200_response of this GameInfoGet200Response.  # noqa: E501
        :rtype: GameInfoGet200Response
        """
        return util.deserialize_model(dikt, cls)

    @property
    def current_game_timer(self) -> int:
        """Gets the current_game_timer of this GameInfoGet200Response.

        Current game time in seconds  # noqa: E501

        :return: The current_game_timer of this GameInfoGet200Response.
        :rtype: int
        """
        return self._current_game_timer

    @current_game_timer.setter
    def current_game_timer(self, current_game_timer: int):
        """Sets the current_game_timer of this GameInfoGet200Response.

        Current game time in seconds  # noqa: E501

        :param current_game_timer: The current_game_timer of this GameInfoGet200Response.
        :type current_game_timer: int
        """

        self._current_game_timer = current_game_timer

    @property
    def hider_name(self) -> str:
        """Gets the hider_name of this GameInfoGet200Response.


        :return: The hider_name of this GameInfoGet200Response.
        :rtype: str
        """
        return self._hider_name

    @hider_name.setter
    def hider_name(self, hider_name: str):
        """Sets the hider_name of this GameInfoGet200Response.


        :param hider_name: The hider_name of this GameInfoGet200Response.
        :type hider_name: str
        """

        self._hider_name = hider_name

    @property
    def seeker_name(self) -> str:
        """Gets the seeker_name of this GameInfoGet200Response.


        :return: The seeker_name of this GameInfoGet200Response.
        :rtype: str
        """
        return self._seeker_name

    @seeker_name.setter
    def seeker_name(self, seeker_name: str):
        """Sets the seeker_name of this GameInfoGet200Response.


        :param seeker_name: The seeker_name of this GameInfoGet200Response.
        :type seeker_name: str
        """

        self._seeker_name = seeker_name
