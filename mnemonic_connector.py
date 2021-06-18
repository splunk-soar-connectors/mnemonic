# --
# File: mnemonic_connector.py
#
# Copyright (c) 2017-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
#
# --

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

from mnemonic_consts import *
import requests
import json
import time
from bs4 import BeautifulSoup


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class RetVal3(tuple):
    def __new__(cls, val1, val2=None, val3=None):
        return tuple.__new__(RetVal, (val1, val2, val3))


class MnemonicConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(MnemonicConnector, self).__init__()

        self._state = None

        self._base_url = None

        self._domain = None

    def _process_empty_reponse(self, response, action_result):

        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        # process the error returned in the response
        message = "Response from server. Status Code: {0}. Details: None".format(response.status_code)

        return RetVal(action_result.set_status(phantom.APP_ERROR, message))

    def _process_html_response(self, response, action_result):

        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code,
                error_text)

        message = message.replace('{', '{{').replace('}', '}}')

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):

        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(str(e))), None)

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace('{', '{{').replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):

        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if 'json' in r.headers.get('Content-Type', ''):
            return self._process_json_response(r, action_result)

        # Process an HTML resonse, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_reponse(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace('{', '{{').replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, headers=None, params=None, data=None, method="get"):

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), resp_json)

        # Create a URL to connect to
        url = self._base_url + endpoint

        try:
            r = request_func(
                            url,
                            data=data,
                            headers=headers,
                            params=params,
                            timeout=20)
        except Exception as e:
            return RetVal(action_result.set_status( phantom.APP_ERROR, "Error Connecting to server. Details: {0}".format(str(e))), resp_json)

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Querying a domain to test connectivity to {0}/{1} ".format(self._base_url, self._domain))

        # make rest call
        ret_val, response = self._make_rest_call('/{0}'.format(self._domain), action_result, params={'limit': 1, 'offset': 0})

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            self.save_progress(MNEMONIC_ERR_TEST_CONNECTIVITY)
            return action_result.get_status()

        self.save_progress(MNEMONIC_SUCCESS_TEST_CONNECTIVITY)
        return action_result.set_status(phantom.APP_SUCCESS)

    def _parse_range(self, min_max, action_result):

        try:
            mini, maxi = (int(x) for x in min_max.split('-'))
        except:
            return RetVal3(action_result.set_status(phantom.APP_ERROR, MNEMONIC_ERR_PARSE_RANGE))

        if (mini < 0) or (maxi < 0):
            return RetVal3(action_result.set_status(phantom.APP_ERROR, MNEMONIC_ERR_INVALID_OFFSET_RANGE, ))

        if mini > maxi:
            return RetVal3(action_result.set_status(phantom.APP_ERROR, MNEMONIC_ERR_INVALID_RANGE))

        limit = maxi - mini

        if limit == 0:
            limit = 1

        return phantom.APP_SUCCESS, mini, limit

    def _handle_lookup_domain(self, param):

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary

        domain = param['domain']

        min_max = param.get('range', MNEMONIC_DEFAULT_RANGE)

        ret_val, offset, limit = self._parse_range(min_max, action_result)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        if phantom.is_url(domain):
            domain = phantom.get_host_from_url(domain)

        endpoint = '/{0}'.format(domain)

        params = {'offset': offset, 'limit': limit}

        # make rest call
        ret_val, response = self._make_rest_call(endpoint, action_result, params=params)

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # so just return from here
            return action_result.get_status()

        # Now post process the data
        data = response.get('data')

        try:
            message = response['messages'][0]['messageTemplate']
        except:
            message = ''

        if data is None:
            return action_result.set_status(phantom.APP_SUCCESS, "No data returned. {}".format(message if message else ''))

        if type(data) != list:
            data = [data]

        for curr_item in data:
            try:
                curr_item['lastSeenTimestampString'] = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(curr_item['lastSeenTimestamp'] / 1000))
            except:
                pass
            try:
                curr_item['firstSeenTimestampString'] = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(curr_item['firstSeenTimestamp'] / 1000))
            except:
                pass

            action_result.add_data(curr_item)

        summary = action_result.update_summary({})
        summary['items_returned'] = action_result.get_data_size()

        try:
            summary['total_items'] = response.get('count')
        except:
            pass

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'lookup_domain':
            ret_val = self._handle_lookup_domain(param)

        return ret_val

    def initialize(self):

        config = self.get_config()

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        self._base_url = MNEMONIC_BASE_URL

        self._domain = config.get('domain', 'phantom.us')

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved accross actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if username and password:
        try:
            print("Accessing the Login page")
            r = requests.get("https://127.0.0.1/login", verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = 'https://127.0.0.1/login'

            print("Logging into Platform to get the session id")
            r2 = requests.post("https://127.0.0.1/login", verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platfrom. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = MnemonicConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)
