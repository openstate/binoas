import bleach
from bleach.sanitizer import Cleaner
from html5lib.filters.base import Filter


def binoas_about(s):
    return "binoas"


def allow_src(tag, name, value):
    if (tag == 'img') and (name in ('alt', 'src')):
        return True
    if (tag == 'a') and (name in ('href')):
        return True
    if (
        (tag == 'div') and (name in ('class')) and
        (value in ("facebook-external-link", "clearfix"))
    ):
        return True
    return False


def do_html_cleanup(s, result):
    ATTRS = {
        '*': allow_src
    }
    TAGS = ['img', 'a', 'p', 'div']
    cleaner = Cleaner(
        tags=TAGS, attributes=ATTRS, filters=[Filter], strip=True)
    try:
        return cleaner.clean(s).replace(
            '<img ',
            '<img style="border:0;display:block;outline:none;text-decoration:none;width:100%;" '
        ).replace('&amp;nbsp;', '')
    except TypeError:
        return u''


def filter_functions():
    return {
        'binoas': binoas_about,
        'binoas_html_clean': do_html_cleanup
    }
