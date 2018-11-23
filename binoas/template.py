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

    def compile(self, message):
        return self._render(
            message, 'templates/default/index.html',
            'templates/applications/%s.html')

    def compile_welcome(self, message):
        return self._render(
            message, 'templates/default/welcome.html',
            'templates/applications/%s.welcome.html')

    def get_subject(self, message):
        queries = [
            a['query']['description'] for a in message['payload']['alerts']]

        return self._render(
            message, 'templates/default/subject.html',
            'templates/applications/%s.subject.html', {'queries': queries})
