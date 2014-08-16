from django.http import HttpResponse,HttpResponseRedirect
import urllib2
from xml.dom.minidom import parseString, parse
import json
from django.conf import settings


def api_contacts(request, backend, uid, user=None, *args, **kwargs):
    accounts = kwargs.get('response', None)
    if backend.name == 'google-oauth2':
        url = 'https://www.google.com/m8/feeds/contacts/default/full?oauth_token='+accounts['access_token'] + '&max-results=2000'
        x = urllib2.urlopen(url).read()
        dom = parseString(x)
        hreflist = [elt.getAttribute("address") for elt in dom.getElementsByTagName('gd:email')]
        emails_from_contacts = []
        for email in hreflist:
            emails_from_contacts.append(email)
            #print email

        settings.CONTACTS['emails'] = emails_from_contacts
        return HttpResponseRedirect('/email_sent/')
    elif backend.name == 'live':
        url = 'https://apis.live.net/v5.0/me/contacts?access_token=' + accounts['access_token']
        x = urllib2.urlopen(url).read()
        emails = json.loads(x)
        emails_from_contacts = []
        for email in emails['data']:
            emails_from_contacts.append(email['name'])
            print email
        settings.CONTACTS['emails'] = emails_from_contacts
        return HttpResponseRedirect('/email_sent/')
    elif backend.name == "yahoo":
        #url = 'http://social.yahooapis.com/v1/user/'+accounts['openid'] +'/contacts'
        #x = urllib2.urlopen(url).read()
        x = 0
        return HttpResponse(x)

