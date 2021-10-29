#
# Copyright (c) 2021 Vasile Vilvoiu <vasi@vilvoiu.ro>
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the MIT license. See LICENSE for details.
#
import os

global server_name
server_name = 'gdb'
global follow
follow = False

def vim_goto_location(file, line):
    if file is None or line is None:
        return
    keystrokes = '<Esc>:edit {}<CR>:{}<CR>zz'.format(file, line)
    os.system('vim --servername {} --remote-send "{}"'.format(server_name, keystrokes))

def get_location():
    try:
        sal = gdb.selected_frame().find_sal()
        return sal.symtab.fullname(), sal.line
    except:
        return None, None

def prompt_handler():
    f, l = get_location()
    vim_goto_location(f, l)

class Vim(gdb.Command):
    def __init__(self):
        super(Vim, self).__init__('vim', gdb.COMMAND_FILES)

    def complete(self, text, word):
        CMDS = ['server', 'follow', 'unfollow']
        return [k for k in CMDS if k.startswith(text)]

    def invoke(self, argument, from_tty):
        global server_name
        global follow
        tok = argument.split()
        if len(tok) == 0:
            f, l = get_location()
            vim_goto_location(f, l)
        elif tok[0] == 'server':
            if len(tok) != 2:
                gdb.write('Usage: vim server <server_name>\n')
            else:
                server_name = tok[1]
        elif tok[0] == 'follow':
            if len(tok) != 1:
                gdb.write('vim follow takes no parameters')
            else:
                try:
                    if not follow:
                        gdb.events.before_prompt.connect(prompt_handler)
                        follow = True
                except:
                    pass
        elif tok[0] == 'unfollow':
            if len(tok) != 1:
                gdb.write('vim unfollow takes no parameters\n')
            else:
                try:
                    if follow:
                        gdb.events.before_prompt.disconnect(prompt_handler)
                        follow = False
                except:
                    pass
        else:
            gdb.write('Bad argument; try "server", "follow", "unfollow" or without arguments\n')

Vim()
