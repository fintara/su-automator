from abc import ABC, abstractmethod, ABCMeta
from typing import List, Sized, Mapping, Optional, Dict
from dataclasses import dataclass, field
from enum import Enum

from lib.utils import filter_dict


@dataclass
class VenueLocation:
    address: Optional[str]
    crossStreet: Optional[str]
    ll: str
    postalCode: Optional[str]
    city: Optional[str]
    country: Optional[str]


@dataclass
class VenueCategory:
    id: str
    name: str

    def __hash__(self):
        return self.id.__hash__()


@dataclass
class Venue:
    id: str
    name: str
    location: VenueLocation
    categories: List[VenueCategory]
    createdAt: int
    shortUrl: str


@dataclass
class VenueAddRequest:
    name: str
    ll: str
    primary_category_id: str
    address: str = field(default="")
    cross_street: str = field(default="")
    city: str = field(default="")
    zip: str = field(default="")
    phone: str = field(default="")
    url: str = field(default="")
    parent_id: str = field(default="")
    chain_ids: List[str] = field(default_factory=list)
    all_category_ids: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict:
        return {
            'name': self.name,
            'll': self.ll,
            'primaryCategoryId': self.primary_category_id,
            'address': self.address,
            'crossStreet': self.cross_street,
            'city': self.city,
            'zip': self.zip,
            'phone': self.phone,
            'url': self.url,
            'parentId': self.parent_id,
            'chainIds': self.chain_ids,
            'allCategoryIds': self.all_category_ids,
        }


@dataclass
class VenueEditRequest:
    name: Optional[str] = field(default=None)
    translations: Dict = field(default_factory=dict)
    address: Optional[str] = field(default=None)
    cross_street: Optional[str] = field(default=None)
    city: Optional[str] = field(default=None)
    zip: Optional[str] = field(default=None)
    phone: Optional[str] = field(default=None)
    twitter: Optional[str] = field(default=None)
    instagram: Optional[str] = field(default=None)
    facebook: Optional[str] = field(default=None)
    url: Optional[str] = field(default=None)
    hours: Optional[str] = field(default=None)
    menu_url: Optional[str] = field(default=None)
    parent_id: Optional[str] = field(default=None)
    chain_id: Optional[str] = field(default=None)

    def as_dict(self) -> Dict:
        result = {
            'name': self.name,
            'address': self.address,
            'crossStreet': self.cross_street,
            'city': self.city,
            'zip': self.zip,
            'phone': self.phone,
            'twitter': self.twitter,
            'instagram': self.instagram,
            'facebookUrl': self.facebook,
            'url': self.url,
            'menuUrl': self.menu_url,
            'parentId': self.parent_id,
            'primaryVenueChainId': self.chain_id,
        }
        for key, value in self.translations.items():
            result[f"name:{key}"] = value
        return filter_dict(result, lambda x: x[1] is not None)


@dataclass
class VenueSimple:
    id: str
    name: str

    def __hash__(self):
        return self.id.__hash__()


@dataclass
class VenueSimpleSearch(VenueSimple):
    distance: int


@dataclass
class UserDetails:
    id: str
    firstName: str
    lastName: str

    def full_name(self) -> str:
        return f"{self.firstName} {self.lastName}"


class VenueFlag(Enum):
    MISLOCATED = "mislocated"
    CLOSED = "closed"
    DUPLICATE = "duplicate"
    INAPPROPRIATE = "inappropriate"
    DOES_NOT_EXIST = "doesnt_exist"
    PRIVATE = "private"
    EVENT_OVER = "event_over"
