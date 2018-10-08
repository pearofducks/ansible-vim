function! s:isAnsible()
  let filepath = expand("%:p")
  let filename = expand("%:t")
  if filepath =~ '\v/(tasks|roles|handlers)/.*\.ya?ml$' | return 1 | en
  if filepath =~ '\v/(group|host)_vars/' | return 1 | en
  if filename =~ '\v(playbook|site|main|local)\.ya?ml$' | return 1 | en

  let shebang = getline(1)
  if shebang =~# '^#!.*/bin/env\s\+ansible-playbook\>' | return 1 | en
  if shebang =~# '^#!.*/bin/ansible-playbook\>' | return 1 | en

  return 0
endfunction

function! s:setupTemplate()
  if exists("g:ansible_template_syntaxes")
    let filepath = expand("%:p")
    for syntax_name in items(g:ansible_template_syntaxes)
      let s:syntax_string = '\v/'.syntax_name[0]
      if filepath =~ s:syntax_string
        execute 'set ft='.syntax_name[1].'.jinja2'
        return
      endif
    endfor
  endif
  set ft=jinja2
endfunction

if !exists('g:ansible_yaml_filetype_name')
  let g:ansible_yaml_filetype_name = 'yaml.ansible'
endif

augroup SetupAnsible
  au!
  au BufNewFile,BufRead * if s:isAnsible() | execute 'set ft='.g:ansible_yaml_filetype_name | en
  au BufNewFile,BufRead *.j2 call s:setupTemplate()
  au BufNewFile,BufRead hosts set ft=ansible_hosts
augroup END
