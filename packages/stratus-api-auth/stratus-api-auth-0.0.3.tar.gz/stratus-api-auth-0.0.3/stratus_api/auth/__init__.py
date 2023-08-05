def echo_access_token():
    from stratus_api.auth.oauth import get_service_access_token
    from stratus_api.core.settings import get_settings
    return dict(active=True, response=get_service_access_token(service_name=get_settings()['service_name']))
