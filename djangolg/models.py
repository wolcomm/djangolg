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
