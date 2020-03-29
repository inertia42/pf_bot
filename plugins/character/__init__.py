from nonebot import on_command, CommandSession,logger
from nonebot import on_natural_language, NLPSession, IntentCommand
from .moudles import *
import pdb
from nonebot.argparse import ArgumentParser
import pickle
import os
import re
from .characters import *

USAGE = r"""
char [-a] [-l] [-h]

使用方法：
char    无参数，用于列出默认角色的所有信息
char -a 用于交互式添加新角色
char -l 用于列出已有角色及其序号
char -h 用于列出使用帮助
""".strip()

HELP = r"""
可用命令：

char [-a --add] [-l list] [-s --switch] [-h --help] 用于创建、修改角色相关信息，具体帮助请使用char -h 命令查看
""".strip()

# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('help')
async def help(session: CommandSession):
    await session.send(HELP)
    return

@on_command('name', aliases=('名字', '天气预报', '查天气'))
async def location(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    # city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    # 获取城市的天气预报
    # weather_report = await get_weather_of_city(city)
    # 向用户发送天气预报
    # data=session.ctx
    # pdb.set_trace()
    # name=data.get('user_id')
    name_report="您的QQ号是"+str(get_qq(session))

    await session.send(name_report)
@on_command('char',only_to_me=False)
async def char(session: CommandSession):
    stripped_arg_raw = session.state['args']
    if not session.state['arg']:
        target_id = get_target_id(session)
        logger.debug("The target_id is "+target_id)
        logger.debug(session.ctx)
        default = Character(session,str(target_id))
        default_char = default.get_default()
        output = '''姓名：%s
性别：%s  阵营：%s
职业：%s
人物属性：%s
生命值：%s  经验值：%s
现金：%s  负重：%s
人物背景：%s
道具：%s
声望：%s'''%(default_char['name'],default_char['gender'],default_char['alignment'],default_char['class'],
        default_char['ability'],default_char['hp'],default_char['xp'],default_char['money'],default_char['weight'],
        default_char['background'],default_char['loot'],default_char['reputation'])
        session.finish(output)
    if session.state['arg'] == '-h':
        session.finish(USAGE)
        
    if session.state['arg'] == '-a':
        if session.is_first_run:
            session.state['data']=dict()
            session.pause('请输入人物名称')
        if re.match(r"谢谢",stripped_arg_raw):
            session.finish("已停止建立人物")
        char_data = session.state['data']
        char_data = get_input_data(char_data,['name',"种族"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['race',"性别"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['gender',"阵营"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['alignment',"职业及等级"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['class',"人物属性"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['ability',"生命值或生命骰"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['hp',"现有经验值"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['xp',"现有道具，如果没有可以填无"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['loot',"负重情况"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['weight',"现金数量"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['money',"简要的人物背景和性格描述"],session,stripped_arg_raw)
        char_data = get_input_data(char_data,['background',"声望值，若未获得声望值请填0"],session,stripped_arg_raw)
        if 'reputation' not in char_data:
            char_data['reputation'] = stripped_arg_raw
        new = Character(session,str(session.ctx['user_id']))
        new.save(char_data)
        new.save_new_to_file()
        session.finish("已建立人物")
    if session.state['arg'] == '-l':
        new = Character(session,str(session.ctx['user_id']))
        print(session.ctx)
        char_list = new.get_list()
        output = '第一个为默认角色\n'
        for i,char_name in enumerate(char_list):
            output+="%d.%s\n"%(i+1,char_name)
        session.finish(output)

@char.args_parser
async def _(session: CommandSession):
    stripped_arg_raw = session.current_arg_text.strip() # 清除空格
    session.state['args'] = stripped_arg_raw
    if session.is_first_run:
        session.state['arg'] = stripped_arg_raw
            
def get_input_data(char_data,info,session,arg):
    if info[0] not in char_data:
        char_data[info[0]] = arg
        session.pause("请输入%s"%info[1])
    return char_data

def get_target_id(session):
    raw_text = session.ctx['raw_message']
    if len(re.findall(r"CQ:at",raw_text))>0:
        return re.findall(r"(\d+)\b",raw_text)[0]
    else:
        return session.ctx['user_id']