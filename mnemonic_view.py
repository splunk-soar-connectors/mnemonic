# File: mnemonic_view.py
#
# Copyright (c) 2017-2025 Splunk Inc.
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
import phantom.app as phantom


def get_ctx_result(result):
    ctx_result = {}
    param = result.get_param()
    summary = result.get_summary()
    data = result.get_data()

    ctx_result["param"] = param
    ctx_result["status"] = result.get_status()
    ctx_result["message"] = result.get_message()

    domain = param["domain"]
    param["domain_contains"] = "domain"

    if phantom.is_url(domain):
        param["domain_contains"] = "url"

    if summary:
        ctx_result["summary"] = summary

    if not data:
        return ctx_result

    ctx_result["data"] = list()
    for curr_item in data:
        curr_item["answer_contains"] = "domain"

        answer = curr_item.get("answer")
        if answer:
            if phantom.is_ip(answer):
                curr_item["answer_contains"] = "ip"
            elif "::" in answer:
                curr_item["answer_contains"] = "ipv6"

        ctx_result["data"].append(curr_item)

    return ctx_result


def display_lookup_domain(provides, all_app_runs, context):
    context["results"] = results = []
    for summary, action_results in all_app_runs:
        for result in action_results:
            ctx_result = get_ctx_result(result)
            if not ctx_result:
                continue
            results.append(ctx_result)
    # print context
    return "display_lookup_domain.html"
