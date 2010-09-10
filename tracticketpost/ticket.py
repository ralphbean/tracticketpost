from twill.browser import TwillBrowser
import ClientForm

import sys

class Ticket(object):
    """ Represents a new trac ticket """
    _param_defaults = {
        'user' : 'user',
        'passwd' : 'password',
        'realm' : 'example realm',
        'uri' : 'trac.example.com'
    }
    _field_defaults = {
            'summary' : 'new ticket',
            'type' : 'task',
            'priority' : 'major',
            'milestone' : '',
            'component' : '',
            'cc' : '',
            'owner' : '',
    }

    def __init__(self, **kw):
        """ Initialize the ticket.
        
        Possible arguments (with defaults) are:
            user        'user'
            passwd      'password'
            realm       'example realm'
            uri         'trac.example.com'
            summary     'new ticket'
            type        'task'
            priority    'major'
            milestone   ''
            component   ''
            cc          ''
            owner       ''
        """
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


    def submit(self):
        """ Submit the ticket.  Returns the HTTP status code. """

        url = 'https://%s/newticket' % self.params['uri']
        self.br.go(url)
        code = self.br.get_code()
        if code != 200:
            raise Exception, "(Code: %i)  Failed to access %s." % (code, url)

        form = self.br.get_form('propertyform')
        for k, v in self.fields.iteritems():
            k = 'field_%s' % k
            control = form.find_control(k)
            if isinstance(control, ClientForm.TextControl):
                form[k] = v
            elif isinstance(control, ClientForm.SelectControl):
                def get_text(item):
                    if len(item.get_labels()) == 0:
                        return ''
                    return item.get_labels()[0].text

                possible = [ get_text(item) for item in control.get_items() ]

                if v not in possible:
                    raise ValueError, '"%s" not a valid option for %s' % (v, k)

                form[k] = [v]
            else:
                raise ValueError, "Unimplemented '%s'." % k
        self.br.clicked(form, form.find_control('submit'))
        self.br.submit()
        return self.br.get_code()
        



