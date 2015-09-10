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
:au BufNewFile,BufRead *.j2 set ft=ansible_template " do we have jinja2 available?
:au BufNewFile,BufRead hosts set ft=dosini

" if hosts file, set dosini and patch for :
" if *.j2, set jinja
" if *.yml or *.yaml - look in the directory to detect
  " or the filename (site.yaml, playbook.yaml)
  " or if the file rests exactly inside of group_vars or host_vars
