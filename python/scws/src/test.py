#!python
#coding: utf-8

import scws_py

def main():
  s = scws_py.SCWS()
  text = "Hello, 我名字叫李那曲是一个中国人, 我有时买Q币来玩, 我还听说过C#语言"

  s.set_charset("utf-8")
  s.add_dict("dict.utf8.xdb", 0)
  s.set_rule("rules.utf8.ini")

  s.send_text(text, len(text))
  assert(s.has_word("n") == 1)

  print "============================"
  a = s.get_result()
  for e in a:
    print (text[e.off:e.off+e.len]), e.idf, e.attr

  print "============================"
  b = s.get_tops(100, None)
  for e in b:
    print (e.word), e.weight, e.times, (e.attr)

  print "============================"
  c = s.get_words("n")
  for e in b:
    print (e.word), e.weight, e.times, (e.attr)

if __name__ == "__main__":
  main()

  

