# vim-follow

This is a very small script (<100loc) that mirrors `gdb`'s current frame location (file and line) within `vim`.
It relies on `vim`'s client-server capabilities and does not need any plugins to be installed.

This script works both under Python 2.7 and 3.

## Installation

Edit `.gdbinit` to source `vim-follow.py`

```
source /path/to/vim-follow.py 
```

## Usage

In `vim`, execute `:call remote_startserver('gdb')`, or alternatively start `vim` with:
```
$ vim --servername gdb
```

Start up `gdb`, and run the `vim follow` command.

When you will start debugging, you will notice that the current buffer in `vim` will reflect the current position in the code.

When you want to stop, run `vim unfollow`.

## Further details

You can use any server name you wish, but `'gdb'` is set by default in `vim-follow.py`.
Run `vim server customname` in `gdb` and `:call remote_startserver('customname')` in `vim` to use `customname` as a server name.

If you just want to set the location once (without following) just run the `vim` command without arguments within `gdb`.
