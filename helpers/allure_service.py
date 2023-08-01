import os
import json


def get_allure_report_data(allure_report_dir):
    path_to_file = os.path.join(allure_report_dir, 'allure-report', 'widgets', 'duration.json')
    with open(path_to_file, "r", encoding='utf-8') as f:
        data = json.load(f)
        return data


def get_allure_link(env_name):
    try:
        allure_link = os.environ[env_name]
    except (KeyError, TypeError):
        allure_link = "link not found"
    return allure_link


def generate_failed_tests_list(data):
    fail_test_list = []
    for test_item in data:
        if test_item["status"] != "passed" and test_item["status"] != "skipped":
            test_name = test_item["name"]
            fail_test_list.append(test_name.replace('test_', ''))
    return "\n".join(fail_test_list)


def count_failed_and_collected_tests(data):
    sum_failed_tests = []
    collected_tests = []
    for test_item in data:
        if test_item["status"] != "passed":
            test_name = test_item["name"]
            sum_failed_tests.append(test_name)
        test_name = test_item["name"]
        collected_tests.append(test_name)
    return len(sum_failed_tests), len(collected_tests)
