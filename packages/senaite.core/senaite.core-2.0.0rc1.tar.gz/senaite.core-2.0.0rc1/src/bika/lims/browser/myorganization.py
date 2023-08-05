# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.
#
# SENAITE.CORE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2020 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from bika.lims.browser import BrowserView


class MyOrganizationView(BrowserView):
    """Redirects to the current user's organization view, if any. Otherwise,
    falls-back to portal view
    """

    def __call__(self):
        url = api.get_url(api.get_portal())
        current_user = api.get_current_user()
        contact = api.get_user_contact(current_user)
        if contact:
            parent = api.get_parent(contact)
            url = api.get_url(parent)

        return self.request.response.redirect(url)
