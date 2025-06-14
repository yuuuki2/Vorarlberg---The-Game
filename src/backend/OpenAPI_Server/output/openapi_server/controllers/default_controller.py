import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.bus_routes_get200_response_inner import BusRoutesGet200ResponseInner  # noqa: E501
from openapi_server.models.bus_stops_get200_response_inner import BusStopsGet200ResponseInner  # noqa: E501
from openapi_server.models.cards_get200_response_inner import CardsGet200ResponseInner  # noqa: E501
from openapi_server.models.curses_get200_response_inner import CursesGet200ResponseInner  # noqa: E501
from openapi_server.models.game_info_get200_response import GameInfoGet200Response  # noqa: E501
from openapi_server.models.hider_info_get200_response import HiderInfoGet200Response  # noqa: E501
from openapi_server.models.questions_current_get200_response import QuestionsCurrentGet200Response  # noqa: E501
from openapi_server.models.questions_get200_response_inner import QuestionsGet200ResponseInner  # noqa: E501
from openapi_server.models.questions_previous_get200_response_inner import QuestionsPreviousGet200ResponseInner  # noqa: E501
from openapi_server.models.seeker_get_coordinates_get200_response import SeekerGetCoordinatesGet200Response  # noqa: E501
from openapi_server.models.seeker_info_get200_response import SeekerInfoGet200Response  # noqa: E501
from openapi_server.models.seeker_post_coordinates_post_request import SeekerPostCoordinatesPostRequest  # noqa: E501
from openapi_server import util


def bus_routes_get():  # noqa: E501
    """Get all bus routes

     # noqa: E501


    :rtype: Union[List[BusRoutesGet200ResponseInner], Tuple[List[BusRoutesGet200ResponseInner], int], Tuple[List[BusRoutesGet200ResponseInner], int, Dict[str, str]]
    """
    return 'do some magic!'


def bus_stops_get():  # noqa: E501
    """Get all bus stops

     # noqa: E501


    :rtype: Union[List[BusStopsGet200ResponseInner], Tuple[List[BusStopsGet200ResponseInner], int], Tuple[List[BusStopsGet200ResponseInner], int, Dict[str, str]]
    """
    return 'do some magic!'


def bus_stops_in_range_get():  # noqa: E501
    """Get bus stops in range

     # noqa: E501


    :rtype: Union[List[BusStopsGet200ResponseInner], Tuple[List[BusStopsGet200ResponseInner], int], Tuple[List[BusStopsGet200ResponseInner], int, Dict[str, str]]
    """
    return 'do some magic!'


def cards_card_id_discard_post(card_id):  # noqa: E501
    """Discard a card

     # noqa: E501

    :param card_id: 
    :type card_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def cards_card_id_use_post(card_id):  # noqa: E501
    """Use a card

     # noqa: E501

    :param card_id: 
    :type card_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def cards_get():  # noqa: E501
    """Get card hand info

     # noqa: E501


    :rtype: Union[List[CardsGet200ResponseInner], Tuple[List[CardsGet200ResponseInner], int], Tuple[List[CardsGet200ResponseInner], int, Dict[str, str]]
    """
    return 'do some magic!'


def curses_curse_id_complete_post(curse_id):  # noqa: E501
    """Complete a curse

     # noqa: E501

    :param curse_id: 
    :type curse_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def curses_get():  # noqa: E501
    """Get current curses info

     # noqa: E501


    :rtype: Union[List[CursesGet200ResponseInner], Tuple[List[CursesGet200ResponseInner], int], Tuple[List[CursesGet200ResponseInner], int, Dict[str, str]]
    """
    return 'do some magic!'


def exists_get():  # noqa: E501
    """Check if server exists

    Test method for the client to see if the server exists. Should always send 200 Success. # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def game_end_post():  # noqa: E501
    """End game

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def game_info_get():  # noqa: E501
    """Get game info

     # noqa: E501


    :rtype: Union[GameInfoGet200Response, Tuple[GameInfoGet200Response, int], Tuple[GameInfoGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def game_start_post():  # noqa: E501
    """Start game

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def game_swap_roles_post():  # noqa: E501
    """Swap hider and seeker

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def hider_bus_stop_bus_stop_id_post(bus_stop_id):  # noqa: E501
    """Set hiding bus stop

     # noqa: E501

    :param bus_stop_id: 
    :type bus_stop_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def hider_get_coordinates_get():  # noqa: E501
    """Get coordinates of hider

     # noqa: E501


    :rtype: Union[SeekerGetCoordinatesGet200Response, Tuple[SeekerGetCoordinatesGet200Response, int], Tuple[SeekerGetCoordinatesGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def hider_info_get():  # noqa: E501
    """Get hider info

     # noqa: E501


    :rtype: Union[HiderInfoGet200Response, Tuple[HiderInfoGet200Response, int], Tuple[HiderInfoGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def hider_post_coordinates_post(body):  # noqa: E501
    """Post coordinates of hider

     # noqa: E501

    :param seeker_post_coordinates_post_request: 
    :type seeker_post_coordinates_post_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    seeker_post_coordinates_post_request = body
    if connexion.request.is_json:
        seeker_post_coordinates_post_request = SeekerPostCoordinatesPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def questions_answer_post():  # noqa: E501
    """Answer current question

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def questions_ask_question_id_post(question_id):  # noqa: E501
    """Ask a question

     # noqa: E501

    :param question_id: 
    :type question_id: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def questions_current_get():  # noqa: E501
    """Get currently asked question info

     # noqa: E501


    :rtype: Union[QuestionsCurrentGet200Response, Tuple[QuestionsCurrentGet200Response, int], Tuple[QuestionsCurrentGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def questions_get():  # noqa: E501
    """Get all questions

     # noqa: E501


    :rtype: Union[List[QuestionsGet200ResponseInner], Tuple[List[QuestionsGet200ResponseInner], int], Tuple[List[QuestionsGet200ResponseInner], int, Dict[str, str]]
    """
    return 'do some magic!'


def questions_previous_get():  # noqa: E501
    """Get previously asked questions info

     # noqa: E501


    :rtype: Union[List[QuestionsPreviousGet200ResponseInner], Tuple[List[QuestionsPreviousGet200ResponseInner], int], Tuple[List[QuestionsPreviousGet200ResponseInner], int, Dict[str, str]]
    """
    return 'do some magic!'


def questions_veto_post():  # noqa: E501
    """Veto current question

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def seeker_get_coordinates_get():  # noqa: E501
    """Get coordinates of seeker

     # noqa: E501


    :rtype: Union[SeekerGetCoordinatesGet200Response, Tuple[SeekerGetCoordinatesGet200Response, int], Tuple[SeekerGetCoordinatesGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def seeker_info_get():  # noqa: E501
    """Get seeker info

     # noqa: E501


    :rtype: Union[SeekerInfoGet200Response, Tuple[SeekerInfoGet200Response, int], Tuple[SeekerInfoGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def seeker_post_coordinates_post(body):  # noqa: E501
    """Post coordinates of seeker

     # noqa: E501

    :param seeker_post_coordinates_post_request: 
    :type seeker_post_coordinates_post_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    seeker_post_coordinates_post_request = body
    if connexion.request.is_json:
        seeker_post_coordinates_post_request = SeekerPostCoordinatesPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
