

def checkIsNeedAutheticaitonForUrl(path):
    unAuthenticateUrlList = [
        '/api/v1/auth/register/',
        '/api/v1/auth/verify-email/',
        '/api/v1/auth/login/',
        '/api/v1/auth/password-reset/'
    ]

    for item in unAuthenticateUrlList:
        if(path == item):
            return True
    return False;