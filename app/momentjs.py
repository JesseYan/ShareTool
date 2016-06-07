#!venv/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'jesse'

from jinja2 import Markup


class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    # <script>
    #     document.write(moment("2012-12-31T23:55:13 Z").format('LLLL'));
    # </script>

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render(("format(\"%s\")" % fmt))

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")



