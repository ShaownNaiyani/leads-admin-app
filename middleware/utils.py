

def checkIsNeedAutheticaitonForUrl(path):
    unAuthenticateUrlList = [
        '/api/v1/auth/register/',
        '/api/v1/auth/verify-email/',
        '/api/v1/auth/login/',
        '/api/v1/auth/password-reset/',
        '/spapi/api/get_sts_credentials',
        '/spapi/api/get_lwa_token'
    ]

    for item in unAuthenticateUrlList:
        if(path == item):
            return True
    return False;