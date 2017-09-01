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
"""Event code constants for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals


EVENT_START = 0
EVENT_QUERY_ACCEPT = 1
EVENT_QUERY_REJECT = 2
EVENT_QUERY_INVALID = 3
EVENT_QUERY_FAILED = 4
EVENT_QUERY_ERROR = 5
EVENT_CHOICES = (
    (EVENT_START, "Session Started"),
    (EVENT_QUERY_ACCEPT, "Query Authorised"),
    (EVENT_QUERY_REJECT, "Query Rejected"),
    (EVENT_QUERY_INVALID, "Invalid Query"),
    (EVENT_QUERY_FAILED, "Query Execution Failed"),
    (EVENT_QUERY_ERROR, "Unhandled Error")
)
