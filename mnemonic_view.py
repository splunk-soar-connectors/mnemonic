# --
# File: mnemonic_view.py
#
# Copyright (c) Phantom Cyber Corporation, 2017
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --


import phantom.app as phantom


def get_ctx_result(result):

    ctx_result = {}
    param = result.get_param()
    summary = result.get_summary()
    data = result.get_data()

    ctx_result['param'] = param

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
        curr_item['answer_contains'] = 'ip'

        answer = curr_item.get('answer')
        if ((answer) and (not phantom.is_ip(answer))):
            curr_item['answer_contains'] = 'domain'

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
