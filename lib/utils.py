from types import LambdaType
from typing import Dict, TypeVar, Mapping, Callable, Tuple, Any


A = TypeVar('A')
B = TypeVar('B')


def filter_dict(value: Dict, predicate: Callable[[Tuple[str, Any]], bool]) -> Dict:
    result = dict()
    for (key, value) in value.items():
        if predicate((key, value)):
            result[key] = value
    return result


def filter_mapping(value: Mapping[A, B], predicate: Callable[[Tuple[A, B]], bool]) -> Mapping[A, B]:
    result = dict()
    for (key, value) in value.items():
        if predicate((key, value)):
            result[key] = value
    return result


# Convert days/hours to API format.
# Examples:
# convert_hour("Monday", "09:00-18:30") -> 1,0900,1830
# convert_hour("Monday-Friday", "06:00-15:00") -> 1,0600,1500;2,0600,1500;...;5,0600,1500
#
# For more info: https://developer.foursquare.com/docs/api/venues/proposededit (hours)
def convert_hour(days: str, hours: str) -> str:
    day_to_num = {
        'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5,
        'Saturday': 6, 'Sunday': 7
    }
    hours_formatted = hours.replace(":", "").replace("-", ",").replace(" ", "")
    splitted = [x.strip() for x in days.split("-")]
    if len(splitted) == 1:
        return f"{day_to_num[days]},{hours_formatted}"
    start = day_to_num[splitted[0]]
    end = day_to_num[splitted[1]]
    rng = range(start, end+1)
    return ";".join([f"{x},{hours_formatted}" for x in rng])


# Example:
# convert_hours({
#   'Monday': '06:00-18:00',
#   'Tuesday-Friday': '09:00-15:00'
# })
def convert_hours(value: Dict) -> str:
    return ";".join([convert_hour(x[0], x[1]) for x in value.items()])