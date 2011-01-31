from zope import interface, schema
from zope.i18nmessageid.message import MessageFactory

_ = MessageFactory('zojax.whatcounts')


class IEmailListFactory(interface.Interface):

    name = schema.TextLine(title=_(u'Name'))

    title = schema.TextLine(title=_(u'Title'))


class IEmailList(interface.Interface):

    name = schema.TextLine(title=_(u'Name'))

    title = schema.TextLine(title=_(u'Title'))

    id = schema.TextLine(title=_(u'Id'),
                         default=u'<Your Id>')


class IWhatCountsConfiglet(interface.Interface):

    enabled = schema.Bool(title=_(u'Enabled'),
                          default=False)

    realm = schema.TextLine(title=_(u'Realm'))

    key = schema.Password(title=_(u'API Key'))

    lists = schema.Tuple(title=_(u"Lists"),
                         value_type=schema.Object(title=_(u'List'),
                                                 schema=IEmailList))

    def getList(name):
        """get list by name"""

    def subscribeUser(email, listId, **data):
        """ subscribe user """
