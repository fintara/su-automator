from lib.api import FoursquareApi, get_token
from lib.models import *
from lib.utils import convert_hours
import json

# In this example we load a bunch of locations from a json file,
# and we search for already created venues near these points.
# If there's none, we create one.

api = FoursquareApi(get_token())
user = api.get_user()
print(f"Hello, {user.full_name()}!")


with open("technomarket.json") as file:
    data = json.load(file)

for row in data:
    print(f"Working on Technomarket @ {row['street']}, {row['city']}")
    should_search_parent = len(row['inside']) > 0
    hours = convert_hours(row['hours'])

    venues = api.search_venues_multiq(["technomarket", "техномаркет"], row['ll'], 3000)

    # not everything can be submitted when new venue is created
    more_request = VenueEditRequest(
        address=row['street'],
        cross_street=row['cross_street'],
        city=row['city'],
        translations={
            'bg': "Техномаркет",
            'en': "Technomarket"
        },
    )

    print("Found {} venues".format(len(venues)))
    for v in venues:
        print("+ https://foursquare.com/v/{} :: {} ({} m)".format(v.id, v.name, v.distance))

    if len(venues) == 0:
        added = api.add_venue("Technomarket", row['ll'], "4bf58dd8d48988d122951735")
        print(f"Added https://foursquare.com/v/{added.id} :: {added.name}")
        api.propose_edit(added.id, more_request)
        print(f"Additionally edited https://foursquare.com/v/{added.id}")

    input("Continue?")
    print("")