from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError


class ValidateModelMixin:
    """
    Mixin to fully validate a model instance before saving.
    """

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            instance.full_clean()
        except ValidationError as e:
            instance.delete()
            raise ValidationError(e)

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
            instance.full_clean()
        except ValidationError as e:
            # Restore the original instance
            instance.refresh_from_db()
            raise ValidationError(e)


class ResponseWithMetadataMixin:
    """
    Mixin to add metadata to list responses.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Get pagination information if pagination is enabled
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
