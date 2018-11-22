from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound


class Templater:
    def __init__(self, config):
        self.config = config
        self.jinja_env = Environment(loader=FileSystemLoader('.'))

    def compile(self, message):
        application = message['application']
        payload = message['payload']

        try:
            templ = self.jinja_env.get_template(
                'templates/applications/%s.html' % (application,))
        except TemplateNotFound:
            templ = self.jinja_env.get_template(
                'templates/default/index.html')
        return templ.render({
            'application': application,
            'app': self.config['binoas']['applications'][application],
            'payload': payload,
            'config': self.config
        })

    def get_subject(self, message):
        application = message['application']
        payload = message['payload']
        queries = [a['query']['description'] for a in payload['alerts']]

        try:
            templ = self.jinja_env.get_template(
                'templates/applications/%s.subject.html' % (application,))
        except TemplateNotFound:
            templ = self.jinja_env.get_template(
                'templates/default/subject.html')
        return templ.render({
            'application': application,
            'app': self.config['binoas']['applications'][application],
            'payload': payload,
            'queries': ', '.join(queries),
            'config': self.config
        })
