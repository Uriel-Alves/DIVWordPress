from asc.core.ABC.UnitTestCase import ASCUnitTestCase, request_response
from src.message import NOT_FOUND_MESSAGE, NOT_FOUND_ID


class DIVWordpressTestCase(ASCUnitTestCase):

    def test_GET_post(self):
        response = request_response(
            url='posts',
            method='GET'
        )
        response_json = response.json()
        self.assertTrue(response.status_code < 400, 'status > 400')


    def test_success_GET_post_by_slug(self):
        response = request_response(
            url='post/jair-sampaio',
            method='GET'
        )
        response_json = response.json()
        self.assertTrue(response_json.get('id'), NOT_FOUND_ID)
        self.assertTrue(response.status_code < 400, 'status > 400')

    def test_failure_GET_post_by_slug(self):
        try:
            response = request_response(
                url='post/jair-teste',
                method='GET'
            )
        except Exception as e:
            print(e)
            pass

        response_json = response.json()
        self.assertTrue(response_json.get('message'), NOT_FOUND_MESSAGE)
        self.assertTrue(response.status_code == 404, 'status != 404')