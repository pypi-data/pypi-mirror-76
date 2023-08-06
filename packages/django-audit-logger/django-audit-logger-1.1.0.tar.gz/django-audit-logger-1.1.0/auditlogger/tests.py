"""
Tests for the module
"""
from django.contrib.auth.models import User  # type: ignore
from django.test import Client, TestCase  # type: ignore

from auditlogger.models import TestModel
from auditlogger.signals import get_organisation_field

# build in try/except for python2
try:
    from unittest import mock  # noqa
except ImportError:
    import mock  # type: ignore  # noqa


class MockedOrganisationObject(object):
    def __init__(self, organisation_name):
        self.organisation_name = organisation_name


class MockedProfileObject(object):
    def __init__(self, profile_id, organisation):
        self.profile_id = profile_id
        self.organisation = organisation


class MockedUserObject(object):
    def __init__(self, username, profile=None, organisation=None):
        self.username = username
        self.profile = profile
        self.organisation = organisation
        self.is_authenticated = True
        self.pk = 42
        self.is_staff = False
        self.is_superuser = False


class MockedRequestObject(object):
    def __init__(self, user=None, id=None):  # noqa
        self.user = user
        self.id = id

    @staticmethod
    def build_absolute_uri():
        return "url"


class MockedRequestObjectNoId(object):
    def __init__(self, user=None):  # noqa
        self.user = user

    @staticmethod
    def build_absolute_uri():
        return "url"


class TestUserObjectLogs(TestCase):
    """
    Test that manipulation of the default User object triggers log actions
    """

    def setUp(self):  # type () -> None
        """Setup testing environment"""
        self.user = User.objects.create_user("TestUser", "test@example.com", 123)
        self.client = Client()

    @mock.patch("auditlogger.signals.log_to_redis")
    def test_user_login_is_logged(self, mocked_log_to_redis):
        self.client.login(username=self.user.username, password=123)
        mocked_log_to_redis.delay.assert_called()
        self.assertEqual("USER_LOGIN", mocked_log_to_redis.delay.call_args[1]["action"])
        self.assertEqual(
            self.user.pk, mocked_log_to_redis.delay.call_args[1]["user"]["pk"]
        )

    @mock.patch("auditlogger.signals.log_to_redis")
    def test_user_user_login_failed_is_logged(self, mocked_log_to_redis):
        self.client.login(username=self.user.username, password="wrong_password")
        mocked_log_to_redis.delay.assert_called()
        self.assertEqual(
            "USER_LOGIN_FAILED", mocked_log_to_redis.delay.call_args[1]["action"]
        )
        self.assertEqual(
            self.user.username,
            mocked_log_to_redis.delay.call_args[1]["user"]["username"],
        )


class TestGetOrganisationFieldFunction(TestCase):
    @mock.patch("auditlogger.signals.app_settings")
    def test_organisation_field_not_set(self, mocked_settings):
        mocked_settings.AUDIT_LOGGER_USER_ORGANISATION_FIELD = []
        mocked_user = MockedUserObject(username="Harry")
        self.assertEqual(None, get_organisation_field(mocked_user))

    @mock.patch("auditlogger.signals.app_settings")
    def test_organisation_field_foreignkey(self, mocked_settings):
        mocked_settings.AUDIT_LOGGER_USER_ORGANISATION_FIELD = ["organisation"]
        mocked_organisation = MockedOrganisationObject(organisation_name="e-corp")
        mocked_user = MockedUserObject(
            username="Harry", organisation=mocked_organisation
        )
        result = get_organisation_field(mocked_user)
        self.assertEqual(
            mocked_organisation.organisation_name, result.organisation_name
        )

    @mock.patch("auditlogger.signals.app_settings")
    def test_organisation_field_nested(self, mocked_settings):
        mocked_settings.AUDIT_LOGGER_USER_ORGANISATION_FIELD = [
            "profile",
            "organisation",
        ]
        mocked_organisation = MockedOrganisationObject(organisation_name="e-corp")
        mocked_profile = MockedProfileObject(
            organisation=mocked_organisation, profile_id="Does not matter"
        )
        mocked_user = MockedUserObject(username="Harry", profile=mocked_profile)
        result = get_organisation_field(mocked_user)
        self.assertEqual(
            mocked_organisation.organisation_name, result.organisation_name
        )


class TestAuditloggerUpdateDeleteLogs(TestCase):
    @mock.patch("auditlogger.signals.log_to_redis")
    def test_edit_is_logged(self, mocked_log_to_redis):
        model_instance = TestModel.objects.create(name="test_2")
        mocked_log_to_redis.delay.assert_called()
        self.assertEqual("OBJ_CREATE", mocked_log_to_redis.delay.call_args[1]["action"])
        self.assertEqual(
            "TestModel", mocked_log_to_redis.delay.call_args[1]["instance"]["model"]
        )
        self.assertEqual(
            model_instance.id, mocked_log_to_redis.delay.call_args[1]["instance"]["pk"]
        )

    @mock.patch("auditlogger.signals.log_to_redis")
    def test_update_is_logged(self, mocked_log_to_redis):
        model_instance = TestModel.objects.create(name="test_1")
        model_instance.name = "changed"
        model_instance.save()
        mocked_log_to_redis.delay.assert_called()
        self.assertEqual("OBJ_UPDATE", mocked_log_to_redis.delay.call_args[1]["action"])
        self.assertEqual(
            "TestModel", mocked_log_to_redis.delay.call_args[1]["instance"]["model"]
        )
        self.assertEqual(
            model_instance.id, mocked_log_to_redis.delay.call_args[1]["instance"]["pk"]
        )
        self.assertEqual("changed", model_instance.name)

    @mock.patch("auditlogger.signals.log_to_redis")
    def test_create_is_logged(self, mocked_log_to_redis):
        model_instance = TestModel.objects.create(name="test_1")
        # Value is assigned to a variable as the instance will be deleted.
        model_instance_id = model_instance.id
        model_instance.delete()
        mocked_log_to_redis.delay.assert_called()
        self.assertEqual("OBJ_DELETE", mocked_log_to_redis.delay.call_args[1]["action"])
        self.assertEqual(
            "TestModel", mocked_log_to_redis.delay.call_args[1]["instance"]["model"]
        )
        self.assertEqual(
            model_instance_id, mocked_log_to_redis.delay.call_args[1]["instance"]["pk"]
        )


class TestSendLogFunction(TestCase):
    @mock.patch("auditlogger.signals.log_to_redis")
    @mock.patch("auditlogger.signals.AuditLoggerMiddleware")
    def test_middleware_called_if_request_not_provided(
        self, mocked_middleware, mocked_log_to_redis
    ):
        TestModel.objects.create(name="test_1")
        mocked_log_to_redis.return_value = None
        mocked_middleware.get_request.assert_called()

    @mock.patch("auditlogger.signals.log_to_redis")
    @mock.patch("auditlogger.signals.app_settings")
    def test_function_does_not_log_excluded_models(
        self, mocked_log_to_redis, mocked_settings
    ):
        mocked_settings.AUDIT_LOGGER_EXCLUDE = ["TestModel"]
        with self.assertRaises(AssertionError):
            TestModel.objects.create(name="test_1")
            mocked_log_to_redis.assert_called()

    @mock.patch("auditlogger.signals.log_to_redis")
    @mock.patch("auditlogger.signals.AuditLoggerMiddleware")
    @mock.patch("auditlogger.signals.get_client_ip")
    def test_request_data_fetched_if_present(
        self, mocked_get_client_ip, mocked_middleware, mocked_log_to_redis
    ):
        mocked_get_client_ip.return_value = 123
        mocked_middleware.get_request.return_value = MockedRequestObject(id=5)

        TestModel.objects.create(name="test_1")
        self.assertEqual(5, mocked_log_to_redis.delay.call_args[1]["request"]["id"])
        self.assertEqual(
            "url", mocked_log_to_redis.delay.call_args[1]["request"]["url"]
        )

    @mock.patch("auditlogger.signals.log_to_redis")
    @mock.patch("auditlogger.signals.AuditLoggerMiddleware")
    @mock.patch("auditlogger.signals.get_client_ip")
    def test_request_data_left_clear_if_not_present(
        self, mocked_get_client_ip, mocked_middleware, mocked_log_to_redis
    ):
        mocked_get_client_ip.return_value = 123
        mocked_middleware.get_request.return_value = MockedRequestObjectNoId()

        TestModel.objects.create(name="test_1")
        self.assertEqual("", mocked_log_to_redis.delay.call_args[1]["request"])

    @mock.patch("auditlogger.signals.log_to_redis")
    @mock.patch("auditlogger.signals.AuditLoggerMiddleware")
    @mock.patch("auditlogger.signals.get_client_ip")
    def test_function_tries_to_fetch_user_from_request(
        self, mocked_get_client_ip, mocked_middleware, mocked_log_to_redis
    ):
        mocked_get_client_ip.return_value = 123
        mocked_middleware.get_request.return_value = MockedRequestObjectNoId(
            user="karl"
        )
        TestModel.objects.create(name="test_1")
        self.assertEqual(
            "karl", mocked_log_to_redis.delay.call_args[1]["user"]["username"]
        )
        self.assertEqual(123, mocked_log_to_redis.delay.call_args[1]["user"]["ip"])

    @mock.patch("auditlogger.signals.log_to_redis")
    @mock.patch("auditlogger.signals.AuditLoggerMiddleware")
    @mock.patch("auditlogger.signals.get_client_ip")
    def test_function_tries_to_get_ip_from_request_ip_present(
        self, mocked_get_client_ip, mocked_middleware, mocked_log_to_redis
    ):
        mocked_get_client_ip.return_value = 123
        mocked_middleware.get_request.return_value = MockedRequestObjectNoId(
            user="karl"
        )
        mocked_log_to_redis.delay.return_value = None
        TestModel.objects.create(name="test_1")
        mocked_get_client_ip.assert_called()

    @mock.patch("auditlogger.signals.log_to_redis")
    @mock.patch("auditlogger.signals.AuditLoggerMiddleware")
    @mock.patch("auditlogger.signals.get_client_ip")
    def test_function_tries_to_get_ip_from_request_ip_not_present(
        self, mocked_get_client_ip, mocked_middleware, mocked_log_to_redis
    ):
        mocked_get_client_ip.return_value = 123
        mocked_middleware.get_request.return_value = None
        mocked_log_to_redis.delay.return_value = None
        with self.assertRaises(AssertionError):
            TestModel.objects.create(name="test_1")
            mocked_get_client_ip.assert_called()

    @mock.patch("auditlogger.signals.log_to_redis")
    @mock.patch("auditlogger.signals.AuditLoggerMiddleware")
    @mock.patch("auditlogger.signals.get_client_ip")
    @mock.patch("auditlogger.signals.get_organisation_field")
    def test_function_calls_get_organisation_field_method_with_correct_arguments(
        self,
        mocked_get_organisation_field,
        mocked_get_client_ip,
        mocked_middleware,
        mocked_log_to_redis,
    ):
        mocked_user = MockedUserObject(username="karl")
        mocked_get_organisation_field.return_value = "e-corp"
        mocked_get_client_ip.return_value = 123
        mocked_middleware.get_request.return_value = MockedRequestObjectNoId(
            user=mocked_user
        )
        mocked_log_to_redis.delay.return_value = None
        TestModel.objects.create(name="test_1")

        mocked_get_organisation_field.assert_called_with(mocked_user)

        self.assertEqual(123, mocked_log_to_redis.delay.call_args[1]["user"]["ip"])
        self.assertEqual(
            "e-corp", mocked_log_to_redis.delay.call_args[1]["user"]["organisation"]
        )
        self.assertEqual(42, mocked_log_to_redis.delay.call_args[1]["user"]["pk"])
        self.assertEqual(
            False, mocked_log_to_redis.delay.call_args[1]["user"]["is_staff"]
        )
        self.assertEqual(
            False, mocked_log_to_redis.delay.call_args[1]["user"]["is_superuser"]
        )
        mocked_get_client_ip.assert_called()
