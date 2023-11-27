from lab1 import lex
from lab3 import e_cmd, EEntry_type, Entry


class SyntaxAnalyzer:
    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.errors = []
        self.pos = 0
        self.entries_list = []

    def start(self):
        self.pos = 0
        self.errors = []
        self.entries_list = []

        result = self.until_statement()

        if result:
            return True, self.entries_list
        return False, self.entries_list

    def get_errors(self):
        return self.errors

    def until_statement(self):
        # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)
        idx_first = len(self.entries_list)
        if self.lexemes[self.pos].type != lex.do:
            error = {
                'error_msg': 'Expected keyword do',
                'pos': self.pos,
            }
            print(f'{error["error_msg"]} {error["pos"]}')
            self.errors.append(error)
            return False

        self.pos += 1

        if not self.statement():
            return False

        while self.pos < len(self.lexemes) and self.lexemes[self.pos].type != lex.loop:
            if not self.statement():
                return False

        # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)

        if self.lexemes[self.pos].type != lex.loop:
            error = {
                'error_msg': 'Expected keyword loop',
                'pos': self.pos,
            }
            print(f'{error["error_msg"]} {error["pos"]}')
            self.errors.append(error)
            return False
        self.pos += 1

        # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)

        if self.lexemes[self.pos].type != lex.until:
            error = {
                'error_msg': 'Expected keyword until',
                'pos': self.pos,
            }
            print(f'{error["error_msg"]} {error["pos"]}')
            self.errors.append(error)
            return False
        self.pos += 1

        # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)

        if not self.condition():
            return False

        self.write_cmd(e_cmd.NOT)
        self.write_cmd_ptr(idx_first)
        self.write_cmd(e_cmd.JZ)

        return True

    def condition(self):
        if not self.log_expr():
            return False
        while self.pos < len(self.lexemes) and self.lexemes[self.pos].type == lex.lOr:
            # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)
            self.pos += 1
            if not self.log_expr():
                return False

            self.write_cmd(e_cmd.OR)

        return True

    def log_expr(self):
        if self.lexemes[self.pos].type == lex.lNot or self.lexemes[self.pos].type == lex.lAnd:
            if self.lexemes[self.pos].type == lex.lNot:
                self.write_cmd(e_cmd.NOT)
            else:
                self.write_cmd(e_cmd.AND)
            self.pos += 1

        if not self.rel_expr():
            return False

        return True

    def rel_expr(self):
        if not self.arith_expr():
            return False
        if self.lexemes[self.pos].type == lex.rel:
            # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)
            cmd = None
            if self.lexemes[self.pos].value == "<":
                cmd = e_cmd.CMPL
            elif self.lexemes[self.pos].value == ">":
                cmd = e_cmd.CMPG
            elif self.lexemes[self.pos].value == "<>":
                cmd = e_cmd.CMPNE
            elif self.lexemes[self.pos].value == "==":
                cmd = e_cmd.CMPE
            self.pos += 1
            if not self.arith_expr():
                return False

            self.write_cmd(cmd)

        return True

    def operand(self):
        # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)

        if self.lexemes[self.pos].type != lex.var and self.lexemes[self.pos].type != lex.const:
            error = {
                'error_msg': 'Expected variable or constant',
                'pos': self.pos,
            }
            print(f'{error["error_msg"]} {error["pos"]}')
            self.errors.append(error)
            return False
        if self.lexemes[self.pos].type == lex.var:
            self.write_var(self.pos)
        elif self.lexemes[self.pos].type == lex.const:
            self.write_const(self.pos)
        self.pos += 1
        return True

    def statement(self):
        # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)
        if self.lexemes[self.pos].type == lex.var:
            self.write_var(self.pos)
            self.pos += 1

            # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)

            if self.lexemes[self.pos].type != lex.lAs:
                error = {
                    'error_msg': 'Expected assignment',
                    'pos': self.pos,
                }
                print(f'{error["error_msg"]} {error["pos"]}')
                self.errors.append(error)
                return False

            self.pos += 1
            if not self.arith_expr():
                return False

            self.write_cmd(e_cmd.SET)
            return True

        elif self.lexemes[self.pos].type == lex.output:
            self.pos += 1
            if not self.operand():
                return False
            self.write_cmd(e_cmd.OUTPUT)
            return True
        else:
            error = {
                'error_msg': 'Expected variable or keyword output',
                'pos': self.pos,
            }
            print(f'{error["error_msg"]} {error["pos"]}')
            self.errors.append(error)
            return False

    def arith_expr(self):
        if not self.operand():
            return False
        while self.pos < len(self.lexemes) and (self.lexemes[self.pos].type == lex.ao1 or self.lexemes[self.pos].type == lex.ao2):
            # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)
            cmd = None
            if self.lexemes[self.pos].value == '+':
                cmd = e_cmd.ADD
            elif self.lexemes[self.pos].value == '-':
                cmd = e_cmd.SUB
            elif self.lexemes[self.pos].value == '/':
                cmd = e_cmd.DIV
            elif self.lexemes[self.pos].value == '*':
                cmd = e_cmd.MUL

            self.pos += 1
            if not self.operand():
                return False

            self.write_cmd(cmd)

        return True

    def write_cmd(self, cmd: e_cmd):
        command = Entry(entry_type=EEntry_type.CMD,
                        cmd=cmd,
                        index=len(self.entries_list))

        self.entries_list.append(command)

        return len(self.entries_list) - 1

    def write_var(self, idx: int):
        variable = Entry(entry_type=EEntry_type.VAR,
                         value=self.lexemes[idx].value,
                         index=len(self.entries_list))

        self.entries_list.append(variable)

        return len(self.entries_list) - 1

    def write_const(self, idx: int):
        constant = Entry(entry_type=EEntry_type.CONST,
                         value=self.lexemes[idx].value,
                         index=len(self.entries_list))

        self.entries_list.append(constant)

        return len(self.entries_list) - 1

    def write_cmd_ptr(self, ptr):
        cmd_ptr = Entry(entry_type=EEntry_type.CMD_PTR,
                        cmd_ptr=ptr,
                        index=len(self.entries_list))

        self.entries_list.append(cmd_ptr)

        return len(self.entries_list) - 1

    def set_cmd_ptr(self, idx: int, ptr: int):
        self.entries_list[idx].cmd_ptr = ptr


