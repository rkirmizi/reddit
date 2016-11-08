# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://code.reddit.com/LICENSE. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is reddit.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is reddit Inc.
#
# All portions of the code written by reddit are Copyright (c) 2006-2015 reddit
# Inc. All Rights Reserved.
###############################################################################
import re
try:
    from sparkpost import SparkPost
except ImportError:
    raise ImportError('Please install sparkpost to be able to use this mail backend')

from r2.lib.configparse import ConfigValue

from r2.lib.providers.email import (
    EmailProvider,
    EmailSendError,
)
from r2.lib.utils import tup


class SparkPostEmailProvider(EmailProvider):
    """A provider that uses sparkpost to send emails."""

    def send_email(self, to_address, from_address, subject, text, reply_to=None,
                   parent_email_id=None, other_email_ids=None):
        from pylons import app_globals as g
        from_address = g.config.get('notification_email') or 'noreply@rsaudis.com'
        to_address = (to_address,)
        API_KEY = 'fb977504a3821f9edb6d1c7ecdb2d7514a923c97'
        sp = SparkPost(API_KEY)
        try:
            response = sp.transmissions.send(recipients=to_address, html=text, from_email=from_address,subject=subject)
            g.stats.simple_event("sparkpost.outgoing.success")
            email_id = response["id"]
            return email_id

        except Exception as e:
            msg = "sparkpost sending email failed: {}".format(unicode(e))
            g.stats.simple_event("sparkpost.outgoing.failure")
            raise EmailSendError(msg)
