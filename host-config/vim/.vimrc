set showcmd
set ruler
set backspace=2
set nocompatible
set autoindent
"set cindent
set history=50
set vb t_vb=
set noerrorbells
set hlsearch
set number
set term=xterm
set tabstop=4       " numbers of spaces of tab character
set shiftwidth=4    " numbers of spaces to (auto)indent
set softtabstop=4
set expandtab
"set mouse=a

syntax on           
set t_Co=256
syntax enable


" Force using the Django template syntax file
let g:sls_use_jinja_syntax = 1

filetype plugin indent on
filetype on

set background=dark
colorscheme solarized
"colorscheme elflord
"colorscheme peachpuff
"colorscheme anotherdark
"colorscheme slate

" Press F4 to toggle highlighting on/off, and show current value.
noremap <F4> :set hlsearch! hlsearch?<CR>
noremap <F5> :set number! number?<CR>

au VimResized,TermResponse,GUIEnter,FocusGained,VimEnter,WinEnter,BufFilePost,BufReadPost,BufNewFile * let &titlestring = ' ' . expand("%:t")
set title

au BufWritePost {*.pm,*.pl,*.inc,*.cgi} !perl -c %
au BufWritePost {*.xsl} !xsltproc % > /dev/null
au BufWritePost {*.py} call CheckPythonSyntax()
au BufWritePost {*.pp} !puppet parser validate  %

"For align
set nocp

"set foldmethod=indent

function CheckPythonSyntax()
  " Write the current buffer to a temporary file, check the syntax and
  " if no syntax errors are found, write the file
  let curfile = bufname("%")
  let tmpfile = tempname()
  silent execute "write! ".tmpfile
  let output = system("python -c \"__import__('py_compile').compile(r'".tmpfile."')\" 2>&1")
  if output != ''
    " Make sure the output specifies the correct filename
    let output = substitute(output, fnameescape(tmpfile), fnameescape(curfile), "g")
    echo output
  else
    write
  endif
  " Delete the temporary file when done
  call delete(tmpfile)
endfunction


