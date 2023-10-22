class KDAutomate:

    states = {}
    symbols = {}
    beg_state = None
    end_state = None

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
                self.states[k] = states[k].split()

    def set_states(self, states):
        self.states = states

    def set_end_state(self, end_state):
        self.end_state = end_state

    def set_beg_state(self, beg_state):
        self.beg_state = beg_state

    def set_symbols(self, symbols):
        self.symbols = symbols

    def print_table(self):
        print("\t  ", end="")
        chars = "".join([f"{ch: >8}" for ch in self.symbols.keys()])
        print(chars)
        for i in range(len(self.states)):
            if str(i) == self.beg_state:
                print("->", end="")
            else:
                print("  ", end="")
            if str(i) in self.end_state:
                print("* ", end="")
            else:
                print("  ", end="")
            tmp = "    ".join([f"q{k: <3}" if k != "-" else "- " for k in self.states[i]])
            print(f'q{i: <5}\t{tmp}')

    def read_word(self, word):
        print(f"The word: {word}")
        cur_state = 0
        for ch in word:
            if ch not in self.symbols.keys():
                print(f"Unexpected symbol {ch}")
                print(f"The {word} NOT in language")
                return
            new_state = self.states[cur_state][self.symbols[ch]]
            if new_state != '-':
                print(f"q{cur_state} --{ch}--> q{new_state}")
                cur_state = int(new_state)
            else:
                print(f"The end state q{cur_state}")
                print(f"The {word} NOT in language")
                return
        if str(cur_state) in self.end_state:
            print(f"The {word} in language")
            return
        print(f"The {word} NOT in language")


if __name__ == "__main__":
    KDA = KDAutomate("input_KDA.txt")
    KDA.print_table()
    print()
    KDA.read_word("ababbbaa")