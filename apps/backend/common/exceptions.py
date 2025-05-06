from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Service temporarily unavailable, please try again later.'
    default_code = 'service_unavailable'


class InvalidInput(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input provided.'
    default_code = 'invalid_input'


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF to standardize error responses.
    """
    # Call DRF's default exception handler first to get the standard error response
    response = exception_handler(exc, context)

    # If this is a Django validation error, convert it to DRF validation error
    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(detail=exc.message_dict)
        response = exception_handler(exc, context)

    # If no response is generated yet, let Django handle it
    if response is None:
        return None

    # Add more context to the error response
    if isinstance(exc, Http404):
        response.data = {
            'success': False,
            'message': 'Not found.',
            'detail': str(exc),
            'code': 'not_found'
        }
    elif isinstance(exc, DRFValidationError):
        response.data = {
            'success': False,
            'message': 'Validation error.',
            'errors': response.data,
            'code': 'validation_error'
        }
    else:
        response.data = {
            'success': False,
            'message': getattr(exc, 'default_detail', str(exc)),
            'detail': response.data.get('detail', str(exc)),
            'code': getattr(exc, 'default_code', 'error')
        }

    return response
