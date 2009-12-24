import logging
from rwproperty import getproperty, setproperty
import urllib
import xml.etree.ElementTree
from xml.parsers.expat import ExpatError

from PyWhatCounts.Wrapper import WCWrapper
from PyWhatCounts.exceptions import WCSystemError, WCUserError, WCAuthError

from zope import component, interface, schema

from zojax.principal.profile.interfaces import IPrincipalInformation,\
    IPersonalProfile

from interfaces import _, IEmailListFactory, IEmailList

logger = logging.getLogger("zojax.whatcounts")


class WhatCountsConfiglet(object):

    def subscribeUser(self, email, listId, **data):
        realm = self.realm
        key = self.key
        if not self.enabled:
            return
        if not realm or not key or not listId:
            # WhatCounts API is not configured. Abort the submission.
            logger.warning("WhatCounts API is not configured.")
            return
        client = WCWrapper()
        client._setConnectionInfo(realm, key)
        try:
            client.subscribeUser(email, listId)
            if data:
                client.updateUser(email, listId, **data)
        except (WCAuthError, WCSystemError, WCUserError), exc:
            logger.warning('Subscribe error', exc_info=True)

    @getproperty
    def lists(self):
        lists = self.data.get('lists', {})
        if not isinstance(lists, dict):
            lists = {}
        updated = False
        res = []
        for name, factory in component.getUtilitiesFor(IEmailListFactory):
            if name not in lists:
                lists[name] = factory()
                updated = True
            res.append(lists[name])
        if updated:
            self.data['lists'] = lists
        return sorted(res, key=lambda x: x.title)

    @setproperty
    def lists(self, value):
        self.data['lists'] = dict([(lst.name, lst) for lst in value])

    def getList(self, name):
        lists = self.lists
        return self.data['lists'][name]
