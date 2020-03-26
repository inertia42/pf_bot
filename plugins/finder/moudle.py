import pickle
import re
import copy
import imgkit
import pymysql.cursors
from nonebot import logger
import os

async def get_name_of_data(keywords: list):
    '''
    输入参数为数组，内容为搜索关键词。
    '''
    connection = pymysql.connect(host='127.0.0.1',
    user='pfbot',
    password='pfbot',
    db='pathfinder',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
    logger.debug(keywords)
    try:
        sql = ''
        with connection.cursor() as cursor:
            for i,subtitle in enumerate(keywords):
                args = '%'+subtitle+'%'
                if i==0:
                    sql+="select * from data where name like '%s'"%args
                else:
                    sql+="and name like '%s'"%args
            cursor.execute(sql) 
            result = cursor.fetchall()
            logger.debug(len(result))
        connection.commit()
    finally:
        connection.close()
        return result

def convert_html_to_image(session):
    '''
    输入参数为数组，内容为匹配到的数据名称。
    
    将选定的数据转换为图片
    '''
    data = session.state['final']
    # img_id = str(data['id'])
    img_id = data['name']
    img_id=re.sub(r'/','',img_id) #去除数据名中可能带有的"/"符号
    img_path = "/dcoolq/data/image/pf_finder/%s.jpg"%img_id
    if os.path.exists(img_path):
        return img_id
    else:
        text = data['raw']
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
        imgkit.from_string(text,img_path,options=options)
        return img_id