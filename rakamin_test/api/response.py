import json

from typing import Optional

from rest_framework import status, serializers
from rest_framework.response import Response



class ErrorResponse(Response):
    """
    API subclass from rest_framework response to simplify constructing error messages
    """
    def __init__(self, serializer: Optional[serializers] = None, error_code: str = "", error_message: str = ""):
        super().__init__(status=status.HTTP_400_BAD_REQUEST)

        data: dict = {
            'error_message': 'Your request cannot be completed',
            'error_code': 'invalid_request'
        }

        if error_code:
            data["error_code"] = error_code

        if error_message:
            data["error_message"] = error_message

        print(serializer.errors)
        if serializer and serializer.errors.items():
            data['errors'] = {}

            for field, errors in serializer.errors.items():
                key = field
                message = errors[0]
                data['errors'][key] = message.title()
                data["error_code"] = message.code if message.code else "invalid_data"
                data["error_message"] = message.title()

                break
        self.data = data

def error_response(message: str) -> Response:
    data ={
        'messages': message,
        'is_success': False
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
