import requests
import logging

LOG = logging.getLogger("log")


def rpc_request(session, url, params):
    try:
        result = session.post(url=url,
                              json=params)
        response = result.json()

        error = response.get("error")
        if error:
            LOG.error("Request error: %s %s %s", error, url, params)
            LOG.exception(error)
            return None

    except requests.exceptions.RequestException as error:
        LOG.error("Request error: %s %s", url, params, error)
        LOG.exception(error)
        return None

    except Exception as error:
        LOG.error("Request error: %s %s", url, params, error)
        LOG.exception(error)
        return None

    return response
