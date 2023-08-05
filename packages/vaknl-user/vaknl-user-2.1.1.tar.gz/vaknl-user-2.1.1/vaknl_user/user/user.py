"""User dataclass.

User class created from firestore website clickstream data.

Created: 2020-03-0? (Merijn)
Updated: 2020-08-06 (Merijn, DAT-1583)
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field
from typing import Dict, List
from dacite import from_dict
import logging


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
from vaknl_user.user import utils
from vaknl_user.user.statistics import Statistics
from vaknl_user.user.email import Email
from vaknl_user import event
from vaknl_NBC import NBC


# ----------------------------------------------------------------------------------------------------------------------
# User dataclass
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class User:
    """User dataclass for `dmp_user`."""
    dmp_user_id: str
    statistics: Statistics = field(default_factory=Statistics)

    def __post_init__(self):
        self.__validate_attribute_types()

    @property
    def email(self) -> Email:
        """Generate email information for user, only if there exist at least one `sfmc_contact_id` in
        `statistics.general.user_identifiers`.

        Return:
            Email instance.
        """
        if self.statistics.general.user_identifiers:
            return Email.from_statistics(dmp_user_id=self.dmp_user_id, statistics=self.statistics)

    def __validate_attribute_types(self):
        """Validate if attributes are are of the correct type."""
        for attr_name, attr_type in self.__annotations__.items():
            if not isinstance(getattr(self, attr_name), attr_type):
                raise ValueError(f'The value given in field `{attr_name}` is of a wrong type.')

    def _add_event(self, evt: event.event.Event, nbc_api: NBC = None):
        """Adds single event from an `Event` object.

        Args:
            evt: `Event` instance.
            nbc_api: NBC API instance, from which Non Bookable Content for an accommodation can be collected.
        """
        self.statistics.add_event(evt, nbc_api)

    def _add_events(self, evts: event.event.Events, nbc_api: NBC = None):
        """Adds multiple events represented as an `Events` object.

        Args:
            evts: `Events` instance that contains a list of `Event` instances.
            nbc_api: NBC API instance, from which Non Bookable Content for an accommodation can be collected.
        """
        self.statistics.add_events(evts, nbc_api)

    def _add_raw_event(self, raw_event: dict, nbc_api: NBC = None):
        """Adds single raw clickstream event.

        Args:
            raw_event: Raw clickstream event.
            nbc_api: NBC API instance, from which Non Bookable Content for an accommodation can be collected.
        """
        evt = event.create_event(raw_event)
        self._add_event(evt, nbc_api)

    def _add_raw_events(self, raw_events: List[Dict], nbc_api: NBC = None):
        """Adds multiple raw clickstream events.

        Args:
            raw_events: List of raw clickstream events.
            nbc_api: NBC API instance, from which Non Bookable Content for an accommodation can be collected.
        """
        evts = event.event.Events()
        evts.add_raw_events(raw_events)
        self._add_events(evts, nbc_api)

    @classmethod
    def _from_dict(cls, data: dict):
        """Create `User` dataclass from a dictionary representation of the dataclass.

        Args:
            data: Dictionary representation of the dataclass.
        """
        return from_dict(data_class=cls, data=data)

    def _to_dict(self) -> dict:
        """Write `User` dataclass to a dictionary representation.

        Return:
            Dictionary representation of the dataclass.
        """
        self.__validate_attribute_types()
        data = {
            'dmp_user_id': self.dmp_user_id,
            'statistics': self.statistics.to_dict(),
        }
        if self.statistics.general.user_identifiers.get('sfmc_contact_id'):
            data['email'] = self.email.to_dict()
        return data

    def update(self, client: utils.firestore.Client, nbc_api: NBC = None):
        """Gets all raw clickstream events that has occurred after the latest event tracked in the `statistics` and
        updates the user with it.

        Args:
            client: Firestore client instance.
            nbc_api: NBC API instance.
        """
        data = utils.import_website_clickstream_events(
            client=client,
            dmp_user_id=self.dmp_user_id,
            timestamp_left_bound=self.statistics.general.activity_last_timestamp  # Okay if None, then all data is used.
        )
        self._add_raw_events(raw_events=data, nbc_api=nbc_api)

    @classmethod
    def from_firestore_clickstream(cls, client: utils.firestore.Client, dmp_user_id: str, nbc_api: NBC = None):
        """Creates user with all raw clickstream events available.

        Args:
            client: Firestore client instance.
            dmp_user_id: The `dmp_user_id` of the user.
            nbc_api: NBC API instance.
        """
        usr = cls(dmp_user_id=dmp_user_id)
        usr.update(client=client, nbc_api=nbc_api)
        return usr

    @classmethod
    def from_firestore_user(cls, client: utils.firestore.Client, dmp_user_id: str):
        """Create `User` dataclass from a Firestore user.

        Args:
            client: Firestore client instance.
            dmp_user_id: The `dmp_user_id` of the user.
        """
        data = utils.read_from_firestore_user(client=client, dmp_user_id=dmp_user_id)
        if data:
            data['dmp_user_id'] = dmp_user_id
            return cls._from_dict(data)
        else:
            return cls(dmp_user_id=dmp_user_id)

    def to_firestore(self, client: utils.firestore.Client):
        """Exports user to Firestore user collection, overwriting it.

        Args:
            client: Firestore client instance.
        """
        if self.statistics.general.event_cnt > 0:
            data = self._to_dict()
            data.pop('dmp_user_id')
            utils.write_to_firestore_user(client=client, dmp_user_id=self.dmp_user_id, data=data)
        else:
            logging.getLogger('user.user.User.to_firestore').warning(
                f'The user (`dmp_user_id={self.dmp_user_id}`) has not been written to Firestore, because it has no '
                f'events.'
            )
