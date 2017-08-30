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
from __future__ import print_function
from __future__ import unicode_literals

from djangolg import dialects, models


class LookingGlass(object):
    def __init__(self, router=None):
        if not isinstance(router, models.Router):
            raise ValueError
        self.dialect = dialects.get_dialect(router.dialect)
        self.device = self.dialect.driver_class(
            hostname=router.hostname,
            username=router.credentials.username,
            password=router.credentials.password)

    def __enter__(self):
        self.device.open()
        return self

    def __exit__(self, *args):
        self.device.__exit__(*args)

    def execute(self, method=None, target=None, option_index=None):
        output = {}
        method.dialect = self.dialect
        command = method.get_command(target=target, option_index=option_index)
        tmp = self.device.cli([command])
        raw = tmp[command]
        output['raw'] = raw
        return output
