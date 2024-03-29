SU Automator
=======================

Makes superuser's life easier

## Requirements
* Python 3.7
* Pipenv
* App registered in Foursquare Developers (should have `http://localhost` in App Settings > Redirect URL)
* Code editor (highly recommend PyCharm)

## How to use
1. Clone this repository.
2. Run `pipenv install`
3. Create a file `api.txt` with API credentials:
    ```
    client_id=ABCDEF
    client_secret=GHIJKL
    ```
4. Use the api:
    ```python
    from lib.api import FoursquareApi, get_token
    from lib.models import *

    api = FoursquareApi(get_token())
    user = api.get_user()
    print(f"Hello, {user.full_name()}!")
    ```
   Upon first run you will be asked to open the provided URL where you
   will allow access for your app.
   Then you will be redirected to http://localhost/?code=XYZ#_=_.
   Copy the code (between `=` and `#`), paste it in the console and you are in!
   If you want to "log out", delete the created `token.txt` file.
   
   You can check `example_*.py` for examples.

The rest can be checked in [Foursquare Developer docs](https://developer.foursquare.com/docs/api/endpoints).

## Available methods
* `get_user(id: str = "self)` - get user's details
* `search_venues(query: str, ll: str, radius: int, category_ids=None)` - search for venues near location
* `search_venues_multiq(query: List[str], ...)` - same as previous with multiple queries
* `get_venue(id: str)` - get venue's details
* `add_venue(name: str, ll: str, category_id: str)` - submit new venue with minimally required data
* `add_venue_with_data(name: str, ll: str, category_id: str, data: VenueEditRequest)` - same as previous with additional data
* `propose_edit(id: str, venue: VenueEditRequest)` - submit changes for venue
* `flag_venue(id: str, flag: VenueFlag)` - flags a venue with one of the possible problems