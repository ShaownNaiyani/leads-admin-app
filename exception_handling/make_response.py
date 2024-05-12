

def response(data, status_code, message):
    """
    Generate a response with the given data and status code.
    """
    return {
        'data': data,
        'status_code': status_code,
        'message': message
    }
