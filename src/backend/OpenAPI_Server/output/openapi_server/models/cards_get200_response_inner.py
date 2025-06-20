from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class CardsGet200ResponseInner(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, card_id=None, name=None, description=None, type=None):  # noqa: E501
        """CardsGet200ResponseInner - a model defined in OpenAPI

        :param card_id: The card_id of this CardsGet200ResponseInner.  # noqa: E501
        :type card_id: str
        :param name: The name of this CardsGet200ResponseInner.  # noqa: E501
        :type name: str
        :param description: The description of this CardsGet200ResponseInner.  # noqa: E501
        :type description: str
        :param type: The type of this CardsGet200ResponseInner.  # noqa: E501
        :type type: str
        """
        self.openapi_types = {
            'card_id': str,
            'name': str,
            'description': str,
            'type': str
        }

        self.attribute_map = {
            'card_id': 'cardId',
            'name': 'name',
            'description': 'description',
            'type': 'type'
        }

        self._card_id = card_id
        self._name = name
        self._description = description
        self._type = type

    @classmethod
    def from_dict(cls, dikt) -> 'CardsGet200ResponseInner':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _cards_get_200_response_inner of this CardsGet200ResponseInner.  # noqa: E501
        :rtype: CardsGet200ResponseInner
        """
        return util.deserialize_model(dikt, cls)

    @property
    def card_id(self) -> str:
        """Gets the card_id of this CardsGet200ResponseInner.


        :return: The card_id of this CardsGet200ResponseInner.
        :rtype: str
        """
        return self._card_id

    @card_id.setter
    def card_id(self, card_id: str):
        """Sets the card_id of this CardsGet200ResponseInner.


        :param card_id: The card_id of this CardsGet200ResponseInner.
        :type card_id: str
        """

        self._card_id = card_id

    @property
    def name(self) -> str:
        """Gets the name of this CardsGet200ResponseInner.


        :return: The name of this CardsGet200ResponseInner.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this CardsGet200ResponseInner.


        :param name: The name of this CardsGet200ResponseInner.
        :type name: str
        """

        self._name = name

    @property
    def description(self) -> str:
        """Gets the description of this CardsGet200ResponseInner.


        :return: The description of this CardsGet200ResponseInner.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this CardsGet200ResponseInner.


        :param description: The description of this CardsGet200ResponseInner.
        :type description: str
        """

        self._description = description

    @property
    def type(self) -> str:
        """Gets the type of this CardsGet200ResponseInner.


        :return: The type of this CardsGet200ResponseInner.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this CardsGet200ResponseInner.


        :param type: The type of this CardsGet200ResponseInner.
        :type type: str
        """

        self._type = type
