import requests
from factionpy.config import AUTH_ENDPOINT
from factionpy.logger import log


def validate_authorization_header(header_value):
    log(f"got header {header_value}")
    success = False
    result = None
    try:
        log(f"got header {header_value}")
        headers = {"Authorization": header_value}
        url = f"{AUTH_ENDPOINT}/verify/"
        log(f"using url: {url}")
        r = requests.get(url, headers=headers).json()
        log(f"got response {r}")
        if r['success'] == "True":
            success = True
            result = r
    except Exception as e:
        result = e
    rsp = {"success": success, "result": result}
    log(f"returning: {rsp}")
    return rsp
