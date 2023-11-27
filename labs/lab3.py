from enum import Enum

e_cmd = Enum('e_cmd', ["JMP", 'JZ', 'SET',
                       'ADD', 'SUB', 'MUL', 'DIV',
                       'NOT', 'AND', 'OR',
                       'CMPE', 'CMPNE', 'CMPL', 'CMPG',
                       'OUTPUT'])

EEntry_type = Enum('EEntry_type', ["CMD", "VAR", "CONST", "CMD_PTR"])


class Entry:
    def __init__(
            self,
            index=0,
            entry_type=EEntry_type.CMD,
            cmd=e_cmd.JZ,
            value='',
            current_value=0,
            cmd_ptr=EEntry_type.CMD_PTR
    ):
        self.index = index
        self.entry_type = entry_type
        self.cmd = cmd
        self.value = value
        self.current_value = current_value
        self.cmd_ptr = cmd_ptr

    def __str__(self):
        print_value = self.cmd.name
        if self.entry_type == EEntry_type.VAR or self.entry_type == EEntry_type.CONST:
            print_value = self.value
        elif self.entry_type == EEntry_type.CMD_PTR:
            print_value = self.cmd_ptr

        return f'{self.index: ^3} | {self.entry_type.name:<10} | {print_value:<7}'


