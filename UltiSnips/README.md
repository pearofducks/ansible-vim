Generate Snippets Based on Ansible Modules
==========================================

A script to generate `UltiSnips` based on ansible code on the fly.

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
* python **2** only, because Ansible currently doesn't offically support Python 3.

Thanks
------
* Based on (ansible)[https://github.com/ansible/ansible] Awesome Documentation
* Inspired by [bleader/ansible_snippet_generator](https://github.com/bleader/ansible_snippet_generator)
