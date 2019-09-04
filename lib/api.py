import requests
import os.path
from typing import List, Sized, Mapping, Optional
from lib.models import *
from lib.utils import filter_mapping


class FoursquareApi:
    __version = "20190815"
    __base = "https://api.foursquare.com/v2/"

    def __init__(self, token):
        self.__token = token

    """https://developer.foursquare.com/docs/api/users/details"""
    def get_user(self, id: str = "self") -> UserDetails:
        res = self.__get(f"users/{id}").json()['response']['user']
        return UserDetails(
            id=res['id'],
            first_name=res['firstName'],
            last_name=res['lastName']
        )

    """https://developer.foursquare.com/docs/api/venues/search"""
    def search_venues(self, name: str, ll: str, radius: int, category_ids=None) -> List[VenueSimpleSearch]:
        if category_ids is None:
            category_ids = []
        payload = {
            'll': ll,
            'intent': "browse",
            'radius': str(radius),
            'query': name,
            'categoryId': ",".join(category_ids),
        }
        res = self.__get("venues/search", payload)
        res.raise_for_status()
        res = res.json()['response']['venues']
        result = [VenueSimpleSearch(id=row['id'], name=row['name'], distance=row['location']['distance']) for row in res]
        result.sort(key=lambda x: x.distance)
        return result

    def search_venues_multiq(self, names: List[str], ll: str, radius: int, category_ids=None) -> List[VenueSimpleSearch]:
        if category_ids is None:
            category_ids = []
        results = [self.search_venues(name, ll, radius, category_ids) for name in names]
        result = list(set([x for b in results for x in b]))
        result.sort(key=lambda x: x.distance)
        return result

    """https://developer.foursquare.com/docs/api/venues/details"""
    def get_venue(self, venue_id: str) -> Venue:
        res = self.__get("venues/{}".format(venue_id))
        res.raise_for_status()
        res = res.json()['response']['venue']
        location = res['location']
        return Venue(
            id=res['id'],
            name=res['name'],
            location=VenueLocation(
                address=location.get('address'),
                cross_street=location.get('crossStreet'),
                ll="{},{}".format(location['lat'], location['lng']),
                postal_code=location.get('postalCode'),
                city=location.get('city'),
                country=location.get('country'),
            ),
            categories=[VenueCategory(id=c['id'], name=c['name']) for c in res['categories']],
            created_at=res['createdAt'],
            short_url=res['shortUrl']
        )

    """https://developer.foursquare.com/docs/api/venues/add"""
    def add_venue(self, name: str, ll: str, category_id: str) -> Optional[VenueSimple]:
        data = {
            'name': name,
            'll': ll,
            'primaryCategoryId': category_id,
        }
        res = self.__post("venues/add", data)
        if res.status_code == 409:
            res = res.json()['response']
            print("Found possible duplicates:")
            for dup in res['candidateDuplicateVenues']:
                addr=dup['location'].get('formattedAddress') or ["(No address)"]
                addr=", ".join(addr)
                print(f"+ https://foursquare.com/v/{dup['id']} :: {dup['name']} ({dup['location']['distance']} m) :: {addr}")
            choice = input("Force submit [y/n]: ").strip()
            if choice != 'y':
                return None
            repeat = {
                'ignoreDuplicates': "true",
                'ignoreDuplicatesKey': res['ignoreDuplicatesKey']
            }
            data = {**data, **repeat}
            res = self.__post("venues/add", data)
        res.raise_for_status()
        res = res.json()['response']['venue']
        return VenueSimple(id=res['id'], name=res['name'])

    """https://developer.foursquare.com/docs/api/venues/proposededit"""
    def propose_edit(self, venue_id: str, changes: VenueEditRequest):
        res = self.__post("venues/{}/proposeedit".format(venue_id), changes.as_dict())
        return res

    def add_venue_with_data(self, name: str, ll: str, category_id: str, data: VenueEditRequest) -> Optional[VenueSimple]:
        added = self.add_venue(name, ll, category_id)
        if added is None:
            return None
        try:
            self.propose_edit(added.id, data)
            return added
        except Exception as e:
            print("Added https://foursquare.com/v/{}, but failed to edit".format(added.id))
            raise e

    """https://developer.foursquare.com/docs/api/venues/flag"""
    def flag_venue(self, venue_id: str, flag: VenueFlag):
        res = self.__post("venues/{}/flag".format(venue_id), {'problem': flag.value})
        return res

    """Send GET request"""
    def __get(self, endpoint: str, payload: Mapping[str, Sized] = None) -> requests.Response:
        if payload is None:
            payload = dict()

        auth = self.__get_auth()
        non_empty = filter_mapping(payload, lambda x: len(x[1]) > 0)
        params = {**auth, **non_empty}
        res = requests.get("{}{}".format(self.__base, endpoint), params=params)
        self.__log_quota(endpoint, res)
        return res

    """Send POST request"""
    def __post(self, endpoint: str, payload: Mapping[str, Sized]) -> requests.Response:
        auth = self.__get_auth()
        non_empty = filter_mapping(payload, lambda x: len(x[1]) > 0)
        params = {**auth, **non_empty}
        res = requests.post("{}{}".format(self.__base, endpoint), params=params)
        self.__log_quota(endpoint, res)
        if str(res.status_code)[0] != '2':
            print(res.json())
        return res

    def __get_auth(self):
        return {
            'oauth_token': self.__token,
            'v': self.__version
        }

    @staticmethod
    def __log_quota(tag: str, response: requests.Response):
        remaining = response.headers.get('X-RateLimit-Remaining')
        limit = response.headers.get('X-RateLimit-Limit')
        # print("[{}] RateLimit: {}/{}".format(tag, remaining, limit))


def get_token() -> str:
    redirect_uri = "http://localhost"
    auth_url_template = "https://foursquare.com/oauth2/authenticate?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
    token_url_template = "https://foursquare.com/oauth2/access_token?client_id={client_id}&client_secret={client_secret}&grant_type=authorization_code&redirect_uri={redirect_uri}&code={code}"

    token_filename = "token.txt"
    if not os.path.exists(token_filename):
        creds = {}
        with open("api.txt") as file:
            for line in file:
                name, value = line.partition("=")[::2]
                creds[name.strip()] = value.strip()
        auth_url = auth_url_template.format(client_id=creds['client_id'], redirect_uri=redirect_uri)
        print("Open: {}".format(auth_url))
        code = input("Code: ")
        token_url = token_url_template.format(
            client_id=creds['client_id'],
            client_secret=creds['client_secret'],
            redirect_uri=redirect_uri,
            code=code
        )
        res = requests.get(token_url).json()
        with open(token_filename, 'w') as out:
            out.write(res['access_token'])

    token = ""
    with open(token_filename) as file:
        token = file.readline()

    return token
