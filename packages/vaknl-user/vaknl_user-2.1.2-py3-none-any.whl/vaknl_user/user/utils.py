"""Utility functions/classes for `vaknl_user/user`.

Created: 2020-07-10 (Merijn, DAT-1583)
Updated: 2020-08-06 (Merijn, DAT-1583)
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import libraries
# ----------------------------------------------------------------------------------------------------------------------
import logging
from typing import List, Dict, Union
import google.auth
from google.cloud import firestore


# ----------------------------------------------------------------------------------------------------------------------
# Constant variables
# ----------------------------------------------------------------------------------------------------------------------
CLICKSTREAM_FIRESTORE_COLLECTION = u'in_website_clickstream'
USER_FIRESTORE_COLLECTION = u'dmp_user'


# ----------------------------------------------------------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------------------------------------------------------
def create_firestore_client(project_id: str = None) -> firestore.Client:
    """Sets up Firestore client.

    Args:
        project_id: GCP 'project id'.

    Return:
        A Firestore Client instance.
    """
    if not project_id:
        _, project_id = google.auth.default()
    return firestore.Client(project=project_id)

    # DEPRECATED: should be put back in place when using AppEngine, for efficiency reasons:
    # import firebase_admin
    # from firebase_admin import credentials, firestore
    # cred = credentials.ApplicationDefault()
    # firebase_admin.initialize_app(cred, {'projectId': project_id})
    # return firestore.client()


def import_website_clickstream_events(client: firestore.Client, dmp_user_id: str, timestamp_left_bound: int = None) \
        -> List[Dict]:
    """Import raw website clickstream events from Firestore.

    Args:
        client: Firestore client instance.
        dmp_user_id: The `dmp_user_id` of the user.
        timestamp_left_bound: Unix timestamp for which all events need to have a greater timestamp to be included. If
            left `None`, all clickstream event data is used.

    Return:
        A list of raw website clickstream events.
    """
    # Get `dmp_session_id`s stored in Firestore for given `dmp_user_id`.
    doc_ref = client.collection(CLICKSTREAM_FIRESTORE_COLLECTION).document(dmp_user_id) \
        .collection(u'sessions').stream()
    sessions = [doc.id for doc in doc_ref]

    # Get all events.
    event_list = []
    for session in sessions:
        event_list += client.collection(CLICKSTREAM_FIRESTORE_COLLECTION).document(dmp_user_id) \
            .collection(u'sessions').document(session) \
            .collection(u'events').document(u'event_list').get().to_dict()['event_list']

    if event_list:
        # Only take events greater than the `timestamp_left_bound`.
        if timestamp_left_bound is not None:
            event_list = [item for item in event_list if item.get('timestamp', 0) > timestamp_left_bound]
    else:
        logging.getLogger('user.utils.import_website_clickstream_events').warning(
            f'No events were found for `dmp_user_id={dmp_user_id}` in the `{CLICKSTREAM_FIRESTORE_COLLECTION}` '
            f'Firestore collection.'
        )
    return event_list


def read_from_firestore_user(client: firestore.Client, dmp_user_id: str) -> Dict:
    """Import a user from the Firestore user collection.

    Args:
        client: Firestore client instance.
        dmp_user_id: The `dmp_user_id` of the user.

    Return:
        Dictionary of Firestore user.
    """
    data = client.collection(USER_FIRESTORE_COLLECTION).document(dmp_user_id).get().to_dict()
    if data:
        return data
    else:
        logging.getLogger('user.utils.read_from_firestore_user').warning(
            f'No data for `dmp_user_id={dmp_user_id}` was found in the `{USER_FIRESTORE_COLLECTION}` Firestore '
            f'collection.'
        )


def write_to_firestore_user(client, dmp_user_id: str, data: dict):
    """(Over)Writes a user in the `dmp_user` collection in Firestore. Note: by using `set()` it overwrites the
    whole document. The method `update()` can only be used if the collection already exists.

    Args:
        client: Firestore client instance.
        dmp_user_id: The `dmp_user_id` of the user.
        data: Data to be written to Firestore in the form of a User dictionary.
    """
    doc_ref = client.collection(USER_FIRESTORE_COLLECTION).document(dmp_user_id)
    doc_ref.set(data)


def remove_firestore_user(client, dmp_user_id: str):
    """Deletes a Firestore document in the `dmp_user` collection with given `dmp_user_id`.

    Args:
        client: Firestore client instance.
        dmp_user_id: The `dmp_user_id` of the user.
    """
    doc_ref = client.collection(USER_FIRESTORE_COLLECTION).document(dmp_user_id)
    doc_ref.delete()
