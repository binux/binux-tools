# coding: utf-8
import mmseg
#mmseg.dict_load_defaults()
mmseg.dict_load_words("../data/remove_list.dic")
a = "虚空之门"
print repr(a)
print repr(a.decode("utf-8"))
print repr(a.decode("utf-8").encode("utf-8"))
#for tk in mmseg.Algorithm("虚空之门"):
b = a.decode("utf-8")
for tk in mmseg.Algorithm(a.decode("utf-8").encode("utf-8")):
    print tk.text, repr(tk.text), tk.attr
for tk in mmseg.Algorithm("一无"):
    print tk.text, tk.attr
