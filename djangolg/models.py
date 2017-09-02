# Copyright 2017 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Model classes for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.db import models

from djangolg import dialects, events


class Router(models.Model):
    """Database representation of a router."""

    hostname = models.CharField(max_length=20, unique=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL,
                                 null=True)
    credentials = models.ForeignKey('Credential', on_delete=models.SET_NULL,
                                    null=True)
    dialect = models.CharField(
        max_length=20,
        choices=dialects.available_dialects(output="choices"),
        null=True)

    @property
    def label(self):
        """Render router display label from attributes."""
        from djangolg.settings import ROUTER_LABEL
        return ROUTER_LABEL(self)

    def __str__(self):
        """Return string representation."""
        return self.hostname

    def __unicode__(self):
        """Return string representation."""
        return self.__str__()


class Location(models.Model):
    """Database representation of a location."""

    name = models.CharField(max_length=50)
    sitecode = models.CharField(max_length=10, unique=True)

    def __str__(self):
        """Return string representation."""
        return self.sitecode

    def __unicode__(self):
        """Return string representation."""
        return self.__str__()


class Credential(models.Model):
    """Database representation of device credentials."""

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
        """Return string representation."""
        return self.name

    def __unicode__(self):
        """Return string representation."""
        return self.__str__()


class Log(models.Model):
    """Database representation of a command log entry."""

    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.IntegerField(choices=events.EVENT_CHOICES)
    src_host = models.CharField(max_length=20)
    router = models.ForeignKey('Router', on_delete=models.SET_NULL, null=True)
    method_name = models.CharField(max_length=20, null=True)
    target = models.CharField(max_length=20, null=True)
    key = models.CharField(max_length=40, null=True)
    error = models.CharField(max_length=40, null=True)

    def __str__(self):
        """Return string representation."""
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
        """Return string representation."""
        return self.__str__()
