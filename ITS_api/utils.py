from users.serializers import UserSerializer


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

def my_jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        'user_id': user.pk,
        'email': user.email,
        'is_superuser': user.is_superuser
       # 'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        #'orig_iat': timegm(
        #    datetime.utcnow().utctimetuple()
       # )
    }

def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.

    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data

    }