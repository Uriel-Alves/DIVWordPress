from test import APITest
from src.message import NOT_FOUND_MESSAGE, NOT_FOUND_ID


class DIVWordpressTestCase(APITest):

    def test_GET_post(self):
        response, status = self.request(
            url='posts',
            method='GET'
        )
        print(response)

        self.assertTrue(status < 400, 'status > 400')

    def test_success_GET_post_by_slug(self):
        response, status = self.request(
            url=f'post/{self.meta_data["posts"][-1]["name"]}',
            method='GET'
        )
        self.assertTrue(response.get('id'), NOT_FOUND_ID)
        self.assertTrue(status < 400, 'status > 400')

    def test_failure_GET_post_by_slug(self):
        try:
            response, status = self.request(
                url='post/jair-teste',
                method='GET'
            )
        except Exception as e:
            print(e)
            pass

        self.assertTrue(response.get('message'), NOT_FOUND_MESSAGE)
        self.assertTrue(status == 404, 'status != 404')