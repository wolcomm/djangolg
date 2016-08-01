from __future__ import unicode_literals

from django.db import models


# TODO: Replace "Syntax" with "Dialect" option field
class Router(models.Model):
    hostname = models.CharField(max_length=20, unique=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    credentials = models.ForeignKey('Credential', on_delete=models.SET_NULL, null=True)
    syntax = models.ForeignKey('Syntax', on_delete=models.SET_NULL, null=True)

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


# TODO: Remove
class Syntax(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


# TODO: Remove
class Command(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


# TODO: Remove
class CommandMap(models.Model):
    syntax = models.ForeignKey('Syntax', on_delete=models.SET_NULL, null=True)
    command = models.ForeignKey('Command', on_delete=models.CASCADE)
    cmd_template = models.CharField(max_length=50)

    def __str__(self):
        return u"%u / %u" % (self.syntax, self.command)

    def __unicode__(self):
        return self.__str__()
