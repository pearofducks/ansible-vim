#!/usr/bin/env python3
import argparse
import os
import os.path
import ansible
from packaging import version
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
ANSIBLE_VERSION = ansible.release.__version__


def get_files_builtin() -> List[str]:
    """Return the sorted list of all module files that ansible provides with the ansible package

    Returns
    -------
    List[str]
        A list of strings representing the Python module files provided by
        Ansible
    """

    file_names: List[str] = []
    for root, dirs, files in os.walk(os.path.dirname(ansible.modules.__file__)):
        files_without_symlinks = []
        for f in files:
            if not os.path.islink(os.path.join(root, f)):
                files_without_symlinks.append(f)
        file_names += [
            f"{root}/{file_name}"
            for file_name in files_without_symlinks
            if file_name.endswith(".py") and not file_name.startswith("__init__")
        ]

    return sorted(file_names)

def get_files_user() -> List[str]:
    """Return the sorted list of all module files provided by collections installed in the
    user home folder ~/.ansible/collections/

    Returns
    -------
    List[str]
        A list of strings representing the Python module files installed in ~/.ansible/collections/
    """

    file_names: List[str] = []
    for root, dirs, files in os.walk(os.path.expanduser('~/.ansible/collections/ansible_collections/')):
        files_without_symlinks = []
        for f in files:
            if not os.path.islink(os.path.join(root, f)):
                files_without_symlinks.append(f)
        file_names += [
            f"{root}/{file_name}"
            for file_name in files_without_symlinks
            if file_name.endswith(".py") and not file_name.startswith("__init__") and "plugins/modules" in root
        ]

    return sorted(file_names)


def get_module_docstring(file_path: str) -> Any:
    """Extract and return docstring information from a module file

    Parameters
    ----------
    file_names: file_path[str]
        string representing module file

    Returns
    -------
    Any
        An AnsibleMapping object, representing docstring information
        (in dict form), excluding those that are marked as deprecated.

    """

    docstring = get_docstring(file_path, fragment_loader)[0]

    if docstring and not docstring.get("deprecated"):
        return docstring


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
                .replace("`", r"\`")
                .replace("{", r"\{")
                .replace("}", r"\}")
                .replace("$", r"\$")
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
    if not choices and default is None and not args.no_description:
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
        if not option.get("required") and not args.comment_non_required:
            if index != 0:
                module_options.insert(index, (None, None))
            break

    for index, (name, option_data) in enumerate(module_options, start=1):
        # insert a line to separate required/non-required options
        if not name and not option_data:
            options += [""]
        else:
            # set comment character for non-required options
            if not option_data.get("required") and args.comment_non_required:
                comment = "#"
            else:
                comment = ""
            # the free_form option in some modules are special
            if name == "free_form":
                options += [
                    f"\t{comment}${{{index}:{name}{delimiter}{option_data_to_snippet_completion(option_data)}}}"
                ]
            else:
                options += [
                    f"\t{comment}{name}{delimiter}${{{index}:{option_data_to_snippet_completion(option_data)}}}"
                ]

    return options


def convert_docstring_to_snippet(convert_docstring: Any, collection_name) -> List[str]:
    """Converts data about an Ansible module into an UltiSnips snippet string

    Parameters
    ----------
    convert_docstring: Any
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
    if "module" in convert_docstring.keys():
        module_name = convert_docstring["module"]
        module_short_description = convert_docstring["short_description"]

        # use only the module name if ansible version < 2.10
        if version.parse(ANSIBLE_VERSION) < version.parse("2.10"):
            snippet_module_name = f"{module_name}:"
        # use FQCN if ansible version is 2.10 or higher
        else:
            snippet_module_name = f"{collection_name}.{module_name}:"

        snippet += [f'snippet {module_name} "{escape_strings(module_short_description)}" {snippet_options}']
        if args.style == "dictionary":
            snippet += [f"{snippet_module_name}"]
        else:
            snippet += [f"{snippet_module_name}:{' >' if convert_docstring.get('options') else ''}"]
        module_options = module_options_to_snippet_options(convert_docstring.get("options"))
        snippet += module_options
        snippet += ["endsnippet"]

    return snippet

def get_collection_name(filepath:str) -> str:
    """ Returns the collection name for a full file path """

    path_splitted = filepath.split('/')

    collection_top_folder_index = path_splitted.index('ansible_collections')
    collection_namespace = path_splitted[collection_top_folder_index + 1]
    collection_name = path_splitted[collection_top_folder_index + 2]

    #  print(f"{collection_namespace}.{collection_name}")
    return f"{collection_namespace}.{collection_name}"


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
    parser.add_argument(
        '--user',
        help="Include user modules",
        action="store_true",
        default=False
    )
    parser.add_argument(
        '--no-description',
        help="Remove options description",
        action="store_true",
        default=False
    )
    parser.add_argument(
        '--comment-non-required',
        help="Comment non-required options",
        action="store_true",
        default=False
    )
    args = parser.parse_args()


    if version.parse(ANSIBLE_VERSION) < version.parse("2.10"):
        print(f"ansible version {ANSIBLE_VERSION} doesn't support FQCN")
        print("generated snippets will only use the module name e.g. 'yum' instead of 'ansible.builtin.yum'")
    else:
        print(f"ansible version {ANSIBLE_VERSION} supports using FQCN")
        print("Generated snippets will use FQCN e.g. 'ansible.builtin.yum' instead of 'yum'")
        print("Still, you only need to type 'yum' to trigger the snippet")

    modules_docstrings = []

    builtin_modules_paths = get_files_builtin()
    for f in builtin_modules_paths:
        docstring_builtin = get_module_docstring(f)
        if docstring_builtin and docstring_builtin not in modules_docstrings:
            docstring_builtin['collection_name'] = "ansible.builtin"
            modules_docstrings.append(docstring_builtin)

    if args.user:
        user_modules_paths = get_files_user()
        for f in user_modules_paths:
            docstring_user = get_module_docstring(f)
            if docstring_user and docstring_user not in modules_docstrings:
                collection_name = get_collection_name(f)
                docstring_user['collection_name'] = collection_name
                modules_docstrings.append(docstring_user)

    with open(args.output, "w") as f:
        f.writelines(f"{header}\n" for header in HEADER)
        for docstring in modules_docstrings:
            f.writelines(
                f"{line}\n" for line in convert_docstring_to_snippet(docstring, docstring.get("collection_name"))
            )
