import os
import requests

from helpers.allure_service import generate_failed_tests_list, count_failed_and_collected_tests, \
    get_allure_report_data, get_allure_link
from settings.env_config import settings


def generate_message_for_telegram(dir_path):
    ENV = os.environ.get("ENV")
    allure_link = get_allure_link("BUILD")
    sep = '\U00002063'
    message = ""
    allure_report = get_allure_report_data(allure_report_dir=dir_path)
    failed_tests_lst = generate_failed_tests_list(data=allure_report)
    sum_failed_tests, collected_tests = count_failed_and_collected_tests(data=allure_report)
    if len(failed_tests_lst) == 0:

        if ENV == 'prod':
            message = ""

    else:
        if ENV == 'prod':
            message = \
                f"{sep}          [{ENV}]----VGZ_UI_tests---- \n" \
                f"\n" \
                f"{sep}\U0000274C{sep} Fails:\n" \
                f"{failed_tests_lst}\n" \
                f"\n" \
                f"Tests failed/total: {sum_failed_tests}/{collected_tests}\n" \
                f"\n" \
                f"Allure link: {allure_link}\n" \

        else:
            message = \
                f"{sep}          [{ENV}]----VGZ_UI_tests---- \n" \
                f"\n" \
                f"{sep}\U0000274C{sep} Fails:\n" \
                f"{failed_tests_lst}\n" \
                f"\n" \
                f"Tests failed/total: {sum_failed_tests}/{collected_tests}\n" \
                f"\n" \
                f"Allure link: {allure_link}\n"

    return message


def request_in_telegram(message, token, chat_id):
    try:
        requests.post(f'{settings.telegram.bot_url}{token}/sendMessage',
                      json=dict(chat_id=chat_id, text=message, parse_mode='html'))
    except requests.exceptions.RequestException as error:
        from start_tests import LOG
        LOG.error("Request in telegram error: %s %s %s", message, token, chat_id)
        LOG.exception(error)


def send_message_to_telegram(message, argument):
    if argument == "prod":
        request_in_telegram(message=message, token=settings.telegram.token, chat_id=settings.telegram.chat_id)

    if argument == "dev":
        request_in_telegram(message=message, token=settings.telegram.token, chat_id=settings.telegram.chat_id)

