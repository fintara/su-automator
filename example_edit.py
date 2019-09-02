from lib.api import FoursquareApi, get_token
from lib.models import *
from lib.utils import convert_hours

# Here we load a bunch of venue ids and we submit new information

api = FoursquareApi(get_token())
user = api.get_user()
print(f"Hello, {user.full_name()}!")

with open("ids.txt") as file:
    ids = [line.strip() for line in file]

for venue_id in ids:
    request = VenueEditRequest(
        name="North Fish",
        chain_id="5d603c258bc5be00065be9a2",
        hours=convert_hours({'Monday-Friday': "09:00-18:30"})
    )
    api.propose_edit(venue_id, request)
