import Levenshtein
import docx
import re

for i in range(8):
    file = open('.\\file\\file' + str(i) + '.txt', 'r', encoding='UTF-8')
    original = ""
    for line in file:
        original += line.replace("\n", "")
    print(original)
    print(len(original))

    produce = open('.\\result\\result' + str(i) + '.txt', 'r', encoding='UTF-8')
    new = ""
    for line in produce:
        new += line.replace("\n", "")
    print(new)
    print(len(new))

    levenshtein = Levenshtein.distance(original, new)
    print("编辑距离{0}:{1}".format(i, levenshtein))
    print("相似度{0}：{1}".format(i, (len(new)-levenshtein)/len(new)))
    print("\n")