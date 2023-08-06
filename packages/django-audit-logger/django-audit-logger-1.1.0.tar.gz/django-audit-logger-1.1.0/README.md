# Django Audit Logger

A django package that allows you to log user logins and changes to instances of the models within your project.

## Install


#### Pip
`pip install django-audit-logger`


#### Dependencies:

* Django
* Boto3
* Celery
* Redis

Works with both python 2.7 and all versions of python that support Django 1.11 (>= 3.4)


#### Update Settings


Add the following settings to your `settings.py` file and give them the correct values.

```
AUDIT_LOGGER_REGION = ''
AUDIT_LOGGER_KEY_ID = ''
AUDIT_LOGGER_SECRET_ACCESS_KEY = ''
AUDIT_LOGGER_GROUP_NAME = ''
AUDIT_LOGGER_STREAM_NAME = ''
AUDIT_LOGGER_EXCLUDE = []
AUDIT_LOGGER_USER_ORGANISATION_FIELD = []
LOG_INTERVAL = ''
```

Add `auditlogger` to your `INSTALLED_APPS`.

#### Optional: Add your models to the logger:

By default, only `User` logins are logged. You can start logging additional models by using the `@auditlogger_update_delete` decorator.

```
from auditlogger.signals import auditlogger_update_delete

@auditlogger_update_delete
class ModelToLog(models.Model):
    name = models.CharField(max_length=100)
    (...)

```

Both create, update and delete actions will be logged.


## Settings

### AWS settings

```
AUDIT_LOG_REGION
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```
These settings manage the connection to AWS.


### CloudWatch settings


`AUDIT_LOG_GROUP_NAME`

The name of the LogGroup within CloudWatch to sent the logs to.

`AUDIT_LOG_STREAM_NAME`

The name of the log stream. 

### Audit-logger settings:

`AUDIT_LOG_EXCLUDE` 

Just as you can include models to be logged, you can also exclude them. This is useful for models that will be logged by default. For example, one can exclude the django `Session` object like so: `AUDIT_LOG_EXCLUDE = ['Session']`

`AUDIT_LOGGER_USER_ORGANISATION_FIELD`

If the project that you wish to collect the audit-logger to uses tenants, academies or an equivalent that users are members of, you can add them to the logs through this setting. The organisation will be displayed as the value of the `organisation` field in the logs.

The `organisation` may be linked to the `user` as a direct relation, or through an intermediary object like a `profile` model. To support both scenarios the value 
should be provided as a list.

For example in the following scenarios:

`user` -> `organisation` the value should be: `['organisation']`

`user` -> `profile` -> `organisation` the value should be: `['profile', 'organisation']`


`LOG_INTERVAL`

The logs are pushed to cloudwatch in batches, with all logged events being held in redis until the log interval expires. The interval value represents the time in minutes, with `5` as the default.


## Custom log events

You can also link other signals used in your app to the logger like so:

```
from auditlogger.signals import send_log
from django.dispatch import receiver, Signal
from myapp.models import Organisation

organisation_login_signal = Signal(providing_args=['date', 'instance'])


@receiver(organisation_login_signal, sender=Organisation)
def organisation_login(**kwargs):
    """detect organisation logins"""
    send_log('ORGANISATION_LOGIN', **kwargs)

```

## Test

The app comes with included tests that you can run with the following command from the `django-audit-logger` directory (requires the `python manage.py migrate` command to have been run):

`python auditlogger/run_tests.py`
