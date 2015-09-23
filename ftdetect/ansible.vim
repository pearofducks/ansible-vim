function! DetectAnsible()
  let filepath = expand("%:p")
  let filename = expand("%:t")
  if filepath =~ '\v/(tasks|roles)/.*\.ya?ml$' || filepath =~ '\v/(group|host)_vars/' || filename =~ '\v(playbook|site)\.ya?ml$'
    set ft=ansible
  endif
  unlet filepath
  unlet filename
endfunction

:au BufNewFile,BufRead *.yml,*yaml,*/{group,host}_vars/*  call DetectAnsible()
:au BufNewFile,BufRead *.j2 set ft=ansible_template
:au BufNewFile,BufRead hosts set ft=ansible_hosts
