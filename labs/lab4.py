from lab1 import lex_analysis, print_table, list_lex
from lab2 import SyntaxAnalyzer
from lab3 import e_cmd, EEntry_type, Entry


class Interpreter:
    def __init__(
        self,
        syntax_result,
        syntax_response,
        entry_list: list[Entry] = [],
        stack: list = [],
        logs: list[str] = [],
    ):
        self.entry_list = entry_list
        self.stack = stack
        self.logs = logs
        self.syntax_result = syntax_result
        self.syntax_response = syntax_response

    @staticmethod
    def format_out(s):
        print(f'{s}')

    def start(self) -> bool:
        self.logs = []
        self.entry_list = self.syntax_response.copy()
        self.stack = []

        if self.syntax_result:
            self.enter_variable_values()
            print('Результат: ')
            self.interpret()
            print('------------------------------')

            for log in self.logs:
                print(log)

    def interpret(self):
        temp = None
        pos: int = 0
        self.log(pos)

        while pos < len(self.entry_list):
            if self.entry_list[pos].entry_type == EEntry_type.CMD:
                cmd = self.entry_list[pos].cmd
                if cmd == e_cmd.JMP:
                    pos = self.pop_val()
                elif cmd == e_cmd.JZ:
                    temp = self.pop_val()

                    if self.pop_val() == 1:
                        pos += 1
                    else:
                        pos = temp
                elif cmd == e_cmd.SET:
                    self.set_var_and_pop(self.pop_val())
                    pos += 1
                elif cmd == e_cmd.ADD:
                    self.push_val(self.pop_val() + self.pop_val())
                    pos += 1
                elif cmd == e_cmd.SUB:
                    self.push_val(-self.pop_val() + self.pop_val())
                    pos += 1
                elif cmd == e_cmd.MUL:
                    self.push_val(self.pop_val() * self.pop_val())
                    pos += 1
                elif cmd == e_cmd.DIV:
                    self.push_val(int(1.0 / self.pop_val() * self.pop_val()))
                    pos += 1
                elif cmd == e_cmd.NOT:
                    self.push_val(not(self.pop_val() != 0))
                    pos += 1
                elif cmd == e_cmd.AND:
                    self.push_val(self.pop_val() != 0 and (1 if self.pop_val() != 0 else 0))
                    pos += 1
                elif cmd == e_cmd.OR:
                    self.push_val(self.pop_val() != 0 or (1 if self.pop_val() != 0 else 0))
                    pos += 1
                elif cmd == e_cmd.CMPE:
                    self.push_val(1 if self.pop_val() == self.pop_val() else 0)
                    pos += 1
                elif cmd == e_cmd.CMPNE:
                    self.push_val(1 if self.pop_val() != self.pop_val() else 0)
                    pos += 1
                elif cmd == e_cmd.CMPL:
                    self.push_val(1 if self.pop_val() > self.pop_val() else 0)
                    pos += 1
                elif cmd == e_cmd.CMPG:
                    self.push_val(1 if self.pop_val() < self.pop_val() else 0)
                    pos += 1
                elif cmd == e_cmd.OUTPUT:
                    output = self.pop_val()
                    self.logs.append(f"OUTPUT : {output}")
                    pos += 1
                else:
                    print('!!!!!')
            else:
                self.push_elem(self.entry_list[pos])
                pos += 1

            if pos < len(self.entry_list):
                self.log(pos)

        return True

    def log(self, pos: int) -> None:
        print_pos = f'pos: {pos}'
        print_elem = f'elem: {self.get_entry_string(self.entry_list[pos])}'
        print_val = f'values: {self.get_var_values()}'
        print_stack = f'stack: {self.get_stack_state()}'
        self.logs.append(f"{print_pos: <13} | {print_elem: <20} | {print_val: <20} | {print_stack: <20} |")

    def pop_val(self) -> int:
        if len(self.stack) != 0:
            obj: Entry = self.stack.pop()

            match obj.entry_type:
                case EEntry_type.VAR:
                    return obj.current_value
                case EEntry_type.CONST:
                    return int(obj.value)
                case EEntry_type.CMD:
                    return obj.cmd.value
                case EEntry_type.CMD_PTR:
                    return obj.cmd_ptr
                case _:
                    raise Exception(';)')
        else:
            return 0

    def push_val(self, val: int) -> None:
        entry: Entry = Entry(entry_type=EEntry_type.CONST, value=int(val))

        self.stack.append(entry)

    def push_elem(self, entry: Entry) -> None:
        if entry.entry_type == EEntry_type.CMD:
            raise Exception('EntryType')

        self.stack.append(entry)

    def set_var_and_pop(self, val: int) -> None:
        variable: Entry = self.stack.pop()

        if variable.entry_type != EEntry_type.VAR:
            raise Exception('EntryType')

        self.set_values_to_variables(variable.value, val)

    def get_entry_string(self, entry: Entry) -> str:
        if entry.entry_type == EEntry_type.VAR:
            return entry.value
        elif entry.entry_type == EEntry_type.CONST:
            return entry.value
        elif entry.entry_type == EEntry_type.CMD:
            return str(entry.cmd)
        elif entry.entry_type == EEntry_type.CMD_PTR:
            return str(entry.cmd_ptr)

        raise Exception('PostfixEntry')

    def get_stack_state(self) -> str:
        entries: list[Entry] = self.stack.copy()
        sb = ''

        for entry in entries:
            sb += f'{self.get_entry_string(entry)} '

        return sb

    def get_var_values(self) -> str:
        sb = ''

        entries = []
        for entry in self.entry_list:
            if entry.entry_type == EEntry_type.VAR:
                entries.append({
                    'value': entry.value,
                    'current_value': entry.current_value
                })

        entries = list(map(dict, set(tuple(sorted(e.items())) for e in entries)))

        for e in entries:
            sb += f'{e["value"]} = {e["current_value"]} '

        return sb

    def get_variables(self) -> list[Entry]:
        return list(filter(lambda e: e.entry_type == EEntry_type.VAR, self.entry_list))

    def set_values_to_variables(self, name: str, value: int) -> None:
        variables = list(filter(lambda v: v.value == name, self.get_variables()))

        for v in variables:
            v.current_value = value

    def enter_variable_values(self):
        try:
            print('Введите значений переменных:')

            variables = set(map(lambda v: v.value, self.get_variables()))

            for variable in variables:
                print(f'{variable} =', end=' ')
                value = int(input())

                self.set_values_to_variables(variable, value)
        except Exception as err:
            print(err)


if __name__ == "__main__":
    text = input("Enter the text: \n")
    text = text.strip()
    if lex_analysis(text + " "):
        print_table()
        syn_an = SyntaxAnalyzer(list_lex)
        result, response = syn_an.start()
        if result:
            print("\nText is a part of the program\n")
            print(*response, sep='\n')
            print(f"{'Interpretation':-^30}")
            interpreter = Interpreter(syntax_result=result, syntax_response=response)
            interpreter.start()

        else:
            print("Text is NOT a part of the program")


    else:
        print_table()
        print("Text is NOT a part of the program")


# do a = a + b loop until a < 5 or b + 3 > 7
# do a = a + 1 b = b + 2 output a output b loop until a < 5 and b < 9
