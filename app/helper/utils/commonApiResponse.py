from rest_framework.response import Response
from rest_framework import status


def CommonApiResponse(data=None, message=None, status_code=None, errors=None):
        response = {
            "success": status.is_success(status_code),
            "status_code": status_code,
            "message": message if message else status.HTTP_200_OK,
            "data": data if data else {},
            "errors": errors if errors else {},
        }
        return Response(response, status=status_code)