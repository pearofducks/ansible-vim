## introduction

This is a vim syntax plugin for Ansible 2.x, it supports YAML playbooks, Jinja2 templates, and Ansible's `hosts` files.

- YAML playbooks are detected if:
  - they are in the `group_vars` or `host_vars` folder
  - they are in the `tasks`, `roles`, or `handlers` folder and have either a *.yml* or *.yaml* suffix
  - they are named `playbook.y(a)ml`, `site.y(a)ml`, or `main.y(a)ml`
- Jinja2 templates are detected if they have a *.j2* suffix
- Files named `hosts` will be treated as Ansible hosts files

You can also set the filetype to `yaml.ansible`, `*.jinja2`, or `ansible_hosts` if auto-detection does not work (e.g. `:set ft=yaml.ansible` or `:set ft=ruby.jinja2`). **Note**: If you want to detect a custom pattern of your own, you can easily add this in your `.vimrc` using something like this:

```vim
au BufRead,BufNewFile */playbooks/*.yml set filetype=yaml.ansible
```

If you want to override the default file type detection you can easily do this in your `.vimrc`. For example if you use YAML syntax for `hosts` include something like this:

```vim
augroup ansible_vim_fthosts
  autocmd!
  autocmd BufNewFile,BufRead hosts setfiletype yaml.ansible
augroup END
```

This plugin should be quite reliable, as it sources the original formats and simply modifies the highlights as appropriate. This also enables a focus on simplicity and configurability instead of patching bad syntax detection.

##### examples (with [solarized](https://github.com/altercation/vim-colors-solarized) colorscheme)

Bright (and selective highlight)     |  Dim
:-----------------------------------:|:-------------------------:
![](http://i.imgur.com/whBOZZK.png)  |  ![](http://i.imgur.com/XS0T00e.png)

##### installation

Use your favorite plugin manager, or try [vim-plug](https://github.com/junegunn/vim-plug) if you're looking for a really nice one!

**vim-plug:** `Plug 'pearofducks/ansible-vim'`

**vim-plug with post-update hook:** `Plug 'pearofducks/ansible-vim', { 'do':
'./UltiSnips/generate.sh' }`

*Note: Because of Ansible API changes, `generate.sh` may require the latest (or near-latest) version of Ansible.*

*Note2: `generate.sh` can receive some parameters, for more info see its [Readme](https://github.com/pearofducks/ansible-vim/tree/master/UltiSnips#script-parameters)*

**vundle:** `Plugin 'pearofducks/ansible-vim'`

**pathogen:** `git clone https://github.com/pearofducks/ansible-vim ~/.vim/bundle/ansible-vim`

**Arch Linux:** Package [vim-ansible](https://www.archlinux.org/packages/community/any/vim-ansible/) is available in the *community* repository.

**Fedora:** The [vim-ansible](https://src.fedoraproject.org/rpms/vim-ansible) package is available in the default repository.

**RHEL/CentOS:** The [vim-ansible](https://src.fedoraproject.org/rpms/vim-ansible) package is available in the [EPEL](https://fedoraproject.org/wiki/EPEL) repository.

## options

##### g:ansible_unindent_after_newline

`let g:ansible_unindent_after_newline = 1`

When this variable is set, indentation will completely reset (unindent to column 0) after two newlines in insert-mode. The normal behavior of YAML is to always keep the previous indentation, even across multiple newlines with no content.

##### g:ansible_yamlKeyName

`let g:ansible_yamlKeyName = 'yamlKey'`

This option exists to provide additional compatibility with [stephpy/vim-yaml](https://github.com/stephpy/vim-yaml).

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

Highlight the following additional keywords: `become become_exe become_flags become_method become_user become_pass prompt_l10n debugger always_run check_mode diff no_log args tags force_handlers vars vars_files vars_prompt delegate_facts delegate_to any_errors_fatal ignore_errors ignore_unreachable max_fail_percentage connection hosts port remote_user module_defaults environment fact_path gather_facts gather_subset gather_timeout async poll throttle timeout order run_once serial strategy`.

By default we only highlight: `include include_role include_tasks include_vars import_role import_playbook import_tasks when changed_when failed_when block rescue always notify listen register action local_action post_tasks pre_tasks tasks handlers roles collections` and loop keywords `with_.+`, `loop`, `loop_control`, `until`, `retries`, `delay`.

##### g:ansible_extra_keywords_highlight_group
`let g:ansible_extra_keywords_highlight_group = 'Statement'`

Accepts any syntax group name from `:help E669` - e.g. _Comment_, _Constant_, _Identifier_

*Note:* Defaults to 'Structure' when not set.

##### g:ansible_normal_keywords_highlight
`let g:ansible_normal_keywords_highlight = 'Constant'`

Accepts any syntax group name from `:help E669` - e.g. _Comment_, _Constant_, _Identifier_

*Note:* Defaults to 'Statement' when not set.

This option change the highlight of the following common keywords: `include include_role include_tasks include_vars import_role import_playbook import_tasks when changed_when failed_when block rescue always notify listen register action local_action post_tasks pre_tasks tasks handlers roles collections`.

##### g:ansible_loop_keywords_highlight
`let g:ansible_loop_keywords_highlight = 'Constant'`

Accepts any syntax group-name from `:help E669` - e.g. _Comment_, _Constant_, _Identifier_

*Note:* Defaults to 'Statement' when not set.

This option changes the highlight of all `with_.+`, `loop`, `loop_control`, `until`, `retries` and `delay` keywords.

##### g:ansible_template_syntaxes
`let g:ansible_template_syntaxes = { '*.rb.j2': 'ruby' }`

Accepts a dictionary in the form of `'regex-for-file': 'filetype'`.
- _regex-for-file_ will receive the full filepath, so directory matching can be done.
- _filetype_ is the root filetype to be applied, `jinja2` will be automatically appended

All files ending in `*.j2` that aren't matched will simply get the `jinja2` filetype.

##### g:ansible_ftdetect_filename_regex
`let g:ansible_ftdetect_filename_regex = '\v(playbook|site|main|local|requirements)\.ya?ml$'`

Accepts a regex string that is used to match the filename to determine if the file should use the Ansible filetype

Can be used to avoid clashes with other files that are named the same - e.g. main.yaml used in github workflows by removing `main` from the regex

## goto role under cursor (similar to gf)

This behavior is not supported out of the box, but you can use [this snippet](https://gist.github.com/mtyurt/3529a999af675a0aff00eb14ab1fdde3) in your vimrc.

You'll then be able to go to a role's definition with `<leader>gr`.

## bugs, suggestions/requests, & contributions

##### bugs

It's unlikely that there will be bugs in highlighting that don't exist in the core format. Where appropriate these will be fixed in this plugin, but if the problem is with the original syntax we should probably focus on fixing that instead.

Indenting a full document - e.g with `gg=G` - will not be supported and is not a goal of this plugin (unless someone else develops it!). Please do not file a bug report on this.

##### suggestions/requests

Suggestions for improvements are welcome, pull-requests with completed features even more so. :)
