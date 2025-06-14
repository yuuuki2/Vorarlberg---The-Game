import unittest

from flask import json

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
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_bus_routes_get(self):
        """Test case for bus_routes_get

        Get all bus routes
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/bus/routes',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_bus_stops_get(self):
        """Test case for bus_stops_get

        Get all bus stops
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/bus/stops',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_bus_stops_in_range_get(self):
        """Test case for bus_stops_in_range_get

        Get bus stops in range
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/bus/stops/in-range',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cards_card_id_discard_post(self):
        """Test case for cards_card_id_discard_post

        Discard a card
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/cards/{card_id}/discard'.format(card_id='card_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cards_card_id_use_post(self):
        """Test case for cards_card_id_use_post

        Use a card
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/cards/{card_id}/use'.format(card_id='card_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_cards_get(self):
        """Test case for cards_get

        Get card hand info
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/cards',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_curses_curse_id_complete_post(self):
        """Test case for curses_curse_id_complete_post

        Complete a curse
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/curses/{curse_id}/complete'.format(curse_id='curse_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_curses_get(self):
        """Test case for curses_get

        Get current curses info
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/curses',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_exists_get(self):
        """Test case for exists_get

        Check if server exists
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/exists',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_game_end_post(self):
        """Test case for game_end_post

        End game
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/game/end',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_game_info_get(self):
        """Test case for game_info_get

        Get game info
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/game/info',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_game_start_post(self):
        """Test case for game_start_post

        Start game
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/game/start',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_game_swap_roles_post(self):
        """Test case for game_swap_roles_post

        Swap hider and seeker
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/game/swap-roles',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_hider_bus_stop_bus_stop_id_post(self):
        """Test case for hider_bus_stop_bus_stop_id_post

        Set hiding bus stop
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/hider/bus-stop/{bus_stop_id}'.format(bus_stop_id='bus_stop_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_hider_get_coordinates_get(self):
        """Test case for hider_get_coordinates_get

        Get coordinates of hider
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/hider/get_coordinates',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_hider_info_get(self):
        """Test case for hider_info_get

        Get hider info
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/hider/info',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_hider_post_coordinates_post(self):
        """Test case for hider_post_coordinates_post

        Post coordinates of hider
        """
        seeker_post_coordinates_post_request = openapi_server.SeekerPostCoordinatesPostRequest()
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/hider/post_coordinates',
            method='POST',
            headers=headers,
            data=json.dumps(seeker_post_coordinates_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_questions_answer_post(self):
        """Test case for questions_answer_post

        Answer current question
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/questions/answer',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_questions_ask_question_id_post(self):
        """Test case for questions_ask_question_id_post

        Ask a question
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/questions/ask/{question_id}'.format(question_id='question_id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_questions_current_get(self):
        """Test case for questions_current_get

        Get currently asked question info
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/questions/current',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_questions_get(self):
        """Test case for questions_get

        Get all questions
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/questions',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_questions_previous_get(self):
        """Test case for questions_previous_get

        Get previously asked questions info
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/questions/previous',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_questions_veto_post(self):
        """Test case for questions_veto_post

        Veto current question
        """
        headers = { 
        }
        response = self.client.open(
            '/api/v1/questions/veto',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_seeker_get_coordinates_get(self):
        """Test case for seeker_get_coordinates_get

        Get coordinates of seeker
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/seeker/get_coordinates',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_seeker_info_get(self):
        """Test case for seeker_info_get

        Get seeker info
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/seeker/info',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_seeker_post_coordinates_post(self):
        """Test case for seeker_post_coordinates_post

        Post coordinates of seeker
        """
        seeker_post_coordinates_post_request = openapi_server.SeekerPostCoordinatesPostRequest()
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/seeker/post_coordinates/',
            method='POST',
            headers=headers,
            data=json.dumps(seeker_post_coordinates_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
