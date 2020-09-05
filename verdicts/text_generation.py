from importlib import reload
import ner
import pandas as pd
import re
from pandas import DataFrame
import numpy as np

template_path = '.\\template\\'
mapping_path = '.\\content_mapping\\'
result_path = '.\\result\\'
file_path = '.\\file\\'
contrast_path = '.\\contrast\\'

for index in range(8):
    template_object = open(template_path + 'template.txt', 'r', encoding='UTF-8')
    mapping_object = open(mapping_path + 'mapping' + str(index) + '.txt', 'r', encoding='UTF-8')
    result_object = open(result_path + 'result' + str(index) + '.txt', 'w', encoding='UTF-8')
    file_object = open(file_path + 'file' + str(index) + '.txt', 'r', encoding='UTF-8')
    contrast_object = open(contrast_path + 'contrast' + str(index) + '.txt', 'w', encoding='UTF-8')

    titles = []
    values = []
    for line in mapping_object:
        list = line.split("：")
        title = list[0]
        value = list[1].replace('\n', '')
        print(title)
        print(value)
        titles.append(title)
        values.append(value)

    print(titles)
    print(values)

    for line in template_object:
        flag = False
        if line.find('[' or ']') == -1:
            result_object.write(line)
            continue
        for i in range(len(titles)):
            if line.find(titles[i]) != -1:
                flag = True

                list = values[i].split("、")
                size = len(list)

                if ("审判长" in line) or ("审判员" in line) or ("人民陪审员" in line) or ("法官助理" in line) or ("书记员" in line):
                    new = line.replace('[' + titles[i] + ']', list[0])
                    if "&&&" not in new:
                        for k in range(1, size):  # 一个属性对应至少二个值
                            new += "&&&" + line.replace('[' + titles[i] + ']', list[k])
                        line = new
                    print("1:" + line)

                elif size == 1 or (size>1 and line.find("：") == -1):
                    if "出生日期" in titles[i]:  # 出生日期的特殊情况
                        new = line.replace('[' + titles[i] + ']', values[i] + "出生")
                    # elif "地址" in titles[i]:  # 住址的特殊情况
                    #     new = line.replace('[' + titles[i] + ']', "住所地" + values[i])
                    else:
                        new = line.replace('[' + titles[i] + ']', values[i])
                    line = new
                else:
                    temp = ""
                    num = line.count('[')  # 查看包含几个属性
                    for j in range(size):
                        new = line
                        for k in range(i, i+num):
                            list1 = values[k].split("、")
                            if titles[k] in new:
                                new = new.replace('[' + titles[k] + ']', list1[j])
                        temp += new
                    line = temp

        print(line)
        now = line

        if flag:
            while now.find('[' or ']') != -1:
                if "由[案件受理费承担方]负担" in now:
                    now = now.replace("由[案件受理费承担方]负担", "予以免收")
                else:
                    start = now.index('[')
                    end = now.index(']')
                    if now[start-1] == "，":
                        start -= 1
                    now = now.replace(now[start:end+1], '')
            print(now)
            ans = now.replace("&&&", "")
            result_object.write(ans)