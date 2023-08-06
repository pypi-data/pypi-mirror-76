from functools import wraps
from flask import request
from factionpy.logger import log
from factionpy.services import validate_authorization_header

standard_read = [
    'admin',
    'operator',
    'read-only'
]

standard_write = [
    'admin',
    'operator'
]


def authorized_groups(groups: list):
    print(f"factionpy:authorized_groups - Called..")
    """
    This decorator takes a list of group names that are authorized to perform the function. The following shortcuts are
    available:
        * "standard_read" covers super-user, user, and read-only roles
        * "standard_write" covers super-user and user roles
        * "all" allows any authenticated user to perform the function
    These shortcuts can be combined with other group names, for example: @authorized_groups("standard_read", "transports")
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            print(f"factionpy:authorized_groups - Checking if authenticated..")
            user_data = None
            authorized = False
            try:
                auth_header = request.headers.get("Authorization", None)
                print(f"factionpy:authorized_groups - got auth_header: {auth_header}")
                if auth_header:
                    verified_header = validate_authorization_header(auth_header)
                    print(f"factionpy:authorized_groups - got verfied_header: {verified_header}")
                    if verified_header["success"] == "True":
                        user_data = verified_header["results"]
            except Exception as e:
                print(f"factionpy:authorized_groups - Could not verify Authorization header. Error: {e}")
                return False

            if user_data:
                try:
                    print(f"factionpy:authorized_groups - got user_data: {user_data}")
                    # Replace meta group names with contents of meta group
                    if 'standard_read' in groups:
                        groups.remove('standard_read')
                        groups.extend(standard_read)

                    if 'standard_write' in groups:
                        groups.remove('standard_write')
                        groups.extend(standard_write)

                    if 'all' in groups:
                        authorized = True

                    # Iterate through valid groups, checking if the user is in there.
                    if user_data['role'] in groups:
                        print(f"factionpy:authorized_groups - user authorized")
                        authorized = True
                except Exception as e:
                    print(f"factionpy:authorized_groups - Could not verify user_data. Error: {e}")
                    return False

            if authorized:
                print(f"factionpy:authorized_groups - returning function")
                return f(*args, **kwargs)
            else:
                print(f"factionpy:authorized_groups - User {user_data['username']} is not in the following groups: {groups}")
                return False
        return wrapped
    return decorator
