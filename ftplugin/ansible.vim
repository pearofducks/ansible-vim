" Slow yaml highlighting workaround
if exists('+regexpengine') && ('&regexpengine' == 0)
  setlocal regexpengine=1
endif
setlocal expandtab
setlocal softtabstop=2
setlocal shiftwidth=2
setlocal commentstring=#%s
setlocal formatoptions=crl
setlocal autoindent

" This function is from https://gist.github.com/871107
" Author: Ian Young
function! GetYamlIndent()
  let cnum = v:lnum
  let lnum = v:lnum - 1
  if lnum == 0
    return 0
  endif
  let line = substitute(getline(lnum),'\s\+$','','')
  let cline = substitute(getline(cnum),'\s\+$','','')
  let indent = indent(lnum)
  let increase = indent + &sw
  let decrease = indent - &sw
  if line =~ ':$'
    return increase
  elseif line !~ ':$' && cline =~ ':$'
    return decrease
  elseif line =~ ':$'
  else
    return indent
  endif
endfunction
setlocal indentexpr=GetYamlIndent()

" folding
setlocal foldmethod=indent
setlocal foldlevel=6  " by default do not fold
