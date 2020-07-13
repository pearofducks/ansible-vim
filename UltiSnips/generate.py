#!/usr/bin/env python3
import argparse
import os
import os.path
import ansible.modules
from ansible.utils.plugin_docs import get_docstring
from ansible.plugins.loader import fragment_loader
from typing import Any, List


OUTPUT_FILENAME = "ansible.snippets"
OUTPUT_STYLE = ["multiline", "dictionary"]
HEADER = [
    "# NOTE: This file is auto-generated. Modifications may be overwritten.",
    "priority -50",
]
MAX_DESCRIPTION_LENGTH = 512


def get_files() -> List[str]:
    """Return the sorted list of all module files that ansible provides

    Returns
    -------
    List[str]
        A list of strings representing the Python module files provided by
        Ansible
    """

    file_names: List[str] = []
    for root, dirs, files in os.walk(os.path.dirname(ansible.modules.__file__)):
        file_names += [
            f"{root}/{file_name}"
            for file_name in files
            if file_name.endswith(".py") and not file_name.startswith("__init__")
        ]

    return sorted(file_names)


def get_docstrings(file_names: List[str]) -> List[Any]:
    """Extract and return a list of docstring information from a list of files

    Parameters
    ----------
    file_names: List[str]
        A list of strings representing file names

    Returns
    -------
    List[Any]
        A list of AnsibleMapping objects, representing docstring information
        (in dict form), excluding those that are marked as deprecated.

    """

    docstrings: List[Any] = []
    docstrings += [
        get_docstring(file_name, fragment_loader)[0] for file_name in file_names
    ]
    return [
        docstring
        for docstring in docstrings
        if docstring and not docstring.get("deprecated")
    ]


def escape_strings(escapist: str) -> str:
    """Escapes strings as required for ultisnips snippets

    Escapes instances of \\, `, {, }, $

    Parameters
    ----------
    escapist: str
        A string to apply string replacement on

    Returns
    -------
    str
        The input string with all defined replacements applied
    """

    return (
        escapist.replace("\\", "\\\\")
        .replace("`", "\`")
        .replace("{", "\{")
        .replace("}", "\}")
        .replace("$", "\$")
        .replace("\"", "'")
    )


def option_data_to_snippet_completion(option_data: Any) -> str:
    """Convert Ansible option info into a string used for ultisnip completion

    Converts data about an Ansible module option (retrieved from an
    AnsibleMapping object) into a formatted string that can be used within an
    UltiSnip macro.

    Parameters
    ----------
    option_data: Any
        The option parameters

    Returns
    -------
    str
        A string representing one formatted option parameter
    """

    # join descriptions that are provided as lists and crop them
    description = escape_strings(
        "".join(option_data.get("description"))[0:MAX_DESCRIPTION_LENGTH]
    )
    default = option_data.get("default")
    choices = option_data.get("choices")
    option_type = option_data.get("type")

    # if the option is of type "bool" return "yes" or "no"
    if option_type and "bool" in option_type:
        if default in [True, "True", "true", "yes"]:
            return "true"
        if default in [False, "False", "false", "no"]:
            return "false"

    # if there is no default and no choices, return the description
    if not choices and default is None:
        return f"# {description}"

    # if there is a default but no choices return the default as string
    if default is not None and not choices:
        if len(str(default)) == 0:
            return '""'
        else:
            if isinstance(default, str) and "\\" in default:
                return f'"{escape_strings(str(default))}"'
            elif isinstance(default, str):
                return escape_strings(str(default))
            else:
                return default

    # if there is a default and there are choices return the list of choices
    # with the default prefixed with #
    if default is not None and choices:
        if isinstance(default, list):
            # prefix default choice(s)
            prefixed_choices = [
                f"#{choice}" if choice in default else f"{choice}" for choice in choices
            ]
            return str(prefixed_choices)
        else:
            # prefix default choice
            prefixed_choices = [
                f"#{choice}" if str(choice) == str(default) else f"{choice}"
                for choice in choices
            ]
            return "|".join(prefixed_choices)

    # if there are choices but no default, return the choices as pipe separated
    # list
    if choices and default is None:
        return "|".join([str(choice) for choice in choices])

    # as fallback return empty string
    return ""


def module_options_to_snippet_options(module_options: Any) -> List[str]:
    """Convert module options to UltiSnips snippet options

    Parameters
    ----------
    module_options: Any
        The "options" attribute of an AnsibleMapping object

    Returns
    -------
    List[str]
        A list of strings representing converted options
    """

    options: List[str] = []
    delimiter = ": " if args.style == "dictionary" else "="

    if not module_options:
        return options

    # order by option name
    module_options = sorted(module_options.items(), key=lambda x: x[0])
    # order by "required" attribute
    module_options = sorted(
        module_options, key=lambda x: x[1].get("required", False), reverse=True
    )

    # insert an empty option above the list of non-required options
    for index, (_, option) in enumerate(module_options):
        if not option.get("required"):
            if index != 0:
                module_options.insert(index, (None, None))
            break

    for index, (name, option_data) in enumerate(module_options, start=1):
        # insert a line to seperate required/non-required options
        if not name and not option_data:
            options += [""]
        else:
            # the free_form option in some modules are special
            if name == "free_form":
                options += [
                    f"\t${{{index}:{name}{delimiter}{option_data_to_snippet_completion(option_data)}}}"
                ]
            else:
                options += [
                    f"\t{name}{delimiter}${{{index}:{option_data_to_snippet_completion(option_data)}}}"
                ]

    return options


def convert_docstring_to_snippet(docstring: Any) -> List[str]:
    """Converts data about an Ansible module into an UltiSnips snippet string

    Parameters
    ----------
    docstring: Any
        An AnsibleMapping object representing the docstring for an Ansible
        module

    Returns
    -------
    str
        A string representing an ultisnips compatible snippet of an Ansible
        module
    """

    snippet: List[str] = []
    snippet_options = "b"
    module_name = docstring["module"]
    module_short_description = docstring["short_description"]

    snippet += [f'snippet {module_name} "{escape_strings(module_short_description)}" {snippet_options}']
    if args.style == "dictionary":
        snippet += [f"{module_name}:"]
    else:
        snippet += [f"{module_name}:{' >' if docstring.get('options') else ''}"]
    module_options = module_options_to_snippet_options(docstring.get("options"))
    snippet += module_options
    snippet += ["endsnippet"]

    return snippet


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        help=f"Output filename (default: {OUTPUT_FILENAME})",
        default=OUTPUT_FILENAME,
    )
    parser.add_argument(
        "--style",
        help=f"YAML format used for snippets (default: {OUTPUT_STYLE[0]})",
        choices=OUTPUT_STYLE,
        default=OUTPUT_STYLE[0],
    )
    args = parser.parse_args()

    docstrings = get_docstrings(get_files())
    with open(args.output, "w") as f:
        f.writelines(f"{header}\n" for header in HEADER)
        for docstring in docstrings:
            f.writelines(
                f"{line}\n" for line in convert_docstring_to_snippet(docstring)
            )
