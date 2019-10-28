from rest_framework.permissions import BasePermission
from .models import MailingList, Subscriber


class CanUseMailingList(BasePermission):
    message = 'User do not have access to this resource'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if isinstance(obj, Subscriber):
            return obj.mailing_list.user_can_use_mailinglist(user)
        elif isinstance(obj, MailingList):
            return obj.user_can_use_mailinglist(user)
        else:
            return False
