# --
# File: mnemonic_consts.py
#
# Copyright (c) 2017-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
#
# --

MNEMONIC_BASE_URL = "https://api.mnemonic.no/pdns/v3"
MNEMONIC_DEFAULT_RANGE = '0-100'

MNEMONIC_SUCCESS_TEST_CONNECTIVITY = "Test Connectivity Passed"
MNEMONIC_ERR_TEST_CONNECTIVITY = "Test Connectivity Failed"

MNEMONIC_ERR_PARSE_RANGE = "Unable to parse the range. Please specify the range as min_offset-max_offset"
MNEMONIC_ERR_INVALID_OFFSET_RANGE = "Invalid min or max offset value specified in range"
MNEMONIC_ERR_INVALID_RANGE = "Invalid range value, min_offset should be less than max_offset"
