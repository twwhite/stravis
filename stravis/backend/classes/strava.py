import json, requests, logging
from dotenv import dotenv_values
from uuid import uuid4
from pathlib import Path

logger = logging.getLogger(__name__)

class Strava:

    def __init__(self, api_access_token, api_refresh_token, api_client_id, api_client_secret):

        self.id = uuid4()
        self.api_access_token   = api_access_token
        self.api_refresh_token  = api_refresh_token
        self.api_client_id      = api_client_id
        self.api_client_secret  = api_client_secret

    def refresh_access_token(self):
        
        data = {
            "client_id": self.api_client_id,
            "client_secret": self.api_client_secret,
            "scope": "read,activity:read_all",
            "grant_type": "authorization_code",
        }

        url = 'https://www.strava.com/api/v3/oauth/token'
        payload = json.dumps(data)
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.post(url, data=payload, headers=headers)
        logger.info(r.json())

        try:
            self.api_access_token = r.json()['access_token']
        except KeyError:
            logger.error(r.json())
        return r

    def get_activities(self):
        url = f'https://www.strava.com/api/v3/athlete/activities'
        headers = {'Authorization': 'Bearer ' + self.api_access_token}
        print(headers)
        r = requests.get(url, headers=headers)
        print(r.json())
        logger.info(r)

        with open(f'{get_project_root()}/data/activities.json', 'w', encoding='utf-8') as f:
            json.dump(r.json(), f, ensure_ascii=False, indent=4)

        return r

    def load_activities_from_file(self):
        with open(f'{get_project_root()}/data/activities.json', 'r', encoding='utf-8') as f:
            self.activities = json.load(f)
            return self.activities

def get_project_root() -> Path:
    print(Path(__file__).parent.parent.parent)
    return Path(__file__).parent.parent.parent


if __name__ == "__main__":

    env = dotenv_values(".env")
    s = Strava(env['STRAVA_ACCESS_TOKEN'], env['STRAVA_REFRESH_TOKEN'], env['STRAVA_CLIENT_ID'], env['STRAVA_CLIENT_SECRET'])
