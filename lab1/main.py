from enum import Enum

states = Enum('states', ["S", 'Ai', 'Ac', 'As', 'Bs', "Cs",
                         'Ds', 'Gs', "E", "F"])

lex = Enum('lex', ["do", 'loop', 'until',
                   'lNot', 'lAnd', 'lOr', 'output',
                   'rel', 'lAs', 'ao', 'var', 'const'])


class Lex:
    type = None
    value = None

    def __init__(self, type, value):
        self.type = type
        self.value = value


list_lex = []


def add_lex(state, string, block):
    # print("\t\t", state, string, block)
    if len(list_lex) > 0:
        prev_state = list_lex[-1].type

    tmp = string.lower()

    if tmp == "do":
        if len(list_lex) == 0:
            list_lex.append(Lex(lex.do, tmp))
            return True
        return False
    if len(list_lex) == 0:
        return False

    if tmp == "loop":
        if prev_state == lex.var or prev_state == lex.const:
            list_lex.append(Lex(lex.loop, tmp))
            return True
        return False

    if tmp == "until":
        if prev_state == lex.loop:
            list_lex.append(Lex(lex.until, tmp))
            return True
        return False

    if tmp == "not":
        if prev_state in [lex.until, lex.lAnd, lex.lOr]:
            list_lex.append(Lex(lex.lNot, tmp))
            return True
        return False

    if tmp == "and":
        if prev_state == lex.var or prev_state == lex.const:
            list_lex.append(Lex(lex.lAnd, tmp))
            return True
        return False

    if tmp == "or":
        if prev_state == lex.var or prev_state == lex.const:
            list_lex.append(Lex(lex.lOr, tmp))
            return True
        return False

    if tmp == "output":
        if prev_state == lex.var or prev_state == lex.const:
            list_lex.append(Lex(lex.output, tmp))
            return True
        return False

    if state in [states.As, states.Ds, states.Gs]:
        if prev_state == lex.var or prev_state == lex.const:
            list_lex.append(Lex(lex.rel, tmp))
            return True
        if state == states.Ds:
            prev_2_state = list_lex[-2].type if len(list_lex) > 2 else None
            if prev_state == lex.var or prev_state == lex.const or prev_2_state == lex.var or prev_2_state == lex.const:
                list_lex.append(Lex(lex.rel, tmp))
                return True
        return False

    if state == states.Bs:
        prev_2_state = list_lex[-2].type if len(list_lex) > 2 else None
        if prev_state == lex.var or prev_state == lex.const or prev_2_state == lex.var or prev_2_state == lex.const:
            list_lex.append(Lex(lex.lAs, tmp))
            return True
        return False

    if state == states.Cs:
        if prev_state == lex.var or prev_state == lex.const:
            list_lex.append(Lex(lex.ao, tmp))
            return True
        return False

    if state == states.Ai or state == states.Ac:
        if block == 0:
            if prev_state in [lex.lAs, lex.output, lex.do, lex.ao]:
                if state == states.Ai:
                    list_lex.append(Lex(lex.var, tmp))
                if state == states.Ac:
                    list_lex.append(Lex(lex.const, tmp))
                return True
        elif block == 1:
            if prev_state == lex.lAs or prev_state == lex.output:
                return False
            if state == states.Ai:
                list_lex.append(Lex(lex.var, tmp))
            if state == states.Ac:
                list_lex.append(Lex(lex.const, tmp))
            return True

        return False


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
                    if not add_lex(prev_state, lexm, type_expr):
                        return False

                lexm = ""

            if len(list_lex) > 0 and list_lex[-1].type == lex.until:
                type_expr = 1

            if cur_state != states.E and cur_state != states.F:
                lexm += string[i]
                i += 1

    if type_expr == 0 or list_lex[-1].type not in [lex.var, lex.const]:
        return False

    return True


if __name__ == "__main__":
    text = input("Enter the text: \n")
    text = text.strip()
    if lex_analysis(text + " "):
        print("Text is a part of the program\n")
        for x in list_lex:
            print(x.value, x.type)
    else:
        print("Text is NOT a part of the program")
