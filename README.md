## upcoming changes in v2

Near the end of March 2018, this plugin will update to v2 and will have a few minor breaking changes. This branch can be previewed at `v2` and should be stable.

- The filetype for playbooks will be set to `yaml.ansible`.
  - Using a compound filetype here improves compatibility with some other plugins, and is a bit more honest about the filetypes being used. We _could_ set it to `yaml.jinja2.ansible`, if there are strong opinions on this please open an issue.
  - This _only_ breaks setups using vim plugin on-demand loading features — e.g. `{ 'for': 'ansible' }` in vim-plug. Otherwise this change should not break anything.
- `g:ansible_extra_syntaxes` will be deprecated in favor of `g:ansible_template_syntaxes` — which will use conditional compound filetypes, instead of sourcing all filetypes listed and hiding them under `ansible_template`.
  - While this is a complete deprecation of one setting, the new functionality is significantly better all around and should support the same use-cases.
  - Example: a ruby+ansible-template will have a filetype of `ruby.jinja2` instead of `ansible_template`
  
One non-breaking change will also be added, this plugin will gain additional compatibility with _stephpy/vim-yaml_ — syntax highlights will be improved when using this plugin.

## introduction

This is a vim syntax plugin for Ansible 2.0, it supports YAML playbooks, Jinja2 templates, and Ansible's `hosts` files.

- YAML playbooks are detected if:
  - they are in the `group_vars` or `host_vars` folder
  - they are in the `tasks`, `roles`, or `handlers` folder and have either a *.yml* or *.yaml* suffix
  - they are named `playbook.y(a)ml`, `site.y(a)ml`, or `main.y(a)ml`
- Jinja2 templates are detected if they have a *.j2* suffix
- Files named `hosts` will be treated as Ansible hosts files

You can also set the filetype to `ansible`, `ansible_template`, or `ansible_hosts` if auto-detection does not work (e.g. `:set ft=ansible`). **Note**: If you want to detect a custom pattern of your own, you can easily add this in your `.vimrc` using something like this:

```vim
au BufRead,BufNewFile */playbooks/*.yml set filetype=ansible
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
'cd ./UltiSnips; python2 generate.py' }`

*Note: `generate.py` requires Ansible 2.4 or later.*

**vundle:** `Plugin 'pearofducks/ansible-vim'`

**pathogen:** `git clone https://github.com/pearofducks/ansible-vim ~/.vim/bundle/ansible-vim`

**Arch Linux:** Package [ansible-vim-git](https://aur.archlinux.org/packages/ansible-vim-git/) available on AUR

## options

##### g:ansible_unindent_after_newline

`let g:ansible_unindent_after_newline = 1`

When this variable is set, indentation will completely reset (unindent to column 0) after two newlines in insert-mode. The normal behavior of YAML is to always keep the previous indentation, even across multiple newlines with no content.

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

##### g:ansible_normal_keywords_highlight
`let g:ansible_normal_keywords_highlight = 'Constant'`

This option accepts the first line of each option in `:help E669` - thus the first 3 options are _Comment_, _Constant_, and _Identifier_

*Note:* Defaults to 'Statement' when not set.

This controls the highlight of the following common keywords in playbooks: `include until retries delay when only_if become become_user block rescue always notify`

##### g:ansible_with_keywords_highlight
`let g:ansible_with_keywords_highlight = 'Constant'`

This option accepts the first line of each group in `:help E669` - thus the first 3 are _Comment_, _Constant_, and _Identifier_

*Note:* Defaults to 'Statement' when not set.

This controls the highlight of all `with_.+` keywords in playbooks.

## bugs, suggestions/requests, & contributions

##### bugs

It's unlikely that there will be bugs in highlighting that don't exist in the core format. Where appropriate these will be fixed in this plugin, but if the problem is with the original syntax we should probably focus on fixing that instead.

Indenting a full document - e.g with `gg=G` - will not be supported and is not a goal of this plugin (unless someone else develops it!). Please do not file a bug report on this.

##### suggestions/requests

Suggestions for improvements are welcome, pull-requests with completed features even more so. :)

##### contributions

Thanks to:

- The developers of `salt-vim` for parts of the original YAML implementation this is based on
