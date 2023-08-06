from flask import request
from factionpy.logger import log
from functools import wraps
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


class authorized_groups(object):
    def __init__(self, groups: list):
        self.groups = groups

    def __call__(self, func):

        @wraps(func)
        def callable(*args, **kwargs):
            print(f"factionpy:authorized_groups - Checking if authenticated..")
            user_data = None
            authorized = False
            groups = self.groups
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
                    else:
                        print(f"factionpy:authorized_groups - User {user_data['username']} is not in the following "
                              f"groups: {groups}")
                except Exception as e:
                    print(f"factionpy:authorized_groups - Could not verify user_data. Error: {e}")

            if authorized:
                print(f"factionpy:authorized_groups - returning function")
                return func(*args, **kwargs)
        return callable
