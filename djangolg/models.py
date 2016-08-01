from __future__ import unicode_literals

from django.db import models


# TODO: Add "Dialect" option field
class Router(models.Model):
    hostname = models.CharField(max_length=20, unique=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    credentials = models.ForeignKey('Credential', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.hostname

    def __unicode__(self):
        return self.__str__()


class Location(models.Model):
    name = models.CharField(max_length=20)
    sitecode = models.CharField(max_length=10, unique=True, primary_key=True)

    def __str__(self):
        return self.sitecode

    def __unicode__(self):
        return self.__str__()


class Credential(models.Model):
    CRED_TYPE_PASSWD = 0
    CRED_TYPE_PUBKEY = 1
    CRED_TYPE_CHOICES = (
        (CRED_TYPE_PASSWD, "Password"),
        (CRED_TYPE_PUBKEY, "Public Key"),
    )
    name = models.CharField(max_length=20, unique=True)
    type = models.IntegerField(choices=CRED_TYPE_CHOICES)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    pubkey = models.BinaryField()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class Log(models.Model):
    EVENT_START = 0
    EVENT_QUERY_ACCEPT = 1
    EVENT_QUERY_REJECT = 2
    EVENT_QUERY_INVALID = 3
    EVENT_CHOICES = (
        (EVENT_START, "Session Started"),
        (EVENT_QUERY_ACCEPT, "Query Authorised"),
        (EVENT_QUERY_REJECT, "Query Rejected"),
        (EVENT_QUERY_INVALID, "Invalid Query"),
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.IntegerField(choices=EVENT_CHOICES)
    src_host = models.CharField(max_length=20)
    router = models.ForeignKey('Router', on_delete=models.SET_NULL, null=True)
    method_name = models.CharField(max_length=20, null=True)
    target = models.CharField(max_length=20, null=True)
    error = models.CharField(max_length=40, null=True)

    def __str__(self):
        str = "%s %s:: from:%s to:%s method:%s target:%s error:%s" % (
            self.timestamp,
            self.event,
            self.src_host,
            self.router,
            self.method_name,
            self.target,
            self.error,
        )
        return str

    def __unicode__(self):
        return self.__str__()
