#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import os
import os.path
import ansible.modules
from ansible.utils.plugin_docs import get_docstring
from ansible.plugins.loader import fragment_loader


def get_documents():
    for root, dirs, files in os.walk(os.path.dirname(ansible.modules.__file__)):
        for f in files:
            if f == '__init__.py' or not f.endswith('py'):
                continue
            documentation = get_docstring(os.path.join(root, f), fragment_loader)[0]
            if documentation is None:
                continue
            yield documentation


def to_snippet(document):
    snippet = []
    if 'options' in document:
        options = document['options'].items()
        if args.sort:
            options = sorted(options, key=lambda x: x[0])

        options = sorted(options, key=lambda x: x[1].get('required', False), reverse=True)

        for index, (name, option) in enumerate(options, 1):
            if 'choices' in option:
                default = option.get('default')
                if isinstance(default, list):
                    prefix = lambda x: '#' if x in default else ''
                    suffix = lambda x: "'%s'" % x if isinstance(x, str) else x
                    value = '[' + ', '.join("%s%s" % (prefix(choice), suffix(choice)) for choice in option['choices'])
                else:
                    prefix = lambda x: '#' if x == default else ''
                    value = '|'.join('%s%s' % (prefix(choice), choice) for choice in option['choices'])
            elif option.get('default') is not None and option['default'] != 'None':
                value = option['default']
                if isinstance(value, bool):
                    value = 'yes' if value else 'no'
            else:
                value = "# " + option.get('description', [''])[0]
            if args.style == 'dictionary':
                delim = ': '
            else:
                delim = '='

            if name == 'free_form':  # special for command/shell
                snippet.append('\t${%d:%s%s%s}' % (index, name, delim, value))
            else:
                snippet.append('\t%s%s${%d:%s}' % (name, delim, index, value))

        # insert a line to seperate required/non-required fields
        for index, (_, option) in enumerate(options):
            if not option.get("required"):
                if index != 0:
                    snippet.insert(index, '')
                break

    if args.style == 'dictionary':
        snippet.insert(0, '%s:' % (document['module']))
    else:
        snippet.insert(0, '%s:%s' % (document['module'], ' >' if len(snippet) else ''))
    snippet.insert(0, 'snippet %s "%s" b' % (document['module'], document['short_description']))
    snippet.append('')
    snippet.append('endsnippet')
    return "\n".join(snippet)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output',
        help='output filename',
        default='ansible.snippets'
    )
    parser.add_argument(
        '--style',
        help='yaml format to use for snippets',
        choices=['multiline', 'dictionary'],
        default='multiline'
    )
    parser.add_argument(
        '--sort',
        help='sort module arguments',
        action='store_true',
        default=False
    )

    args = parser.parse_args()

    with open(args.output, "w") as f:
        f.writelines(["priority -50\n", "\n", "# THIS FILE IS AUTOMATED GENERATED, PLEASE DON'T MODIFY BY HAND\n", "\n"])
        for document in get_documents():
            if 'deprecated' in document:
                continue
            snippet = to_snippet(document)
            if not isinstance(snippet, str):
                # python2 compatibility
                snippet = snippet.encode('utf-8')
            f.write(snippet)
            f.write("\n\n")
