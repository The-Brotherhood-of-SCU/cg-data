import re
import json

print("file name is similar to 'Year-Nickname-count'")
print("eg. 2024-57u-1")
file_name=input("Input-file-name: ")
if not file_name.endswith(".json"):
    file_name=file_name+".json"

#input the ocr info here 
ocr=r"""

"""

ocr=ocr.replace("\n\n",'\n')

pattern=r"\d\d?、\["


match = re.search(pattern, ocr)

# 如果找到匹配项，获取匹配项后面的所有内容
if match:
    # 获取匹配项的结束位置
    end_position = match.end()
    # 获取匹配项后面的所有内容
    ocr = ocr[end_position:]

result = re.split(pattern, ocr)

pattern_remove=[
    "判断题]",
    "单选题]",
    r"[(（]?分?\n*?值?[(（]分值2[）)][）)]",
    r"[(（][）)]",
    r"[(（]\n?分值",
    r"[(（]\n值2[）)][）)]"
    ]
result2=[]
for line in result:
    for pattern in pattern_remove:
        line=(re.sub(pattern, "", line))
    result2.append(line)

j=json.dumps(result2,indent=2, ensure_ascii=False)

with open("src/"+file_name,"w",encoding='utf-8') as f:
    f.write(j)
