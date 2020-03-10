import pickle
import re
import copy
import imgkit

async def get_name_of_data(keywords: list):
    '''
    输入参数为数组，内容为搜索关键词。
    '''
    f = open('data/finder/crb_name','rb')
    data_names = pickle.load(f)
    f.close()
    for keyword in keywords:  # 遍历关键词
        data_names_copy=copy.deepcopy(data_names)
        pattern = re.compile(r'%s'%keyword)
        for spell_name in data_names: # 遍历搜索所有的法术
            if not pattern.search(spell_name[0]):
                data_names_copy.remove(spell_name)
        data_names=copy.deepcopy(data_names_copy)
    return data_names 

def convert_html_to_image(data_name: list):
    '''
    输入参数为数组，内容为匹配到的数据名称。
    
    将选定的数据转换为图片
    '''
    number = data_name[0][1]
    f=open('data/finder/crb_new','rb')
    raw_text=pickle.load(f)
    f.close()
    text=raw_text[number]
    aa='''<html>
    <meta http-equiv="Content-Type" content="text/Html; charset=utf-8" />
    <head>'''
    text=aa+text
    options = {
        'width': 512,
        'quality': 100,
        'quiet': '',
        'xvfb': '',
        'encoding': 'utf8'
        }
    imgkit.from_string(text,'/dcoolq/data/image/out.jpg',options=options)
    return