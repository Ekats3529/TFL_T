from lab1 import lex_analysis, add_lex, Lex, states, lex, dict_lex, print_table, list_lex
from enum import Enum


class SyntaxAnalyzer:
    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.errors = []
        self.pos = 0

    def start(self):
        self.pos = 0
        self.errors = []

        return self.until_statement()

    def get_errors(self):
        return self.errors

    def until_statement(self):
        # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)

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

        return True

    def condition(self):
        if not self.log_expr():
            return False
        while self.pos < len(self.lexemes) and self.lexemes[self.pos].type == lex.lOr:
            # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)
            self.pos += 1
            if not self.log_expr():
                return False

        return True

    def log_expr(self):
        if self.lexemes[self.pos].type == lex.lNot or self.lexemes[self.pos].type == lex.lAnd:
            self.pos += 1

        if not self.rel_expr():
            return False

        return True

    def rel_expr(self):
        if not self.arith_expr():
            return False
        if self.lexemes[self.pos].type == lex.rel:
            # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)
            self.pos += 1
            if not self.arith_expr():
                return False

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
        self.pos += 1
        return True

    def statement(self):
        # print(self.lexemes[self.pos].value, self.lexemes[self.pos].type, self.pos)
        if self.lexemes[self.pos].type == lex.var:
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
            return True

        elif self.lexemes[self.pos].type == lex.output:
            self.pos += 1
            if not self.operand():
                return False
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
            self.pos += 1
            if not self.operand():
                return False

        return True


if __name__ == "__main__":
    text = input("Enter the text: \n")
    text = text.strip()
    if lex_analysis(text + " "):
        print_table()
        syn_an = SyntaxAnalyzer(list_lex)
        if syn_an.start():
            print("Text is a part of the program\n")
        else:
            print("Text is NOT a part of the program")

    else:
        print_table()
        print("Text is NOT a part of the program")


# do s = s * b + 10 output s loop until s < 100 or s <> b
# do s = p loop s < 100 or s <> b