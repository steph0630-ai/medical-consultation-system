import json
import secrets
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE_URL = "http://127.0.0.1:8001/api/v1"


def post(path: str, payload: dict) -> tuple[int, dict]:
    request = Request(
        BASE_URL + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        return error.code, json.load(error)


def get(path: str, token: str) -> tuple[int, dict]:
    request = Request(BASE_URL + path, headers={"Authorization": f"Bearer {token}"})
    with urlopen(request) as response:
        return response.status, json.load(response)


email = f"check-{secrets.token_hex(4)}@example.com"
credentials = {"email": email, "password": "password1"}
registration = {**credentials, "first_name": "San", "last_name": "Zhang"}

assert post("/auth/register", registration)[0] == 200
assert post("/auth/register", registration)[0] == 400
status, login = post("/auth/login", credentials)
assert status == 200 and login["data"]["access_token"]
status, profile = get("/users/me", login["data"]["access_token"])
assert status == 200 and profile["data"]["email"] == email
assert post("/auth/login", {**credentials, "password": "wrong"})[0] == 400
print("auth check passed")
