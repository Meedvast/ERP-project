status_msg = {
    200: 'OK',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    500: 'Internal Server Error',
    503: 'Service Unavailable'
}


def to_dict_msg(status=200, data=None, msg=None):
    return {
        "status": status,
        "data": data,
        "msg": msg if msg else status_msg[status]
    }
