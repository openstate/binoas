import importlib
import logging

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from templates.filters import filter_functions


class Templater:
    def __init__(self, config):
        self.config = config
        self.jinja_env = Environment(loader=FileSystemLoader('.'))
        self.jinja_env.filters.update(filter_functions())
        for app in self.config['binoas']['applications'].keys():
            try:
                filters_module = importlib.import_module(
                    'templates.filters.%s' % (app,))
            except ModuleNotFoundError:
                filters_module = None
            try:
                module_filters = getattr(filters_module, 'filter_functions')
            except (TypeError, AttributeError) as e:
                module_filters = None

            if module_filters is not None:
                self.jinja_env.filters.update(module_filters())

    def _render(self, message, default_template, app_template, vars={}):
        application = message['application']
        payload = message['payload']

        app_base_template = 'templates/applications/%s.html' % (application,)
        logging.info('Using template %s (or %s) for app %s' % (
            app_template, app_base_emplate, application,))
        try:
            templ = self.jinja_env.get_template(app_template % (application,))
        except TemplateNotFound:
            templ = self.jinja_env.get_template(default_template)

        is_digest = False
        for a in message['payload']['alerts']:
            is_digest = is_digest or (
                ('frequency' in a['query']) and
                (a['query']['frequency'] is not None) and
                (a['query']['frequency'] != ''))

        ctx_vars = {
            'application': application,
            'app': self.config['binoas']['applications'][application],
            'payload': payload,
            'config': self.config,
            'app_base_template': app_base_template,
            'is_digest': is_digest
        }
        ctx_vars.update(vars)

        return templ.render(ctx_vars)

    def compile(self, message, suffix='index', vars={}):
        logging.info('Compiling for suffix %s' % (suffix,))
        default_template = 'templates/default/%s.html' % (suffix,)
        if suffix == 'index':
            app_template = 'templates/applications/%s.html'
        else:
            app_template = 'templates/applications/%%s.%s.html' % (suffix,)
        return self._render(message, default_template, app_template, vars)

    def get_subject(self, message, suffix='index'):
        queries = [
            a['query']['description'] for a in message['payload']['alerts']]

        if suffix == 'index':
            template = 'subject'
        else:
            template = '%s-subject' % (suffix,)

        return self.compile(message, template, {'queries': queries})
