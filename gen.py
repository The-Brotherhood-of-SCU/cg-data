import os
from typing import Dict, List
import json
import gzip
import shutil

def compress_file(input_file_path, output_gz_file_path):
    with open(input_file_path, 'rb') as f_in:
        with gzip.open(output_gz_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

os.makedirs("out",exist_ok=True)

files = [i for i in os.listdir("src") if i.endswith(".txt") or i.endswith(".json")]

raw_list=[]
for i in files:
    with open(f"src/{i}","r",encoding='utf-8') as f:
        raw=f.read()
        if i.endswith(".txt"):
            raw_list+=raw.split("\n\n")
        elif i.endswith(".json"):
            raw_list+=json.loads(raw)

class Entry:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer
        self.priority = 0
        
        index = answer.find("标准答案")
        if index != -1:
            index2 = answer.find("你的答案")
            if index2 != -1:
                self.answer = answer[:index2] + answer[index:]
            else:
                self.answer = answer
            self.priority = 1
        else:
            self.answer = answer

class Finder:
    def __init__(self, list_raw: List):
        self.dict: Dict[str, Entry] = {}
        self.handle_raw_text(list_raw)
        print(f'total entries {len(self.dict)}')
        #self.print_dict()

    def handle_raw_text(self, splited: List):
        for i in splited:
            index = i.find('\n')
            if index == -1 or index == 0:
                continue
            question = i[:index]
            answer = i[index:]
            if question in self.dict:
                if self.dict[question].priority < 1:
                    entry1 = Entry(question, answer)
                    if entry1.priority > 0:
                        self.dict[question] = entry1
            else:
                entry1 = Entry(question, answer)
                self.dict[question] = entry1

    def get_list_str(self):
        total = [v for v in self.dict.values()]
        return(json.dumps([entry.question+entry.answer for entry in total], ensure_ascii=False))

    def get_dict(self):
        return self.dict
    
finder=Finder(raw_list)

data_list=finder.get_list_str()

with open("out/data.json","w",encoding='utf-8') as f:
    f.write(data_list)

compress_file("out/data.json","out/data.json.gz")