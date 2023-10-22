from NKA import NKAutomate


class e_NKAutomate:
    states = {}
    symbols = {}
    beg_state = None
    end_state = None
    auto_type = ""

    def __init__(self, filename):
        with open(filename) as file:
            symbols = file.readline()
            k = 0
            for ch in symbols.split():
                self.symbols[ch] = k
                k += 1
            tmp = file.readline().split()
            self.beg_state = tmp[0]
            self.end_state = tmp[1].split("|")
            states = file.readlines()
            for k in range(len(states)):
                self.states[str(k)] = [state.split("|") for state in states[k].split()]

    def print_table(self):
        print("\t\t", end="")
        sp = " " * 10
        chars = sp.join(self.symbols.keys())
        print(chars)
        for i in range(len(self.states)):
            if str(i) in self.beg_state:
                print("->", end="")
            else:
                print("  ", end="")
            if str(i) in self.end_state:
                print("* ", end="")
            else:
                print("  ", end="")
            tmp = ""
            for lst in self.states[str(i)]:
                if "-" in lst:
                    tmp += f"{'-' : <10}"
                else:
                    tmp += f'{"|".join([f"q{k}" for k in lst]): <10}'
            print(f'q{i}\t{tmp}')

    def read_word(self, word):
        print(f"The word: {word}")
        cur_state = set('0')
        for ch in word:
            if ch not in self.symbols.keys():
                print(f"Unexpected symbol {ch}")
                print(f"The {word} NOT in language")
                return
            new_state = set()
            for st in cur_state:
                tmp = set(self.states[st][self.symbols[ch]])
                new_state = new_state.union(tmp)
            new_state.discard("-")
            if len(new_state) == 0:
                print(f"The end state q{cur_state}")
                print(f"The {word} NOT in language")
                return

            print(f"q{cur_state} --- {ch} ---> q{new_state}")
            cur_state = new_state

        for st in cur_state:
            if st in self.end_state:
                print(f"The {word} in language")
                return
        print(f"The {word} NOT in language")


if __name__ == "__main__":
    KDA = NKAutomate("input_NKA.txt")
    KDA.print_table()
    print()
    KDA.read_word("ababbbcc")
