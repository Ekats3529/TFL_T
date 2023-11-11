from NKA import NKAutomate
from EpsNKA import EpsNKAutomate


def EpsNKA_to_NKA(e_nka, nka):
    nka_states = {}
    nka_symbols = e_nka.symbols.copy()
    nka_ends = set(e_nka.end_state.copy())
    del nka_symbols['e']
    e_ind = e_nka.symbols['e']

    closure = e_nka.closure.copy()

    for state in closure.keys():
        clos_state = closure[state]
        for st in clos_state:
            if st in nka_ends:
                nka_ends.add(state)
        ind_state = list(e_nka.state_names.values()).index(state)
        new_state = []
        for ch in nka_symbols.values():
            cur_ch = set()
            for st in clos_state:
                ind = list(e_nka.state_names.values()).index(st)
                if st == "-":
                    continue
                for s in e_nka.states[ind][ch]:
                    cur_ch.add(s)
            if "-" in cur_ch and len(cur_ch) > 1:
                cur_ch.remove("-")
            new_state.append(sorted(list(cur_ch)))
        nka_states[ind_state] = new_state
    nka.set_symbols(nka_symbols)
    nka.set_end_state(nka_ends)
    nka.set_states(nka_states)
    nka.set_beg_state(e_nka.beg_state)
    nka.set_names(list(e_nka.state_names.values()))


e_nka = EpsNKAutomate("input_epsNKA_1.txt")
e_nka.print_table()
print("-----------------------------------------")
nka = NKAutomate("input_NKA.txt")
EpsNKA_to_NKA(e_nka, nka)
nka.print_table()
nka.read_word("000")
