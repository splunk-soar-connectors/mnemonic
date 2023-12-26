# File: mnemonic_consts.py
#
# Copyright (c) 2017-2023 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
MNEMONIC_BASE_URL = "https://api.mnemonic.no/pdns/v3"
MNEMONIC_DEFAULT_RANGE = '0-100'
DEFAULT_TIMEOUT = 30

MNEMONIC_SUCCESS_TEST_CONNECTIVITY = "Test Connectivity Passed"
MNEMONIC_ERR_TEST_CONNECTIVITY = "Test Connectivity Failed"

MNEMONIC_ERR_PARSE_RANGE = "Unable to parse the range. Please specify the range as min_offset-max_offset"
MNEMONIC_ERR_INVALID_OFFSET_RANGE = "Invalid min or max offset value specified in range"
MNEMONIC_ERR_INVALID_RANGE = "Invalid range value, min_offset should be less than max_offset"
