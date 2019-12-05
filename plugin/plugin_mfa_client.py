#
#   Copyright (c) 2019 One Identity
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
from safeguard.sessions.plugin import AAPlugin, AAResponse
from safeguard.sessions.plugin.mfa_client import MFAClient


class Plugin(AAPlugin):
    def do_authenticate(self):
        # This is glue code to instantiate an MFAClient and execute it
        client = MyClient.from_config(self.plugin_configuration)
        return client.execute_authenticate(self.username, self.mfa_identity, self.mfa_password)


class MyClient(MFAClient):
    def __init__(self, server_url=None):
        self.server_url = server_url
        super().__init__(branded_name="SPS AA Skeleton")

    @classmethod
    def from_config(cls, plugin_configuration, section="skeleton"):
        # It is good practice to separate configuration handling in its own function
        return cls(server_url=plugin_configuration.get(section, "server_url"))

    def otp_authenticate(self, username, otp):
        if otp == "1234":
            # The code may return an AAResponse (dict) which will be passed through to SPS
            return AAResponse.need_info("Are you sure?", "confirm")
        else:
            # Contact the service at self.server_url and actually check the OTP
            # Returning True means returning ACCEPT as verdict
            return True

    def push_authenticate(self, user):
        # Contact the service at self.server_url and actually check the push notification
        # Returning False means returning DENY as verdict
        return False
