""" Models are used to run tests against """
from django.db import models
from auditlogger.signals import auditlogger_update_delete


@auditlogger_update_delete
class TestModel(models.Model):
    """ A simple model to run tests against """

    name = models.CharField(max_length=100)
