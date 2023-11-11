class EpsNKAutomate:
    states = {}
    symbols = {}
    state_names = {}
    beg_state = None
    end_state = None
    closure = {}

    def clear_all(self):
        self.states.clear()
        self.symbols.clear()
        self.beg_state = None
        self.end_state = None
        self.state_names.clear()

    def __init__(self, filename):
        with open(filename) as file:
            self.clear_all()
            # read symbols of language
            symbols = file.readline()
            k = 0
            for ch in symbols.split():
                self.symbols[ch] = k
                k += 1

            # read names of states
            names = file.readline().split()
            for k in range(len(names)):
                self.state_names[k] = names[k]

            # read transitions
            tmp = file.readline().split()
            self.beg_state = tmp[0]
            self.end_state = tmp[1].split("|")
            states = file.readlines()
            for k in range(len(states)):
                self.states[k] = [state.split("|") for state in states[k].split()]
        self.init_closure()

    def init_closure(self):
        e_ind = self.symbols['e']

        for k in range(len(self.state_names)):
            cur_state = self.states[k][e_ind]
            clos = set()
            for st in cur_state:
                if st == '-':
                    break
                clos.add(st)
            clos_ext = set()
            for st in clos:
                ind = list(self.state_names.values()).index(st)
                cur_state = self.states[ind][e_ind]
                for state in cur_state:
                    if state == "-":
                        break
                    clos_ext.add(state)
            clos = clos.union(clos_ext)
            clos.add(self.state_names[k])
            self.closure[self.state_names[k]] = clos

    def print_closure(self):
        for clos in self.closure.keys():
            print(f"{clos}: {self.closure[clos]}")

    def print_table(self):
        print("\t\t", end="")
        sp = " " * 10
        chars = sp.join(self.symbols.keys())
        print(chars)
        for i in range(len(self.states)):
            if self.state_names[i] in self.beg_state:
                print("->", end="")
            else:
                print("  ", end="")
            if self.state_names[i] in self.end_state:
                print("* ", end="")
            else:
                print("  ", end="")
            tmp = ""
            for lst in self.states[i]:
                if "-" in lst:
                    tmp += f"{'-' : <10}"
                else:
                    tmp += f'{"|".join([f"q{k}" for k in lst]): <10}'
            print(f'q{self.state_names[i]}\t{tmp}')

    def read_word(self, word):
        print(f"The word: {word}")
        cur_state = set(self.beg_state)
        cur_closure = self.closure[self.beg_state]
        for ch in word:
            if ch not in self.symbols.keys():
                print(f"Unexpected symbol {ch}")
                print(f"The {word} NOT in language")
                return
            new_state = set()
            new_closure = set()
            for cl in cur_closure:
                new_closure = new_closure.union(self.closure[cl])
            for st in new_closure:
                ind = list(self.state_names.values()).index(st)
                tmp = set(self.states[ind][self.symbols[ch]])
                new_state = new_state.union(tmp)
            new_state.discard("-")
            if len(new_state) == 0:
                print(f"The end state q{cur_state}")
                print(f"The {word} NOT in language")
                return

            print(f"q{cur_state} --- {ch} ---> q{new_state}")
            cur_state = new_state
            cur_closure = new_state

        for st in cur_state:
            if st in self.end_state:
                print(f"The {word} in language")
                return

        for st in cur_closure:
            if st in self.end_state:
                print(f"The {word} in language")
                return
        print(f"The {word} NOT in language")


if __name__ == "__main__":
    nka = EpsNKAutomate("input_epsNKA_1.txt")
    nka.print_table()
    nka.print_closure()
    print("----------------------------------")
    nka.read_word("")

