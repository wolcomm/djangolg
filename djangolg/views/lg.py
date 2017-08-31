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
"""LookingGlass view module for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.http import JsonResponse
from django.views.generic import View

from djangolg import exceptions, forms, keys, methods, models, settings
from djangolg.lg import LookingGlass
from djangolg.views.helpers import get_src


class LookingGlassJsonView(View):
    """LookingGlass view class for djangolg."""

    def get(self, request):
        """Handle GET request."""
        # get the query or return a 400 error
        self.query = request.GET
        if not self.query:
            return JsonResponse({}, status=400)
        # get the source address and auth_key for validation
        self.src_host = get_src(self.request)
        self.key = self.query['auth_key']
        self.method_name = self.query['method_name']
        # set up the log entry
        log = models.Log()

        try:
            self.authorise()
            self.validate()
            data = self.execute()
        except (AuthorisationError, keys.KeyValidationError) as e:
            log.event = models.Log.EVENT_QUERY_REJECT
            log.error = e.message
        except (FormValidationError, methods.LookingGlassMethodError) as e:
            log.event = models.Log.EVENT_QUERY_INVALID
            log.error = e.message
        except ExecutionError as e:
            log.event = models.Log.EVENT_QUERY_FAILED
            log.error = e.message
        except Exception as e:
            log.event = models.Log.EVENT_QUERY_ERROR
            log.error = e.message
            raise e
        finally:
            try:
                if log.event:
                    resp = JsonResponse({}, status=400, reason=log.error)
                else:
                    log.event = models.Log.EVENT_QUERY_ACCEPT
                    resp = JsonResponse(data)
                log.src_host=self.src_host
                log.key = self.key
                log.method_name = self.method_name
                log.router = self.router
                log.target = self.target
            except AttributeError:
                pass
            finally:
                log.save()

        return resp

    def authorise(self):
        """Check AuthKey validity."""
        if not (self.src_host and self.key):
            raise AuthorisationError("src_host or key not set")
        try:
            keys.AuthKey(self.src_host).validate(self.key)
            count = models.Log.objects.filter(key=self.key).count()
        except keys.KeyValidationError:
            raise
        except Exception as e:
            raise AuthorisationError(e.message)
        if not settings.MAX_REQUESTS or count < settings.MAX_REQUESTS:
            return True
        else:
            raise MaxRequestsExceeded(max_requests=settings.MAX_REQUESTS,
                                      request_count=count)
        raise AuthorisationError("An error occured during command \
                                  authorisation")

    def validate(self):
        """Validate the request query parameters."""
        self.method = methods.get_method(self.method_name)
        form = forms.form_factory(method=self.method, data=self.query)
        if form.is_valid():
            self.router = form.cleaned_data['router']
            self.target = form.cleaned_data['target']
            if 'options' in form.fields:
                self.option_index = form.cleaned_data['options']
            else:
                self.option_index = None
        else:
            raise FormValidationError(form.errors)


    def execute(self):
        """Execute Looking Glass request."""
        if not (self.method and self.router and self.target):
            raise ExecutionError("command parameters missing")
        try:
            with LookingGlass(router=self.router) as lg:
                output = lg.execute(
                    method=self.method,
                    target=self.target,
                    option_index=self.option_index
                )
        except Exception as e:
            raise ExecutionError(e.message)
        return output


class AuthorisationError(exceptions.LookingGlassError):
    """Generic command authorisation exception."""


class MaxRequestsExceeded(AuthorisationError):
    """Exception raised when MAX_REQUESTS is exceeded."""

    def __init__(self, max_requests=None, request_count=None, *args, **kwargs):
        """Initialise new MaxRequestsExceeded instance."""
        message = "Request count {0} > {1}".format(request_count, max_requests)
        super(self.__class__, self).__init__(message, *args, **kwargs)


class FormValidationError(exceptions.LookingGlassError):
    """Generic form validation execption."""


class ExecutionError(exceptions.LookingGlassError):
    """Generic command execution exception."""
