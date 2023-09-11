class Automate:
    states = []
    symbols = []
    auto_type = ""

    def __init__(self, filename):
        with open(filename) as file:
            self.symbols = file.readline()
            self.states = file.readlines()
            for k in range(len(self.states)):
                self.states[k] = self.states[k].split()

    def print_table(self):
        print("\t", end="")
        chars = "  ".join(self.symbols)
        print(chars)
        for i in range(len(self.states)):
            tmp = "    ".join([f"q{k}" if k != "-" else "- " for k in self.states[i]])
            print(f'q{i}\t{tmp}')

    def is_valid(self, word):
        pass

    def read_word(self, word):
        for ch in word:
            pass


if __name__ == "__main__":
    KDA = Automate("input.txt")
    KDA.print_table()
    KDA.read_word()





