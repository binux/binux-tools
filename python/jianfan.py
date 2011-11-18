#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ["ftoj", "jtof"]

# 最大正向匹配
def conv(string, dic):
    if isinstance(string, unicode):
        is_unicode = True
    else:
        is_unicode = False
        string = string.decode("utf-8")

    i = 0
    default = (1, )
    result = []
    while i < len(string):
        t = None
        for j in dic['_pretest'].get(string[i], default):
            if string[i:i+j] in dic:
                t = dic[string[i:i+j]]
                result.append(t)
                i += j
                break
        if t is None:
            result.append(string[i])
            i += 1

    string = "".join(result)
    if not is_unicode:
        string = string.encode("utf-8")

    return string

def prefix(dic):
    result = {}
    for key in dic:
        if len(key) == 1:
            continue
        result.setdefault(key[0], set((1, )))
        result[key[0]].add(len(key))
    for key in result:
        result[key] = sorted(result[key], reverse=True)
    dic['_pretest'] = result
    return dic
 
# 生成转换字典
def mdic(dict_path, *rule):
    import os.path
    table = open(os.path.join(os.path.dirname(__file__), dict_path),'r').readlines()
    dic = {}
    name = {}
    for line in table:
        if line[0] == '$':
            dic = {}
            name[line.split("=")[0].strip()[1:]] = dic
        if line[0] == "'":
            word = line.decode("utf-8").split("'")
            dic[word[1]] = word[3]
    name["zh2TW"].update(name["zh2Hant"]) # 简繁通用转换规则(zh2Hant)加上台湾区域用法(zh2TW)
    name["zh2HK"].update(name["zh2Hant"]) # 简繁通用转换规则(zh2Hant)加上香港区域用法(zh2HK)
    name["zh2CN"].update(name["zh2Hans"]) # 繁简通用转换规则(zh2Hans)加上大陆区域用法(zh2CN)

    if len(rule) == 1:
        return prefix(name[rule[0]])
    result = []
    for each in rule:
        result.append(prefix(name[each]))
    return result

dic_CN, dic_TW = mdic("ZhConversion.php", "zh2CN", "zh2TW")
def jtof(string):
    return conv(string, dic_TW)
def ftoj(string):
    return conv(string, dic_CN)
 
if __name__=="__main__":
    a="头发发展萝卜卜卦秒表表达 "
    b="大衛碧咸在寮國見到了布希"
    c="大卫·贝克汉姆在老挝见到了布什"
 
    [dic_TW,dic_HK,dic_CN] = mdic('data/ZhConversion.php', "zh2TW", "zh2HK", "zh2CN")
    str_TW = conv(a,dic_TW)
    str_HK = conv(c,dic_HK)    
    str_CN = conv(b,dic_CN)
    print a, ' < -> ', str_TW, '\n', c, ' < -> ',str_HK,'\n', b,' < -> ',str_CN

