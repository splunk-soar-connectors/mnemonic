# --
# File: mnemonic_view.py
#
# Copyright (c) 2017-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
#
# --


import phantom.app as phantom


def get_ctx_result(result):

    ctx_result = {}
    param = result.get_param()
    summary = result.get_summary()
    data = result.get_data()

    ctx_result['param'] = param
    ctx_result['status'] = result.get_status()
    ctx_result['message'] = result.get_message()

    domain = param['domain']
    param['domain_contains'] = 'domain'

    if (phantom.is_url(domain)):
        param['domain_contains'] = 'url'

    if (summary):
        ctx_result['summary'] = summary

    if (not data):
        return ctx_result

    ctx_result['data'] = list()
    for curr_item in data:
        curr_item['answer_contains'] = 'domain'

        answer = curr_item.get('answer')
        if (answer):
            if (phantom.is_ip(answer)):
                curr_item['answer_contains'] = 'ip'
            elif ('::' in answer):
                curr_item['answer_contains'] = 'ipv6'

        ctx_result['data'].append(curr_item)

    return ctx_result


def display_lookup_domain(provides, all_app_runs, context):

    context['results'] = results = []
    for summary, action_results in all_app_runs:
        for result in action_results:

            ctx_result = get_ctx_result(result)
            if (not ctx_result):
                continue
            results.append(ctx_result)
    # print context
    return 'display_lookup_domain.html'
