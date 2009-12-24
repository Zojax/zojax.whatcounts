from zope import component, interface, schema
from z3c.form.object import registerFactoryAdapter

from interfaces import _, IEmailListFactory, IEmailList


class EmailList(object):
    interface.implements(IEmailList)

    title = None

    id = None

    name = None

    def __init__(self, name='', title=''):
        self.name = unicode(name)
        self.title = unicode(title)


class EmailListFactory(object):
    interface.implements(IEmailListFactory)

    title = None

    name = None

    def __call__(self):
        return EmailList(self.name, self.title)


registerFactoryAdapter(IEmailList, EmailList)
