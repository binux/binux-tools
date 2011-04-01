# coding: utf-8
import mmseg
#mmseg.dict_load_defaults()
#mmseg.dict_load_words("data/words.dic")
mmseg.dict_load_words("../data/remove_list.dic")
while True:
    a = raw_input()
    for tk in mmseg.Algorithm(a.decode("utf-8").encode("utf-8")):
        print tk.text, repr(tk.text), tk.attr
