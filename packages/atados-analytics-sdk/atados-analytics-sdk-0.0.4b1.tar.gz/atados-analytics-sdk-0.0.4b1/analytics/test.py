import unittest
import responses
from unittest.mock import MagicMock
from errors import AnalyticsGraphQLError
from analytics import Analytics, GQL_TRACK_QUERY
import json

API_URL = "http://mock-api/"
API_TOKEN = "<mock-token>"
mock_meta = {"channel": "mock"}


class AnalyitcsTest(unittest.TestCase):
  def test_init_sdk(self):
    analytics = Analytics(api_url=API_URL, api_token=API_TOKEN, meta=mock_meta)
    self.assertIsInstance(analytics, Analytics)

  @responses.activate
  def test_track_request(self):
    analytics = Analytics(api_url=API_URL, api_token=API_TOKEN, meta=mock_meta)
    # Mock response
    responses.add(responses.POST, API_URL, json={'data': {}}, status=200)
    track_result = analytics.track(category='Category',
                                   label='Label',
                                   action={'data': 1},
                                   user_id=1)
    req = responses.calls[0].request
    res = responses.calls[0].response
    self.assertEqual(len(responses.calls), 1)
    self.assertEqual(req.url, API_URL)
    self.assertEqual(req.headers['Content-Type'], 'application/json')
    self.assertEqual(req.headers['Authorization'], 'Bearer ' + API_TOKEN)
    self.assertDictEqual(
        json.loads(req.body), {
            'query': GQL_TRACK_QUERY,
            'variables': {
                "category": 'Category',
                "label": 'Label',
                "action": {
                    'data': 1
                },
                "meta": mock_meta,
                "userId": 1,
                "sessionId": None
            }
        })
    self.assertEqual(res.text, '{"data": {}}')
    self.assertEqual(track_result, True)

  @responses.activate
  def test_track_report_error(self):
    on_error_mock = MagicMock(return_value=None)
    analytics = Analytics(api_url=API_URL,
                          api_token=API_TOKEN,
                          on_error=on_error_mock,
                          meta=mock_meta)
    # Mock response
    responses.add(responses.POST,
                  API_URL,
                  json={'errors': [{
                      'message': '<error>'
                  }]},
                  status=200)
    track_result = analytics.track(category='Category',
                                   label='Label',
                                   action='Action',
                                   user_id=1)
    self.assertEqual(track_result, False)
    on_error_mock.assert_called_once()


if __name__ == '__main__':
  unittest.main()
