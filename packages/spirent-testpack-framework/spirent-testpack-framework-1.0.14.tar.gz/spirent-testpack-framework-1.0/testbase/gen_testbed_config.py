#!/usr/bin/env python
"""
Generate the final testbed file
"""
import os
import sys
import yaml
import jinja2
from jinja2 import TemplateAssertionError
from jinja2.ext import Extension
from jinja2.nodes import CallBlock, Const


#
# http://xion.io/post/code/jinja-custom-errors.html
#
class ErrorExtension(Extension):
    """Extension providing {% error %} tag, allowing to raise errors
    directly from a Jinja template.
    """
    tags = frozenset(['error'])

    def parse(self, parser):
        """Parse the {% error %} tag, returning an AST node."""
        tag = next(parser.stream)
        message = parser.parse_expression()

        node = CallBlock(
            self.call_method('_exec_error', [message, Const(tag.lineno)]),
            [], [], [])
        node.set_lineno(tag.lineno)
        return node

    def _exec_error(self, message, lineno, caller):
        """Execute the {% error %} statement, raising an exception."""
        raise TemplateUserError(message, lineno)


class TemplateUserError(TemplateAssertionError):
    """Exception raised in the template through the use of {% error %} tag."""


def load_config(config):
    """Load yaml file"""
    with open(config) as file_handle:
        return yaml.load(file_handle, Loader=yaml.FullLoader)


def load_template(template_file):
    """Load jinja2  template"""
    if template_file is None:
        return jinja2.Template(
            sys.stdin.read(),
            extensions=[ErrorExtension],
            undefined=jinja2.StrictUndefined)

    path, filename = os.path.split(template_file)
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path),
        extensions=[ErrorExtension],
        undefined=jinja2.StrictUndefined)
    return env.get_template(filename)

def generate(testbed_lab_config_file, testbed_template_file, testbed_id, outfile):
    if not os.path.exists(testbed_lab_config_file):
        sys.exit("Missing config file: {0}".format(testbed_lab_config_file))

    if not os.path.exists(testbed_template_file):
        sys.exit("Missing template file: {0}".format(testbed_template_file))

    # Read JSON config
    variables = load_config(testbed_lab_config_file)

    # Write to file
    template = load_template(testbed_template_file)
    file = open(outfile, "w")
    file.write(template.render(variables[testbed_id]))
    file.write("\n")
    file.close()
