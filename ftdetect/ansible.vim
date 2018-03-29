function! s:isAnsible()
  if exists("g:ansible_disable_auto_ftdetect") | return 0 | en
  let filepath = expand("%:p")
  let filename = expand("%:t")

  let not_ansible_files = ['\v\.travis\.ya?ml$', '\v\.kitchen\.ya?ml']
  let non_ansible_matches = filter(not_ansible_files, 'filename  =~? v:val')
  if len(non_ansible_matches) | return 0 | en

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

augroup filetype_ansible_vim
    au!
    au BufNewFile,BufRead * if s:isAnsible() | set ft=yaml.ansible | en
    au BufNewFile,BufRead *.j2 call s:setupTemplate()
    au BufNewFile,BufRead hosts set ft=ansible_hosts
augroup END
