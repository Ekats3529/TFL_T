from enum import Enum

states = Enum('states', ["S", 'Ai', 'Ac', 'As', 'Bs', "Cs",
                         'Ds', 'Gs', "E", "F"])

lex = Enum('lex', ["do", 'loop', 'until',
                   'lNot', 'lAnd', 'lOr', 'output',
                   'rel', 'lAs', 'ao1', 'ao2', 'var', 'const'])

dict_lex = {lex.do: ["do", "begin of the loop body"],
            lex.loop: ["loop", "end of the loop body"],
            lex.until: ["until", "begin of condition statement"],
            lex.lNot: ["not", "logical not"],
            lex.lAnd: ["and", "logical and"],
            lex.lOr: ["or", "logical or"],
            lex.output: ["output", "output on screen"],
            lex.rel: ["rel", "relation operation"],
            lex.lAs: ["as", "assign"],
            lex.ao1: ["ao1", "arithmetic operation priority 1"],
            lex.ao2: ["ao2", "arithmetic operation priority 2"],
            lex.var: ["var", "variable"],
            lex.const: ["const", "constant"]}


class Lex:
    type = None
    value = None
    pos = -1

    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        self.pos = pos


list_lex = []


def add_lex(state, string, pos):
    # print("\t\t", state, string, block)
    if len(list_lex) > 0:
        prev_state = list_lex[-1].type

    tmp = string.lower()

    if tmp == "do":
        list_lex.append(Lex(lex.do, tmp, pos))
        return True

    if tmp == "loop":
        list_lex.append(Lex(lex.loop, tmp, pos))
        return True

    if tmp == "until":
        list_lex.append(Lex(lex.until, tmp, pos))
        return True

    if tmp == "not":
        list_lex.append(Lex(lex.lNot, tmp, pos))
        return True

    if tmp == "and":
        list_lex.append(Lex(lex.lAnd, tmp, pos))
        return True

    if tmp == "or":
        list_lex.append(Lex(lex.lOr, tmp, pos))
        return True

    if tmp == "output":
        list_lex.append(Lex(lex.output, tmp, pos))
        return True

    if state in [states.As, states.Ds, states.Gs]:
        list_lex.append(Lex(lex.rel, tmp, pos))
        return True

    if state == states.Bs:
        list_lex.append(Lex(lex.lAs, tmp, pos))
        return True

    if state == states.Cs:
        if string in ['+', '-']:
            list_lex.append(Lex(lex.ao2, tmp, pos))
            return True
        if string in ['*', '/']:
            list_lex.append(Lex(lex.ao1, tmp, pos))
            return True

    if state == states.Ai or state == states.Ac:
        if state == states.Ai:
            list_lex.append(Lex(lex.var, tmp, pos))
        if state == states.Ac:
            list_lex.append(Lex(lex.const, tmp, pos))
        return True


def lex_analysis(text):
    cur_state = states.S
    prev_state = states.S
    add = False
    string = text
    i = 0
    type_expr = 0

    while i < len(string):
        lexm = ""
        while cur_state != states.E and cur_state != states.F and i < len(string):
            # print(string[i], lexm, cur_state)
            prev_state = cur_state
            add = False

            if cur_state == states.S:
                if string[i] == " ":
                    cur_state = states.F
                    add = True
                elif string[i].isalpha():
                    cur_state = states.Ai
                elif string[i].isdigit():
                    cur_state = states.Ac
                elif string[i] == "<":
                    cur_state = states.As
                elif string[i] == ">":
                    cur_state = states.Ds
                elif string[i] == "=":
                    cur_state = states.Bs
                elif string[i] in ['*', '-', '+', '-']:
                    cur_state = states.Cs
                else:
                    cur_state = states.E
                    add = False

            elif cur_state == states.Ai:
                if string[i] == " ":
                    cur_state = states.S
                    add = True
                elif string[i].isalnum():
                    add = False
                elif string[i] == "<":
                    cur_state = states.As
                elif string[i] == ">":
                    cur_state = states.Ds
                elif string[i] == "=":
                    cur_state = states.Bs
                elif string[i] in ['*', '-', '+', '-']:
                    cur_state = states.Cs
                else:
                    cur_state = states.E
                    add = False

            elif cur_state == states.Ac:
                if string[i] == " ":
                    cur_state = states.S
                    add = True
                elif string[i].isdigit():
                    add = False
                elif string[i] == "<":
                    cur_state = states.As
                elif string[i] == ">":
                    cur_state = states.Ds
                elif string[i] == "=":
                    cur_state = states.Bs
                elif string[i] in ['*', '-', '+', '-']:
                    cur_state = states.Cs
                else:
                    cur_state = states.E
                    add = False

            elif cur_state == states.As:
                if string[i] == " ":
                    cur_state = states.S
                    add = True
                elif string[i].isalpha():
                    cur_state = states.Ai
                elif string[i].isdigit():
                    cur_state = states.Ac
                elif string[i] == ">":
                    cur_state = states.Ds
                else:
                    cur_state = states.E
                    add = False

            elif cur_state == states.Bs:
                if string[i] == " ":
                    cur_state = states.S
                    add = True
                elif string[i].isalpha():
                    cur_state = states.Ai
                elif string[i].isdigit():
                    cur_state = states.Ac
                elif string[i] == "=":
                    cur_state = states.Gs
                else:
                    cur_state = states.E
                    add = False

            elif cur_state == states.Ds:
                if string[i] == " ":
                    cur_state = states.S
                    add = True
                elif string[i].isalpha():
                    cur_state = states.Ai
                elif string[i].isdigit():
                    cur_state = states.Ac
                else:
                    cur_state = states.E
                    add = False

            elif cur_state == states.Cs:
                if string[i] == " ":
                    cur_state = states.S
                    add = True
                elif string[i].isalpha():
                    cur_state = states.Ai
                elif string[i].isdigit():
                    cur_state = states.Ac
                else:
                    cur_state = states.E
                    add = False

            if cur_state == states.E:
                return False

            if add:
                lexm = "".join(lexm.strip().split())
                if len(lexm) == 0:
                    i += 1
                    continue
                if len(lexm) > 0:
                    if not add_lex(prev_state, lexm, i - len(lexm)):
                        return False

                lexm = ""

            if cur_state != states.E and cur_state != states.F:
                lexm += string[i]
                i += 1

    return True


def print_table():
    print(f"{'value of lex':^13} | {'position of lex':^17} | {'type of lex':^13} | {'definition of lex':<40}")
    print("-" * 72)
    for x in list_lex:
        print(f"{x.value:<13} | {x.pos:^17} | {dict_lex[x.type][0]:<13} | {dict_lex[x.type][1]:<40}")



# do s = s * b + 10 output s loop until s < 100 or s <> b
