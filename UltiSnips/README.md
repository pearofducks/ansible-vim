Generate Snippets Based on Ansible Modules
==========================================

A script to generate `UltiSnips` based on ansible code on the fly.

**Note:** Requires Ansible 2.4 or later.

Script parameters
-----------------
There are a couple of optional arguments for the script.

  * --output: Output filename (Default: ansible.snippets)
  * --style: YAML formatting style for snippets
             Choices: multiline (default), dictionary
  * --sort: Whether to sort module arguments (default: no)

For Users
---------
We display option description somewhere, however, there are some special formatters in it.
For your reference, we list them here and you can find them under `/ansible/repo/hacking/module_formatter.py`:

  * I: Italic
  * B: Bold
  * M: Module
  * U: URL
  * C: Const

For Developers
--------------
* `pip install ansible` first

Thanks
------
* Based on (ansible)[https://github.com/ansible/ansible] Awesome Documentation
* Inspired by [bleader/ansible_snippet_generator](https://github.com/bleader/ansible_snippet_generator)
