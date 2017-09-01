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

from django.http import HttpRequest, JsonResponse
from django.views.generic import View

from djangolg import events, exceptions, forms, keys, methods, models, settings
from djangolg.lg import LookingGlass
from djangolg.views.helpers import get_src


class LookingGlassJsonView(View):
    """LookingGlass view class for djangolg."""

    def get(self, request):
        """Handle GET request."""
        try:
            self.log = models.Log()
            self.parse(request=request)
            self.authorise()
            self.validate()
            data = self.execute()
        except Exception as e:
            resp = JsonResponse(**self.handle_error(e))
            if settings.DEBUG:
                raise e
        else:
            self.log.event = events.EVENT_QUERY_ACCEPT
            resp = JsonResponse(data)
        finally:
            try:
                self.log.src_host = self.src_host
                self.log.key = self.key
                self.log.method_name = self.method_name
                self.log.router = self.router
                self.log.target = self.target
            except AttributeError:
                pass
            finally:
                self.log.save()

        return resp

    def parse(self, request=None):
        """Parse the HttpRequest."""
        exceptions.check_type(instance=request, classinfo=HttpRequest)
        try:
            self.query = request.GET
            self.src_host = get_src(request)
            self.key = self.query['auth_key']
            self.method_name = self.query['method_name']
        except Exception as e:
            raise QueryParsingError(e.message)

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
            raise FormValidationError(form.errors.as_data())

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

    def handle_error(self, e=exceptions.LookingGlassError):
        """Handle an error raised during query progressing."""
        exceptions.check_type(instance=e, classinfo=Exception)
        if isinstance(e, exceptions.LookingGlassError):
            status = e.http_status
            reason = e.http_reason
            data = e.response_data
            self.log.event = e.log_event
            self.log.error = e.log_error
        else:
            status = exceptions.DEFAULT_STATUS
            reason = exceptions.DEFAULT_REASON
            data = {}
            self.log.event = exceptions.DEFAULT_EVENT
            self.log.error = exceptions.default_error_message(e=e)
        return {'data': data, 'status': status, 'reason': reason}


class QueryParsingError(exceptions.LookingGlassError):
    """Generic query parsing exception."""

    log_event = events.EVENT_QUERY_INVALID
    http_status = 400
    http_reason = None


class AuthorisationError(exceptions.LookingGlassError):
    """Generic command authorisation exception."""

    log_event = events.EVENT_QUERY_REJECT
    http_status = 401
    http_reason = "An error occured during authorisation key validation. \
                   Please try again or contact support."


class MaxRequestsExceeded(AuthorisationError):
    """Exception raised when MAX_REQUESTS is exceeded."""

    http_reason = "The maximum number of allowed requests has been exceeded. \
                   Please wait to try again later, or contact support."

    def __init__(self, max_requests=None, request_count=None, *args, **kwargs):
        """Initialise new MaxRequestsExceeded instance."""
        message = "Request count {0} > {1}".format(request_count, max_requests)
        super(self.__class__, self).__init__(message, *args, **kwargs)


class FormValidationError(exceptions.LookingGlassError):
    """Generic form validation execption."""

    log_event = events.EVENT_QUERY_INVALID
    http_status = 400
    http_reason = "Some query parameters failed to validate."

    def __init__(self, wrap_errors=None, *args, **kwargs):
        """Initialise new MaxRequestsExceeded instance."""
        if isinstance(wrap_errors, dict):
            self.wrap_errors = wrap_errors
        super(self.__class__, self).__init__(wrap_errors, *args, **kwargs)

    @property
    def response_data(self):
        """Render a dict with a description of the validation errors."""
        data = {}
        if self.wrap_errors:
            data = {'error_message': ""}
            for field, errors in self.wrap_errors.iteritems():
                data["error_message"] += "{0} ".format(field).capitalize()
                for error in errors:
                    for message in error:
                        data["error_message"] += "{0}.".format(message)
        return data


class ExecutionError(exceptions.LookingGlassError):
    """Generic command execution exception."""

    log_event = events.EVENT_QUERY_FAILED
    http_status = 503
    http_reason = "An error occured during query execution. \
                   Please try again or contact support."
