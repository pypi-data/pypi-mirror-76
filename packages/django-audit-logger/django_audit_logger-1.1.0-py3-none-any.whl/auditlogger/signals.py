"""Signals"""
import datetime
import inspect
import time

import django  # type: ignore
from django.contrib.auth.signals import user_logged_in  # type: ignore
from django.db.models.signals import post_delete, post_save  # type: ignore
from django.dispatch import receiver  # type: ignore
from six import string_types

import auditlogger.app_settings as app_settings
from auditlogger.middleware import AuditLoggerMiddleware
from auditlogger.tasks import log_to_redis


def get_organisation_field(user):
    """
    The organisation field may be linked to the user as a direct relation,
     or through an intermediary object like a Profile model. To support
     both scenarios the AUDIT_LOGGER_USER_ORGANISATION_FIELD returns a list
     of fieldnames to step through, with the lasts one being the name of
    the organisation field.

    This function parses the value of the AUDIT_LOGGER_USER_ORGANISATION_FIELD
     and returns the correct value for the user.
    """
    organisation_field = app_settings.AUDIT_LOGGER_USER_ORGANISATION_FIELD
    if not organisation_field:
        return None

    current_field_value = user
    for field in organisation_field:
        current_field_value = getattr(current_field_value, field)
    if current_field_value:
        return current_field_value


def get_client_ip(request):  # type () -> str
    """Fetch and return IP address of the user"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@receiver(user_logged_in)
def user_logged_in(**kwargs):  # type () -> None
    """Detect a user login"""
    user = kwargs.pop("user")
    send_log("USER_LOGIN", user=user, **kwargs)


# The 'user_login_failed' signal does not exist in Django <= 1.4
if not django.get_version().startswith("1.4"):

    from django.contrib.auth.signals import user_login_failed

    @receiver(user_login_failed)
    def user_login_failed(**kwargs):
        try:
            user = kwargs.get("credentials", {}).get("username")
        except KeyError:
            user = None

        send_log("USER_LOGIN_FAILED", user=user, **kwargs)


def log_save(**kwargs):  # type () -> None
    """
    Detect if save is applied to a newly created object
    or if its an update. Log it to amazon cloudwatch.
    """
    action = "OBJ_UPDATE" if not kwargs.get("created", False) else "OBJ_CREATE"
    send_log(action, **kwargs)


def log_delete(**kwargs):  # type () -> None
    """Log delete"""
    send_log(action="OBJ_DELETE", **kwargs)


def send_log(action, request=None, user=None, **kwargs):  # type () -> None
    """Sends a log to amazon cloudwatch"""

    if not request:
        request = AuditLoggerMiddleware.get_request()

    # Instance data
    sender = kwargs.get("sender")
    sender_name = sender if isinstance(sender, string_types) else str(sender.__name__)

    # Don't log excluded objects
    if sender_name in app_settings.AUDIT_LOGGER_EXCLUDE:
        return

    # Create a list of updated fields, or return an empty one
    update_fields = kwargs.get("update_fields")
    fields = list(update_fields) if update_fields else []

    # Format instance data
    instance = kwargs.get("instance")
    instance_data = (
        dict(
            model=sender_name,
            name=str(instance),
            pk=instance.pk,
            fields=fields,
            timestamp=int(time.time()) * 1000,
        )
        if instance
        else None
    )

    # Request data
    if hasattr(request, "id"):
        request_id = getattr(request, "id") if request else None
        url = request.build_absolute_uri() if request else None
        request_data = dict(id=request_id, url=url)
    else:
        request_data = ""

    # User data
    if not user and request:
        user = getattr(request, "user")

    # Get user IP
    ip = get_client_ip(request) if request else None
    user_data = dict(ip=ip)

    if isinstance(user, string_types):
        user_data.update(username=user)
    elif user and user.is_authenticated:

        organisation_field_value = get_organisation_field(user)
        if organisation_field_value:
            user_data.update(organisation=str(organisation_field_value))

        user_data.update(
            pk=user.pk, is_staff=user.is_staff, is_superuser=user.is_superuser
        )

    # Stack trace
    stack = ["{}:{} {}".format(s[1], s[2], s[3]) for s in inspect.stack()]

    # Create date
    date = datetime.datetime.utcnow().isoformat()

    # Log data
    log_data = dict(
        date=date,
        request=request_data,
        action=action,
        user=user_data,
        instance=instance_data,
        stack=stack,
    )
    log_to_redis.delay(**log_data)


def auditlogger_update_delete(cls):  # type () -> Object
    """Decorator to connect the class to the correct signals"""
    post_save.connect(log_save, cls, dispatch_uid=cls.__name__)
    post_delete.connect(log_delete, cls, dispatch_uid=cls.__name__)
    return cls
