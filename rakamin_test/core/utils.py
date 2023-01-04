from typing import Union

from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from rakamin_test.apps.users.model import users


class PaginatorPage(object):
    def __init__(self, queryset: QuerySet, page_number: Union[str, int] = 1,
                 step: int = 20, skip_step_calculation: bool = False) -> None:
        try:
            page_number = int(page_number or 1)
        except ValueError:
            page_number = 1

        self.next = None
        self.next_object = None
        self.step = step
        self.total_data = queryset.count() if not skip_step_calculation else 0

        # We want our implementation of pagination to have access
        # to both previous and next object.

        stop_index = (page_number * step) + 1

        # If we're not in the first page, fetch the previous item
        # in addition to fetching the next item
        if page_number > 1:
            start_index = (page_number - 1) * step - 1

            list_queryset = list(queryset[start_index:stop_index])
            self.previous = page_number - 1

            # even when number is bigger than possible, no errors are produced
            if len(list_queryset):
                self.previous_object = list_queryset[0]
            else:
                self.previous_object = None
            self.objects = list_queryset[1:step + 1]

            # If the number of result is two more than number
            # of objects in a page, there's a next page
            if len(list_queryset) == step + 2:
                self.next_object = list_queryset[-1]
                self.next = page_number + 1

        else:
            self.previous = None
            self.previous_object = None
            start_index = (page_number - 1) * step
            list_queryset = list(queryset[start_index:stop_index])

            # If the number of result is more than number of objects
            # in page, we know there's a next page
            if len(list_queryset) > step:
                self.next = page_number + 1
                self.next_object = list_queryset[-1]

            self.objects = list_queryset[0:step]

class AuthBackend(ModelBackend):
    def authenticate(username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(mobile_number=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None