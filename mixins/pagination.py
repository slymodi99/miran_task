from django.utils.translation import gettext as _
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"
    page_size = 20


    def get_paginated_response(self, data, extra=None):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'result': data,
            'status': True,
            'other': extra,
            'message': _('Retrieved Successfully')
        }, status=200)
