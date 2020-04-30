"""
The following functions aim to standardise the JSON responses from this API.
This follows the jsend standard with the exception that a status code will be
sent with the response.
"""

def success(data=None):
    """
    When an API call is successful, the JSend object is used as a simple
    envelope for the results using the data key.

    Required keys:

        status: Should always be set to "success".
        data: Acts as the wrapper for any data returned by the API call. If the
        call returns no data (as in the last example), data should be set to
        null.
    """
    return {
        'status': 'success',
        'data': data
    }

def fail(data=None):
    """
    When an API call is rejected due to invalid data or call conditions, the
    JSend object's data key contains an object explaining what went wrong,
    typically a hash of validation errors.

    Required keys:

        status: Should always be set to "fail".
        data: provides the wrapper for the details of why the request
        failed. If the reasons for failure correspond to POST values, the
        response object's keys SHOULD correspond to those POST values.
    """
    return {
        'status': 'fail',
        'data': data
    }

def error(message, data=None):
    """
    When an API call fails due to an error on the server.

    Required keys:

        status: Should always be set to "error".
        message: A meaningful, end-user-readable (or at the least log-worthy)
        message, explaining what went wrong.

    Optional keys:

        code: A numeric code corresponding to the error, if applicable
        data: A generic container for any other information about the error,
        i.e. the conditions that caused the error, stack traces, etc.

    code is currently not used for any errors.
    """
    return {
        'status': 'error',
        'message': message,
        'data': data
    }


class Message():
    """
    TODO: Make this better, I'm not using this at the moment, not sure if it's
    worth using.
    """
    def __init__(self, resource):
        self.resource = resource.lower()
        self.resource_title = self.resource.capitalize()

    @staticmethod
    def validating_form():
        return {'form': 'Error validating form'}

    @staticmethod
    def exists_email():
        return {'user': 'User already exists with this email'}

    @staticmethod
    def exists_username():
        return {'user': 'User already exists with this username'}

    @staticmethod
    def invalid_whitespace():
        return {'form': 'Spaces are not allowed in password'}

    def does_not_exist(self):
        return {
            self.resource: '{} does not exist'.format(self.resource_title)
        }

    def creating(self):
        return {
            self.resource: 'Error creating {}'.format(self.resource_title)
        }

    def reading(self):
        return {
            self.resource: 'Error reading {}'.format(self.resource_title)
        }

    def updating(self):
        return {
            self.resource: 'Error updating {}'.format(self.resource_title)
        }

    def deleting(self):
        return {
            self.resource: 'Error deleting {}'.format(self.resource_title)
        }

