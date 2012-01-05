from twill.browser import TwillBrowser
from BeautifulSoup import BeautifulSoup

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
            'description' : '(no description provided)',
            'keywords' : '',
            'type' : 'task',
            'priority' : 'major',
            'milestone' : '',
            'component' : '',
            'cc' : '',
            'owner' : '',
    }

    def __init__(self, **kw):
        """ Set up a ticket and connection

        Possible arguments (with defaults) are:

            user        'user'
            passwd      'password'
            realm       'example realm'
            uri         'trac.example.com'
        """
        self.params = self._param_defaults
        for k, v in kw.iteritems():
            if not k in self._param_defaults.keys():
                raise ValueError, "Unexpected keyword '%s=%s'"%(str(k),str(v))
            if k in self.params:
                self.params[k] = v
            else:
                raise ValueError, "WTF... '%s=%s'" % (str(k), str(v))

        # Setup our connection
        self.br = TwillBrowser()
        self.br.creds.add_password(*[
            self.params[k] for k in ['realm', 'uri', 'user', 'passwd']
        ])

        # Test our connection
        url = 'https://%s/' % self.params['uri']
        self.br.go(url)
        code = self.br.get_code()
        if code != 200:
            raise Exception, "(Code: %i)  Failed to access %s." % (code, url)

        # signifies that this ticket is in sync with what's in the trac db
        self._dirty = False
        # signifies that this ticket DNE in the trac db as far as we know
        self.id = None

    def update(self, **kw):
        """ Fill in ticket values.

        Possible arguments (with defaults) are:

            summary     'new ticket'
            description '(no description provided)'
            keywords    ''
            type        'task'
            priority    'major'
            milestone   ''
            component   ''
            cc          ''
            owner       ''
        """
        self.fields = self._field_defaults
        for k, v in kw.iteritems():
            if not k in self._field_defaults.keys():
                raise ValueError, "Unexpected keyword '%s=%s'"%(str(k),str(v))

            if k in self.fields:
                if self.fields[k] == v:
                    pass
                else:
                    self.fields[k] = v
                    self._dirty = True
            else:
                raise ValueError, "WTF... '%s=%s'" % (str(k), str(v))

    def search(self, term, unique=True):
        """ Retrieve a ticket from trac by ID and populate my fields """
        url = 'https://%s/search' % self.params['uri']
        self.br.go(url)
        code = self.br.get_code()
        if code != 200:
            raise Exception, "(Code: %i)  Failed to access %s." % (code, url)

        form = self.br.get_form('fullsearch')
        for checkbox in ['wiki', 'milestone', 'changeset']:
            form.find_control(checkbox).checked = False
        form['q'] = term
        self.br.clicked(form, form.find_control(type='submit'))
        self.br.submit()
        code = self.br.get_code()
        if code != 200:
            raise Exception, "(Code: %i)  Failed to search." % code

        soup = BeautifulSoup(self.br.get_html())
        results = soup.findAll(id='results')[0]
        results = soup.findAll(id='results')[0].findAll(name='dt')
        if len(results) < 1:
            raise Exception, "No results for term '%s'" % term

        if unique and len(results) > 1:
            raise Exception, "More than one results for '%s' found." % term

        loc = results[0].findAll(name='a')[0]['href']
        tid = loc.split('/')[-1]
        return int(tid)

    def flush(self):
        """ Flush changes to this ticket to the trac DB via http POSTs """
        if not self._dirty:
            raise ValueError, "No changes to ticket.  Can't flush."

        if not self.id:
            raise ValueError, "Ticket DNE in trac db yet.  Use submit."

        raise NotImplementedError, "Gotta write this method first."

    def submit(self):
        """ Submit a new ticket.  Returns the HTTP status code. """

        if not self._dirty:
            raise ValueError, "Ticket has not been modified."

        if self.id:
            raise ValueError, "Cannot submit already submitted ticket.  Use flush to push modifications to trac."

        url = 'https://%s/newticket' % self.params['uri']
        self.br.go(url)
        code = self.br.get_code()
        if code != 200:
            raise Exception, "(Code: %i)  Failed to access %s." % (code, url)

        form = self.br.get_form('propertyform')
        for k, v in self.fields.iteritems():
            k = 'field_%s' % k

            try:
                control = form.find_control(k)
            except Exception:
                print "Failed on", k, v
                continue

            if control.is_of_kind('text'):
                form[k] = v
            elif control.is_of_kind('list'):
                def get_text(item):
                    if len(item.get_labels()) == 0:
                        return ''
                    return item.get_labels()[0].text

                possible = [ get_text(item) for item in control.get_items() ]

                if v not in possible:
                    raise ValueError, '"%s" not a valid option for %s (%s)' % (
                        v, k, str(possible))

                form[k] = [v]
            else:
                raise ValueError, "Unimplemented '%s'." % k
        self.br.clicked(form, form.find_control('submit'))
        self.br.submit()

        code = self.br.get_code()
        if code == 200:
            self._dirty = False

        # TODO -- get the ticket id and save it!!!!!!!
        print "TODO -- get the ticket id and save it!!!!"

        return code
