function! s:isAnsible()
  let filepath = expand("%:p")
  let filename = expand("%:t")
  if filepath =~ '\v/(tasks|roles)/.*\.ya?ml$' | return 1 | en
  if filepath =~ '\v/(group|host)_vars/' | return 1 | en
  if filename =~ '\v(playbook|site)\.ya?ml$' | return 1 | en

  let shebang = getline(1)
  if shebang =~# '^#!.*/bin/env\s\+ansible-playbook\>' | return 1 | en
  if shebang =~# '^#!.*/bin/ansible-playbook\>' | return 1 | en

  return 0
endfunction

:au BufNewFile,BufRead * if !did_filetype() && s:isAnsible() | setf ansible | en
:au BufNewFile,BufRead *.j2 set ft=ansible_template
:au BufNewFile,BufRead hosts set ft=ansible_hosts
