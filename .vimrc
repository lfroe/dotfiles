" Pathogen setup
runtime bundle/vim-pathogen/autoload/pathogen.vim
" Bundle: tpope/vim-pathogen
call pathogen#infect()

" Bundles
"
" Bundle: tpope/vim-sensible
" Bundle: tpope/vim-rails
" Bundle: tpope/vim-fugitive
" Bundle: tpope/vim-dispatch
" Bundle: bling/vim-airline
" Bundle: airblade/vim-gitgutter
" Bundle: mattn/emmet-vim
" Bundle: endwise.vim
" Bundle: scrooloose/syntastic
" Bundle: tpope/vim-surround
" Bundle: tpope/vim-commentary
" Bundle: scrooloose/nerdtree
" Bundle: altercation/vim-colors-solarized
" Bundle: kien/ctrlp.vim
" Bundle: ervandew/supertab
" Bundle: "rizzatti/funcoo.vim"
" Bundle: "rizzatti/dash.vim"
" Bundle: "amiel/vim-tmux-navigator"
" Bundle: "digitaltoad/vim-jade"

syntax on
filetype plugin on
filetype indent on
filetype on
set clipboard=unnamed
set background=dark
set backspace=indent,eol,start

set t_Co=256
set nocompatible
set modelines=0
set tabstop=2
set shiftwidth=2
set softtabstop=2
set expandtab
set encoding=utf-8
set scrolloff=3
set autoindent
set showmode
set showcmd
set hidden
set wildmenu
set wildmode=longest,list,full
set visualbell
set cursorline
set ttyfast
set ruler
set backspace=indent,eol,start
set laststatus=2
set relativenumber
set rnu
"set undofile
"set undodir=~/.vim/undo " where to save undo histories
"set undolevels=1000         " How many undos
"set undoreload=10000        " number of lines to save for undo
"set backupdir=~/.vim/backup/
"set directory=~/.vim/backup/

let mapleader = ","
let g:ctrlp_map = "<c-p>"
nnoremap / /\v
vnoremap / /\v
nnoremap <leader><leader> <c-^>
vnoremap <leader>G :w !gist -p -t %:e \| pbcopy<cr>
nnoremap <C-u> gUiw
inoremap <C-u> <esc>gUiwea
nnoremap <C-p> Vy<esc>p
vnoremap <leader>S y:execute @@<cr>
nnoremap <leader>S ^vg_y:execute @@<cr>
nnoremap vv ^vg_
nnoremap gn <esc>:tabnew<cr>

cnoremap <c-a> <home>
cnoremap <c-e> <end>

nnoremap <leader>V V`]
cmap w!! w !sudo tee % >/dev/null
nnoremap vv V

set ignorecase
set smartcase
set gdefault
set incsearch
set showmatch
set hlsearch
nnoremap <leader><space> :noh<cr>
nnoremap <tab> %
vnoremap <tab> %

augroup line_return
  au!
  au BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") |
    \   execute 'normal! g`"zvzz' |
    \ endif
augroup END

set wrap
set formatoptions=qrn1
color molokai
set list
set listchars=tab:▸\ ,eol:¬

nnoremap <up> <nop>
nnoremap <down> <nop>
nnoremap <left> <nop>
nnoremap <right> <nop>
inoremap <up> <nop>
inoremap <down> <nop>
inoremap <left> <nop>
inoremap <right> <nop>
nnoremap j gj
nnoremap k gk
nnoremap ; :

au FocusLost * :wa

nnoremap <leader>ev <C-w><C-v><C-l>:e $MYVIMRC<cr>
inoremap jk <ESC>
inoremap kj <ESC>
nnoremap <leader>w <C-w>v<C-w>l
nnoremap n nzzzv
nnoremap N Nzzzv
nnoremap H ^
nnoremap L g_
"inoremap " '
"inoremap ' "

autocmd BufWritePre * :%s/\s\+$//e
nmap <leader>rh :%s/\v:(\w+) \=\>/\1:/g<cr>

inoremap <c-a> <esc>I
inoremap <c-e> <esc>A

nnoremap <silent><leader>/ :execute 'vimgrep /'.@/.'/g %'<CR>:copen<CR>

let g:airline_powerline_fonts = 1
let g:airline#extensions#hunks#non_zero_only = 1

" Nerdtree if no file is specified
autocmd vimenter * if !argc() | NERDTree | endif

set foldlevelstart=-
nnoremap <Space> za
vnoremap <Space> za
nnoremap z0 zCz0
nnoremap <leader>z zMzvzz

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" SWITCH BETWEEN TEST AND PRODUCTION CODE
" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" TODO: Make better for handling test/unit, etc
function! OpenTestAlternate()
  let new_file = AlternateForCurrentFile()
  exec ':e ' . new_file
endfunction
function! AlternateForCurrentFile()
  let current_file = expand("%")
  let new_file = current_file
  let in_engine = match(current_file, '^engines') != -1

  let in_spec = match(current_file, '^spec/') != -1 ||
        \ match(current_file, '^engines/.\+/spec/') != -1
  let going_to_spec = !in_spec
  let in_app = match(current_file, '\<controllers\>') != -1 ||
        \ match(current_file, '\<models\>') != -1 ||
        \ match(current_file, '\<views\>') != -1 ||
        \ match(current_file, '\<helpers\>') != -1 ||
        \ match(current_file, '\<decorators\>') != -1 ||
        \ match(current_file, '\<presenters\>') != -1 ||
        \ match(current_file, '\<uploaders\>') != -1

  if in_engine
    " TODO: use :A for test/unit, etc
    exec ":A"
  else
    if going_to_spec
      if in_app
        let new_file = substitute(new_file, '^app/', '', '')
      end
      let new_file = substitute(new_file, '\.rb$', '_spec.rb', '')
      let new_file = 'spec/' . new_file
    else
      let new_file = substitute(new_file, '\(_spec\|_test\)\.rb$', '.rb', '')
      let new_file = substitute(new_file, '^\(spec\|test\)/', '', '')
      if in_app
        let new_file = 'app/' . new_file
      end
    endif
  endif
  return new_file
endfunction

" Trying out just :A always to see how that goes
" Maybe I'll end up wanting it for rails projects, but then OpenTestAlternate
" for non-rails projects
" nnoremap <leader>. :A<cr>
nnoremap <leader>. :call OpenTestAlternate()<cr>

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" RUNNING TESTS
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
map <leader>r :call RunTestFile()<cr>
map <leader>R :call RunNearestTest()<cr>
map <leader>a :call RunTests('')<cr>

function! RunTestFile(...)
    if a:0
        let command_suffix = a:1
    else
        let command_suffix = ""
    endif

    " Run the tests for the previously-marked file.
    let in_test_file = match(expand("%"), '\(.feature\|_spec.rb\|_test.rb\)$') != -1
    if in_test_file
        call SetTestFile()
    elseif !exists("t:grb_test_file")
        return
    end
    call RunTests(t:grb_test_file . command_suffix)
endfunction

function! RunNearestTest()
    let spec_line_number = line('.')
    call RunTestFile(":" . spec_line_number . " -b")
endfunction

function! SetTestFile()
    " Set the spec file that tests will be run for.
    let t:grb_test_file=@%
endfunction

function! DispatchTests(command)
  let command = a:command

  " if filereadable(".ruby-version")
  "   let ruby_version = "`cat .ruby-version`"
  "   if filereadable(".ruby-gemset")
  "     let ruby_version = ruby . "@`cat .ruby-gemset`"
  "   endif
  " endif


  exec ":Dispatch " . a:command
endfunction

function! RunTests(filename)
    :w
    if filereadable("script/test")
      call DispatchTests("script/test " . a:filename)
    elseif filereadable("Gemfile")
      call DispatchTests("bundle exec rspec --color " . a:filename)
    else
      call DispatchTests("rspec --color " . a:filename)
    end
endfunction

""""""""
" Rails.vim
""""""""

let g:rails_projections = {
  \ 'app/admin/*.rb': {
  \   'command': 'admin',
  \   'template':
  \     'ActiveAdmin.register %S do\nend',
  \   'affinity': 'model'
  \ }}
