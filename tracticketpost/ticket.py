from twill.browser import TwillBrowser
from BeautifulSoup import BeautifulSoup

import sys

class Ticket(object):
    _param_defaults = {
        'username' : 'user',
        'password' : 'password',
        'baseurl' : 'trac.example.com'
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


    def _get_form_token(self):
        print self.params
        self.br.go('https://%s/newticket' % self.params['baseurl'])
        soup = BeautifulSoup(self.br.get_html())
        tags = soup.findAll(name='__FORM_TOKEN')
        print tags
        print len(tags)
        sys.exit(0)



