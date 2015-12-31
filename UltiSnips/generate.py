#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import os.path
import ansible.modules
from ansible.utils.module_docs import get_docstring


def get_documents():
    for root, dirs, files in os.walk(os.path.dirname(ansible.modules.__file__)):
        for f in files:
            if f == '__init__.py':
                continue
            if f.endswith('.pyc'):
                continue
            if f.endswith('.ps1'):
                continue
            documentation = get_docstring(os.path.join(root, f))[0]
            if documentation is None:
                continue
            yield documentation


def to_snippet(document):
    snippet = []
    if 'options' in document:
        options = sorted(document['options'].items(), key=lambda x: x[1].get("required", False), reverse=True)
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
            if name == 'free_form':  # special for command/shell
                snippet.append('\t${%d:%s=%s}' % (index, name, value))
            else:
                snippet.append('\t%s=${%d:%s}' % (name, index, value))

        # insert a line to seperate required/non-required field
        for index, (_, option) in enumerate(options):
            if option.get("required", False) is False:
                if index != 0:
                    snippet.insert(index, '')
                break

    snippet.insert(0, '%s:%s' % (document['module'], ' >' if len(snippet) else ''))
    snippet.insert(0, 'snippet %s "%s" b' % (document['module'], document['short_description']))
    snippet.append('')
    snippet.append('endsnippet')
    return "\n".join(snippet)


if __name__ == "__main__":
    with open("ansible.snippets", "w") as f:
        f.writelines(["priority -50\n", "\n", "# THIS FILE IS AUTOMATED GENERATED, PLEASE DON'T MODIFY BY HAND\n", "\n"])
        for document in get_documents():
            if 'deprecated' in document:
                continue
            f.write(to_snippet(document).encode('utf-8'))
            f.write("\n\n")
