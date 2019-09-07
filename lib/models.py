from typing import List, Sized, Mapping, Optional, Dict
from dataclasses import dataclass, field
from enum import Enum

from lib.translations import Translation
from lib.utils import filter_dict


@dataclass
class VenueLocation:
    address: Optional[str]
    cross_street: Optional[str]
    ll: str
    postal_code: Optional[str]
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
    created_at: int
    short_url: str


@dataclass
class VenueEditRequest:
    name: Optional[str] = field(default=None)
    translations: List[Translation] = field(default_factory=list)
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
    wifi: Optional[bool] = field(default=None)
    credit_cards: Optional[bool] = field(default=None)
    primary_category_id: Optional[str] = field(default=None)
    remove_category_ids: List[str] = field(default_factory=list)

    def merge(self, other: "VenueEditRequest") -> "VenueEditRequest":
        return VenueEditRequest(
            name=other.name or self.name,
            translations=other.translations or self.translations,
            address=other.address or self.address,
            cross_street=other.cross_street or self.cross_street,
            city=other.city or self.city,
            zip=other.zip or self.zip,
            phone=other.phone or self.phone,
            twitter=other.twitter or self.twitter,
            instagram=other.instagram or self.instagram,
            facebook=other.facebook or self.facebook,
            url=other.url or self.url,
            hours=other.hours or self.hours,
            menu_url=other.menu_url or self.menu_url,
            parent_id=other.parent_id or self.parent_id,
            chain_id=other.chain_id or self.chain_id,
            primary_category_id=other.primary_category_id or self.primary_category_id,
            remove_category_ids=other.remove_category_ids or self.remove_category_ids,
        )

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
            'wifi': "yes" if self.wifi else ("no" if self.wifi == False else None),
            'creditCards': "yes" if self.credit_cards else ("no" if self.credit_cards == False else None),
            'hours': self.hours,
            'menuUrl': self.menu_url,
            'parentId': self.parent_id,
            'primaryVenueChainId': self.chain_id,
            'primaryCategoryId': self.primary_category_id,
            'removeCategoryIds': ",".join(self.remove_category_ids),
        }
        for translation in self.translations:
            result[f"name:{translation.code}"] = translation.value
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

    def __hash__(self):
        return self.id.__hash__()


@dataclass
class UserDetails:
    id: str
    first_name: str
    last_name: str

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class VenueFlag(Enum):
    MISLOCATED = "mislocated"
    CLOSED = "closed"
    DUPLICATE = "duplicate"
    INAPPROPRIATE = "inappropriate"
    DOES_NOT_EXIST = "doesnt_exist"
    PRIVATE = "private"
    EVENT_OVER = "event_over"
