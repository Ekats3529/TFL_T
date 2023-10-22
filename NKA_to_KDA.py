from NKA import NKAutomate
from KDA import KDAutomate
from queue import Queue


def print_new_names(lst):
    for st in lst.keys():
        print(f"new name: q{st: <3} previous states: {'|'.join(sorted(lst[st]))}")


def NKA_to_KDA(nka, kda):
    kda_states = {}
    new_names = {'0': list(nka.beg_state)}
    k = 1
    q = Queue()
    q.put(set(nka.beg_state))

    while not q.empty():
        cur_state = q.get()
        if list(new_names.values()).index(list(cur_state)) in kda_states.keys():
            continue

        for ch in nka.symbols:
            new_state = set()
            for state in cur_state:
                for st in nka.states[state][nka.symbols[ch]]:
                    new_state.add(st)

            if "-" in new_state and len(new_state) > 1:
                new_state.discard("-")

            key_state = sorted(list(new_state))

            if key_state not in list(new_names.values()):
                new_names[str(k)] = key_state
                k += 1

            if list(new_names.values()).index(list(cur_state)) not in kda_states.keys():
                kda_states[list(new_names.values()).index(list(cur_state))] = []

            kda_states[list(new_names.values()).index(list(cur_state))].append(
                list(new_names.values()).index(key_state))
            q.put(key_state)

    new_ends = []

    for state in new_names.keys():
        for x in new_names[state]:
            if x in nka.end_state:
                new_ends.append(state)
                break

    print_new_names(new_names)
    kda.set_beg_state(nka.beg_state)
    kda.set_states(kda_states)
    kda.set_end_state(new_ends)
    kda.set_symbols(nka.symbols)


nka = NKAutomate("input_NKA.txt")
kda = KDAutomate("input_KDA.txt")
nka.print_table()
NKA_to_KDA(nka, kda)
kda.print_table()
kda.read_word("ababbbcc")
