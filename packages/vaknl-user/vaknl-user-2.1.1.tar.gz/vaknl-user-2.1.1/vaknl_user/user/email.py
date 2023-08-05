"""Email dataclass.

`Email` dataclass created from a `Statistics` instance.

Created: 2020-07-29 (Merijn, DAT-1583)
Updated: 2020-08-06 (Merijn, DAT-1583)
"""


# TODO: Clean up unused code.


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field, InitVar, asdict
from typing import Dict, Any


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
from vaknl_user import user


# ----------------------------------------------------------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------------------------------------------------------
def dict_max_value_key(dct: Dict[Any, int]) -> Any:
    """Get key with highest value from counting dictionary.

    Args:
        dct: Counter dictionary.

    Return:
        The key of the dictionary where the value is the highest.
    """
    if dct:
        return max(dct, key=dct.get)
    else:
        return None


# ----------------------------------------------------------------------------------------------------------------------
# Email dataclass
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class Email:
    """Email dataclass."""
    # id: int
    Contactid: str  # has none, DATA IN GBQ, primary key in SFMC
    # TODO: `Contactid` often ends up being the email address, because an email address is provided in the `mcparam`
    #  field in the raw events.
    # email: str
    dmp_user_id: str
    google_id: str = 'unknown'
    country1: str = 'unknown'
    country2: str = 'unknown'
    country3: str = 'unknown'
    region1: str = 'unknown'
    region2: str = 'unknown'
    region3: str = 'unknown'
    sessions: int = None  # Nearly everywhere 1
    pageviews: int = None  # Nearly everywhere 1
    productEngagement: int = None  # Nearly everywhere 1
    depdateSelections: int = None  # Nearly everywhere 1
    FavouriteTheme: str = 'zonvakantie'  # Or default is None, but does not appear
    adultsonly: float = None
    allinclusive: float = None
    aquapark: float = None
    kindvriendelijk: float = None
    kleinschalig: float = None
    lastminute: float = None
    luxe: float = None
    stedentrip: float = None
    strandvakantie: float = None
    verreReizen: float = None
    wellness: float = None
    zonvakantie: float = None
    departureAirportAmsterdamNL: int = None
    departureAirportKeulenBonnDE: int = None
    departureAirportEindhovenNL: int = None
    departureAirportRotterdamNL: int = None
    departureAirportBrusselBE: int = None
    departureAirportDusseldorfDE: int = None
    departureAirportGroningenNL: int = None
    departureAirportMaastrichtNL: int = None
    active: int = 0  # only one non-zero
    active_plus: int = 0  # only one non-zero
    inmarket: int = 0  # only one non-zero
    booked: int = 0  # default everywhere
    bucket: str = 'visitor'  # only one non-visitor
    last_active: str = None  # DATE, filled only once
    favDayOfWeek: int = None  # 1-7, nearly empty
    favHour: int = None  # 0-23, nearly empty
    favPeriod: str = None  # DATE, filled only once
    lastMinuteDefined: bool = None  # filled only once
    city1: str = 'unknown'
    city2: str = 'unknown'
    city3: str = 'unknown'
    lastViewedAcco: int = None  # nearly empty
    recommendation_1: int = None
    recommendation_2: int = None
    recommendation_3: int = None
    recommendation_4: int = None
    searchpage_url: str = None
    most_engaged_hotel: int = None  # nearly empty
    last_booked_hotel: int = None
        
    @classmethod
    def from_statistics(cls, dmp_user_id: str, statistics: user.statistics.Statistics):
        """Create `Email` instance from a `Statistics` instance.

        Args:
            dmp_user_id: The `dmp_user_id` of the user.
            statistics: A `Statistics` instance.
        """
        contact_id = statistics.general.user_identifiers.get('sfmc_contact_id', [])[0]
        eml = cls(dmp_user_id=dmp_user_id, Contactid=contact_id)

        eml.google_id = statistics.general.user_identifiers.get('google_id', [])[0]

        # Countries.
        countries = statistics.product.country_name.frequency
        if countries:
            n = len(countries)
            countries = sorted(countries, key=countries.get, reverse=True)[:3]
            eml.country1 = countries[0]
            if n > 1:
                eml.country2 = countries[1]
                if n > 2:
                    eml.country3 = countries[2]

        # Regions.
        regions = statistics.product.region_name.frequency
        if regions:
            n = len(regions)
            regions = sorted(regions, key=regions.get, reverse=True)[:3]
            eml.region1 = regions[0]
            if n > 1:
                eml.region2 = regions[1]
                if n > 2:
                    eml.region3 = regions[2]

        # Cities.
        cities = statistics.product.city_name.frequency
        if cities:
            n = len(cities)
            cities = sorted(cities, key=cities.get, reverse=True)[:3]
            eml.city1 = cities[0]
            if n > 1:
                eml.city2 = cities[1]
                if n > 2:
                    eml.city3 = cities[2]

        eml.sessions = statistics.session.count
        eml.pageviews = statistics.general.pageview_cnt
        # eml.productEngagement =
        eml.depdateSelections = min(1, statistics.search.search_query.departure_date.count + statistics.product.filter_departure_date_cnt)

        # NOTE: the themes are taken from the product pages, but there are also similar data on search filter themes.
        eml.FavouriteTheme = dict_max_value_key(statistics.product.theme.frequency)
        theme_count = sum(statistics.product.theme.frequency.values())
        themes_percentage = {key: round(100 * value / theme_count, 2) for key, value in statistics.product.theme.frequency.items()}
        eml.adultsonly = themes_percentage.get('theme_adult_only', 0.0)
        eml.allinclusive = themes_percentage.get('theme_all_inclusive', 0.0)
        eml.aquapark = themes_percentage.get('theme_aqua_park', 0.0)
        eml.kindvriendelijk = themes_percentage.get('theme_child_friendly', 0.0)
        eml.kleinschalig = themes_percentage.get('theme_boutique', 0.0)
        # eml.lastminute = themes_percentage.get('', 0.0)
        eml.luxe = themes_percentage.get('theme_luxe', 0.0)
        eml.stedentrip = themes_percentage.get('theme_city_trip', 0.0)
        # eml.strandvakantie = themes_percentage.get('', 0.0)
        eml.verreReizen = themes_percentage.get('theme_distant_destination', 0.0)
        eml.wellness = themes_percentage.get('theme_wellness', 0.0)
        eml.zonvakantie = themes_percentage.get('theme_sun_holiday', 0.0)
        # NOTE: 'theme_budget' is also measured
        departure_airports = statistics.search.search_query.departure_airports.frequency
        eml.departureAirportAmsterdamNL = 1 if departure_airports.get('AMS') else 0
        eml.departureAirportKeulenBonnDE = 1 if departure_airports.get('CGN') else 0
        eml.departureAirportEindhovenNL = 1 if departure_airports.get('EIN') else 0
        eml.departureAirportRotterdamNL = 1 if departure_airports.get('RTM') else 0
        eml.departureAirportBrusselBE = 1 if departure_airports.get('BRU') else 0
        eml.departureAirportDusseldorfDE = 1 if departure_airports.get('DUS') else 0
        eml.departureAirportGroningenNL = 1 if departure_airports.get('GRQ') else 0
        eml.departureAirportMaastrichtNL = 1 if departure_airports.get('MST') else 0
        funnel_step = statistics.general.funnel_step
        if funnel_step in ['visitor', 'active', 'active_plus', 'in_market', 'booked']:
            eml.bucket = funnel_step
            if funnel_step != 'visitor':
                eml.active = 1
                if funnel_step != 'active':
                    eml.active_plus = 1
                    if funnel_step != 'active_plus':
                        eml.inmarket = 1
                        if funnel_step != 'in_market':
                            eml.booked = 1
        eml.favDayOfWeek = dict_max_value_key(statistics.session.day_of_week.frequency)
        eml.favHour = dict_max_value_key(statistics.session.hour_of_day.frequency)
        # eml.favPeriod =
        # eml.lastMinuteDefined =
        eml.lastViewedAcco = statistics.product.giata_id.last
        # eml.recommendation_1 =
        # eml.recommendation_2 =
        # eml.recommendation_3 =
        # eml.recommendation_4 =
        # eml.searchpage_url =
        eml.most_engaged_hotel = dict_max_value_key(statistics.product.giata_id.frequency)
        eml.last_booked_hotel = statistics.reservation.booking.last

        return eml

    def to_dict(self) -> dict:
        """Write `Email` dataclass to a dictionary representation.

        Return:
            Dictionary representation of the dataclass.
        """
        return asdict(self)
