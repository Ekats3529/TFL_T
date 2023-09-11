class Automate:
    states = {}
    symbols = {}
    auto_type = ""

    def __init__(self, filename):
        with open(filename) as file:
            symbols = file.readline()
            k = 0
            for ch in symbols.split():
                self.symbols[ch] = k
                k += 1
            states = file.readlines()
            for k in range(len(states)):
                self.states[k] = states[k].split()

    def print_table(self):
        print("\t", end="")
        chars = "\t".join(self.symbols.keys())
        print(chars)
        for i in range(len(self.states)):
            tmp = "    ".join([f"q{k}" if k != "-" else "- " for k in self.states[i]])
            print(f'q{i}\t{tmp}')

    def read_word(self, word):
        print(f"The word: {word}")
        cur_state = 0
        for ch in word:
            if ch not in self.symbols.keys():
                print(f"Unexpected symbol {ch}")
                print(f"The {word} not in language")
                return
            new_state = self.states[cur_state][self.symbols[ch]]
            if new_state != '-':
                print(f"q{cur_state} --{ch}--> q{new_state}")
                cur_state = int(new_state)
            else:
                print(f"The end state q{cur_state}")
                print(f"The {word} not in language")
                return
        print(f"The {word} in language")


if __name__ == "__main__":
    KDA = Automate("input.txt")
    KDA.print_table()
    print()
    KDA.read_word("bac")




