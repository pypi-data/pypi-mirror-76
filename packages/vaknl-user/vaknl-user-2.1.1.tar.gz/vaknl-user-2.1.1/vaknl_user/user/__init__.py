"""User module.

Imports all child modules and includes a `update_firestore_user()` function.

Created: 2020-07-?? (Merijn, DAT-1583)
Updated: 2020-08-06 (Merijn, DAT-1583)
"""


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
from vaknl_NBC import NBC


# ----------------------------------------------------------------------------------------------------------------------
# Import child modules
# ----------------------------------------------------------------------------------------------------------------------
from . import utils
from . import statistics
from . import user
from . import email


# ----------------------------------------------------------------------------------------------------------------------
# Import internal modules
# ----------------------------------------------------------------------------------------------------------------------
def update_firestore_user(client: utils.firestore.Client, dmp_user_id: str, nbc_api: NBC = None):
    """Function to update (or create when not existing yet) Firestore user. Overwrites current state in Firestore.

    Args:
        client: Firestore client instance.
        dmp_user_id: The `dmp_user_id` of the user.
        nbc_api: NBC API instance, from which Non Bookable Content for an accommodation can be collected.
    """
    usr = user.User.from_firestore_user(client=client, dmp_user_id=dmp_user_id)
    usr.update(client=client, nbc_api=nbc_api)
    usr.to_firestore(client=client)
