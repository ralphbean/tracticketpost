from twill.browser import TwillBrowser
from BeautifulSoup import BeautifulSoup

import sys

class Ticket(object):
    _param_defaults = {
        'user' : 'user',
        'passwd' : 'password',
        'realm' : 'example realm',
        'uri' : 'trac.example.com'
    }
    _field_defaults = {
            'summary' : 'new ticket',
            'reporter' : 'tracticketpost',
            'type' : 'task',
            'priority' : 'major',
            'milestone' : '',
            'component' : '',
            'cc' : '',
            'owner' : '',
            'status' : 'new'
    }

    """ List of possible arguments to __init__(self, ...) """
    defaults = dict(
        [(k,v) for k,v in _param_defaults.iteritems()] + \
        [(k,v) for k,v in _field_defaults.iteritems()]
    )

    def __init__(self, **kw):
        self.fields, self.params = self._field_defaults, self._param_defaults
        possible_keys = self._field_defaults.keys()+self._param_defaults.keys()
        for k, v in kw.iteritems():
            if not k in possible_keys:
                raise ValueError, "Unexpected keyword '%s=%s'"%(str(k),str(v))

            if k in self.fields:
                self.fields[k] = v
            elif k in self.params:
                self.params[k] = v

        self.br = TwillBrowser()
        self.br.creds.add_password(*[
            self.params[k] for k in ['realm', 'uri', 'user', 'passwd']
        ])


    def _get_form_token(self):
        url = 'https://%s/newticket' % self.params['uri']
        self.br.go(url)
        code = self.br.get_code()
        if code != 200:
            raise Exception, "(Code: %i)  Failed to access %s." % (code, url)
        soup = BeautifulSoup(self.br.get_html())
        return soup.findAll('input', attrs={'name':'__FORM_TOKEN'})[0]['value']

    def submit(self):
        token = self._get_form_token()
        forms = self.br.get_all_forms()
        print forms
        print len(forms)
        form = self.br.get_form('propertyform')
        print form
        # TODO -- working here!
        print token
        



