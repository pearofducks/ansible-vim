## introduction

This is a vim syntax plugin for Ansible 2.0, it supports YAML playbooks, Jinja2 templates, and Ansible's `hosts` files.

- YAML playbooks are detected if:
  - they are in the `group_vars` or `host_vars` folder
  - they are in the `tasks`, `roles`, or `handlers` folder and have either a *.yml* or *.yaml* suffix
  - they are named `playbook.y(a)ml`, `site.y(a)ml`, or `main.y(a)ml`
- Jinja2 templates are detected if they have a *.j2* suffix
- Files named `hosts` will be treated as Ansible hosts files

You can also set the filetype to `ansible`, `ansible_template`, or `ansible_hosts` if auto-detection does not work (e.g. `:set ft=ansible`). **Note**: If you want to detect a custom pattern of your own, you can easily add this in your `.vimrc` using [this method](http://vim.wikia.com/wiki/Change_filetype_based_on_directory_path) - you do not need to fork just to do this! :)

This plugin should be quite reliable, as it sources the original formats and simply modifies the highlights as appropriate. This also enables a focus on simplicity and configurability instead of patching bad syntax detection.

##### examples (with [solarized](https://github.com/altercation/vim-colors-solarized) colorscheme)

Bright (and selective highlight)     |  Dim
:-----------------------------------:|:-------------------------:
![](http://i.imgur.com/whBOZZK.png)  |  ![](http://i.imgur.com/XS0T00e.png)

##### installation

Use your favorite plugin manager, or try [vim-plug](https://github.com/junegunn/vim-plug) if you're looking for a really nice one!

**vim-plug:** `Plug 'pearofducks/ansible-vim'`

**vundle:** `Plugin 'pearofducks/ansible-vim'`

**pathogen:** `git clone https://github.com/pearofducks/ansible-vim ~/.vim/bundle/ansible-vim`

## options

##### g:ansible_extra_syntaxes
`let g:ansible_extra_syntaxes = "sh.vim ruby.vim"`

The space-separated options specified must be the actual syntax files, not the filetype - typically these are in something like `/usr/share/vim/syntax`. For example Bash is not `bash.vim` but seems to live in `sh.vim`.

This flag enables extra syntaxes to be loaded for Jinja2 templates. If you frequently work with specific filetypes in Ansible, this can help get highlighting in those files.

This will *always* load these syntaxes for *all* .j2 files, and should be considered a bit of a (temporary?) hack/workaround.

##### g:ansible_attribute_highlight
`let g:ansible_attribute_highlight = "ob"`

Ansible modules use a `key=value` format for specifying module-attributes in playbooks. This highlights those as specified. This highlight option is also used when highlighting key/value pairs in `hosts` files.

Available flags (bold are defaults):

- **a**: highlight *all* instances of `key=`
- o: highlight *only* instances of `key=` found on newlines
- **d**: *dim* the instances of `key=` found
- b: *brighten* the instances of `key=` found
- n: turn this highlight off completely

##### g:ansible_name_highlight
`let g:ansible_name_highlight = 'd'`

Ansible modules commonly start with a `name:` key for self-documentation of playbooks. This option enables/changes highlight of this.

Available flags (this feature is off by default):

- d: *dim* the instances of `name:` found
- b: *brighten* the instances of `name:` found

##### g:ansible_extra_keywords_highlight
`let g:ansible_extra_keywords_highlight = 1`

*Note:* This option is enabled when set, and disabled when not set.

Highlight the following additional keywords in playbooks: `register always_run changed_when failed_when no_log args vars delegate_to ignore_errors`

By default we only highlight: `include until retries delay when only_if become become_user block rescue always notify`

## bugs, suggestions/requests, & contributions

##### bugs

It's unlikely that there will be bugs in highlighting that don't exist in the core format. Where appropriate these will be fixed in this plugin, but if the problem is with the original syntax we should probably focus on fixing that instead.

Indenting a full document - e.g with `gg=G` - will not be supported and is not a goal of this plugin (unless someone else develops it!). Please do not file a bug report on this.

##### suggestions/requests

Suggestions for improvements are welcome, pull-requests with completed features even more so. :)

##### contributions

Thanks to:

- The developers of `salt-vim` for parts of the original YAML implementation this is based on
