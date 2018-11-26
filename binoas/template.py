from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound


class Templater:
    def __init__(self, config):
        self.config = config
        self.jinja_env = Environment(loader=FileSystemLoader('.'))

    def _render(self, message, default_template, app_template, vars={}):
        application = message['application']
        payload = message['payload']

        try:
            templ = self.jinja_env.get_template(app_template % (application,))
        except TemplateNotFound:
            templ = self.jinja_env.get_template(default_template)

        ctx_vars = {
            'application': application,
            'app': self.config['binoas']['applications'][application],
            'payload': payload,
            'config': self.config
        }
        ctx_vars.update(vars)

        return templ.render(ctx_vars)

    def compile(self, message, suffix='index', vars={}):
        default_template = 'templates/default/%s.html' % (suffix,)
        if suffix == 'index':
            app_template = 'templates/applications/%s.html'
        else:
            app_template = 'templates/applications/%%s.%s.html' % (suffix,)
        return self._render(message, default_template, app_template, vars)

    def get_subject(self, message, suffix='index'):
        queries = [
            a['query']['description'] for a in message['payload']['alerts']]

        if suffix != 'index':
            template = 'subject'
        else:
            template = '%s-subject' % (suffix,)

        return self.compile(message, template, {'queries': queries})
