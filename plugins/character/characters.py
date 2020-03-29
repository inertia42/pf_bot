import json 
from collections import deque

class Character(object):

    def __init__(self,session,id):
        self.id = id
        self.data = dict()
        self.before_data = None
        self.session = session
        self.__load()
    
    def __load(self):
        try:
            with open('data/characters/%s.json'%self.id, 'r') as f: 
                self.before_data = json.load(f)
        except:
            self.before_data=[]
        return
    
    def save(self,input_data):
        self.data = input_data
        return
    
    def get_list(self):
        if not self.before_data:
            self.session.finish("未录入任何人物信息!")
        char_list = []
        
        for datas in self.before_data:
            char_list.append('-'.join((datas['race'],datas['class'],datas['name'])))
        return char_list

    def get_default(self):
        if not self.before_data:
            self.session.finish("未录入任何人物信息!")
        return self.before_data[0]
    
    def change(self,number):
        if number+1>len(self.before_data):
            self.session.finish("该序号对应的人物不存在！")
        self.before_data[number],self.before_data[1] = self.before_data[1],self.before_data[number]  
        self.session.finish("修改完毕")
        return

    def save_new_to_file(self):
        self.before_data=deque(self.before_data)
        self.before_data.appendleft(self.data)
        with open('data/characters/%s.json'%self.id, 'w+') as f: 
            self.before_data = list(self.before_data)
            json.dump(self.before_data,f,ensure_ascii=False,indent=4)
        return
    
    def save_to_file(self):
        self.before_data[0]=self.data
        return
        
        
