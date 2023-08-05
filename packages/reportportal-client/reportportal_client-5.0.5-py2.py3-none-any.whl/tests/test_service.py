"""This modules includes unit tests for the service.py module."""

from datetime import datetime

import pytest
from delayed_assert import assert_expectations, expect
from pkg_resources import DistributionNotFound
from six.moves import mock

from reportportal_client.service import (
    _convert_string,
    _dict_to_payload,
    _get_data,
    _get_id,
    _get_json,
    _get_messages,
    _get_msg,
    ReportPortalService
)


class TestServiceFunctions:
    """This class contains test methods for helper functions."""

    def test_check_convert_to_string(self):
        """Test for support and convert strings to utf-8."""
        expect(_convert_string('Hello world') == 'Hello world')
        expect(lambda: isinstance(_convert_string('Hello world'), str))
        assert_expectations()

    @pytest.mark.parametrize('system', [True, False])
    def test_dict_to_payload_with_system_key(self, system):
        """Test convert dict to list of dicts with key system."""
        initial_dict = {'aa': 1, 'b': 2, 'system': system}
        expected_list = [{'key': 'aa', 'value': '1', 'system': system},
                         {'key': 'b', 'value': '2', 'system': system}]
        assert _dict_to_payload(initial_dict) == expected_list

    def test_get_id(self, response):
        """Test for the get_id function."""
        assert _get_id(response(200, {'id': 123})) == 123

    def test_get_msg(self, response):
        """Test for the get_msg function."""
        fake_json = {'id': 123}
        assert _get_msg(response(200, fake_json)) == fake_json

    def test_get_data(self, response):
        """Test for the get_data function."""
        fake_json = {'id': 123}
        assert _get_data(response(200, fake_json)) == fake_json

    def test_get_json(self, response):
        """Test for the get_json function."""
        fake_json = {'id': 123}
        assert _get_json(response(200, fake_json)) == fake_json

    def test_get_messages(self):
        """Test for the get_messages function."""
        data = {'responses': [{'errorCode': 422, 'message': 'error'}]}
        assert _get_messages(data) == ['422: error']


class TestReportPortalService:
    """This class stores methods which test ReportPortalService."""

    @mock.patch('reportportal_client.service._get_data')
    def test_start_launch(self, mock_get, rp_service):
        """Test start launch and sending request.

        :param mock_get:   Mocked _get_data() function
        :param rp_service: Pytest fixture
        """
        mock_get.return_value = {'id': 111}
        launch_id = rp_service.start_launch('name', datetime.now().isoformat())
        assert launch_id == 111

    @mock.patch('reportportal_client.service._get_msg')
    def test_finish_launch(self, mock_get, rp_service):
        """Test finish launch and sending request.

        :param mock_get:   Mocked _get_msg() function
        :param rp_service: Pytest fixture
        """
        mock_get.return_value = {'id': 111}
        _get_msg = rp_service.finish_launch(
            'name', datetime.now().isoformat())
        assert _get_msg == {'id': 111}

    @mock.patch('platform.system', mock.Mock(return_value='linux'))
    @mock.patch('platform.machine', mock.Mock(return_value='Windows-PC'))
    @mock.patch('platform.processor', mock.Mock(return_value='amd'))
    @mock.patch('pkg_resources.get_distribution')
    def test_get_system_information(self, distro):
        """Test for validate get_system_information."""
        distro.return_value.version = '5.0'
        expected_result = {'agent': 'reportportal-client-5.0',
                           'cpu': 'amd',
                           'machine': 'Windows-PC',
                           'os': 'linux'}
        cond = (ReportPortalService.get_system_information(
            'reportportal-client') == expected_result)
        assert cond

    @mock.patch('platform.system', mock.Mock())
    @mock.patch('platform.machine', mock.Mock())
    @mock.patch('platform.processor', mock.Mock(return_value=''))
    @mock.patch('pkg_resources.get_distribution', mock.Mock())
    def test_get_system_information_docker(self):
        """Test that cpu key value is not empty.

        platform.processor() returns empty string in case it was called
        inside of the Docker container. API does not allow empty values
        for the attributes.
        """
        result = ReportPortalService.get_system_information('pytest')
        assert result['cpu'] == 'unknown'

    @mock.patch('platform.system', mock.Mock(return_value='linux'))
    @mock.patch('platform.machine', mock.Mock(return_value='Windows-PC'))
    @mock.patch('platform.processor', mock.Mock(return_value='amd'))
    @mock.patch('pkg_resources.get_distribution',
                mock.Mock(side_effect=DistributionNotFound))
    def test_get_system_information_without_pkg(self):
        """Test in negative form for validate get_system_information."""
        expected_result = {'agent': 'not found',
                           'cpu': 'amd',
                           'machine': 'Windows-PC',
                           'os': 'linux'}

        cond = (ReportPortalService.get_system_information('pytest')
                == expected_result)
        assert cond

    @mock.patch('reportportal_client.service._get_data',
                mock.Mock(return_value={'id': 123}))
    def test_start_item(self, rp_service):
        """Test for validate start_test_item.

        :param: rp_service: fixture of ReportPortal
        """
        rp_start = rp_service.start_test_item(name='name',
                                              start_time=1591032041348,
                                              item_type='STORY')
        expected_result = dict(json={'name': 'name',
                                     'description': None,
                                     'attributes': None,
                                     'startTime': 1591032041348,
                                     'launchUuid': 111,
                                     'type': 'STORY', 'parameters': None,
                                     'hasStats': True,
                                     'codeRef': None},
                               url='http://endpoint/api/v2/project/item',
                               verify=True)

        rp_service.session.post.assert_called_with(**expected_result)
        assert rp_start == 123

    start_item_optional = [
        ('code_ref', '/path/to/test - test_item', 'codeRef',
         '/path/to/test - test_item'),
        ('attributes', {'attr1': True}, 'attributes',
         [{'key': 'attr1', 'value': 'True', 'system': False}])
    ]

    @pytest.mark.parametrize(
        'field_name,field_value,expected_name,expected_value',
        start_item_optional)
    @mock.patch('reportportal_client.service._get_data',
                mock.Mock(return_value={'id': 123}))
    def test_start_item_code_optional_params(self, rp_service, field_name,
                                             field_value, expected_name,
                                             expected_value):
        """Test for validate different fields in start_test_item.

        :param: rp_service:     fixture of ReportPortal
        :param: field_name:     a name of a field bypassed to
        rp_service.start_test_item method
        :param: field_value:    a value of a  field bypassed to
        rp_service.start_test_item method
        :param: expected_name:  a name of a field which should be in the result
        JSON request
        :param: expected_value: an exact value of a field which should be in
        the result JSON request
        """
        rp_service.start_test_item(name='name', start_time=1591032041348,
                                   item_type='STORY',
                                   **{field_name: field_value})
        expected_result = dict(json={'name': 'name',
                                     'description': None,
                                     'attributes': None,
                                     'startTime': 1591032041348,
                                     'launchUuid': 111,
                                     'type': 'STORY', 'parameters': None,
                                     'hasStats': True,
                                     'codeRef': None},
                               url='http://endpoint/api/v2/project/item',
                               verify=True)
        expected_result['json'][expected_name] = expected_value
        rp_service.session.post.assert_called_with(**expected_result)
