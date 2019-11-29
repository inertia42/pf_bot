from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from .moudles import *
import pdb
from nonebot.argparse import ArgumentParser
import pickle
import os
import re

USAGE = r"""
char [-a --add] [-l list] [-s --switch] [-h --help]

使用方法：
char -a [角色名称] 用于添加新角色的名称
char -l list 用于列出已有角色及其序号
char -s [角色序号] 用于更换默认角色，输入的角色序号对应于想要设置的默认角色
char -h 用于打印使用帮助
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
@on_command('char', shell_like=True,only_to_me=False)
async def _(session: CommandSession):
    parser = ArgumentParser(session=session ,usage=USAGE)
# 设定参数，add为添加新角色使用，list为列出新角色用
    parser.add_argument('-a','--add')
    parser.add_argument('-l','--list')
    parser.add_argument('-s','--switch')

    #pdb.set_trace()
    args = parser.parse_args(session.argv)
    filename="data/"+str(get_qq(session))+'.dat' #设置储存角色信息的文件名
    if args.add:
        if not os.path.isfile(filename): #判断文件是否存在
            f = open(filename, 'wb')
            # character_data={'default':1,1:{'name':args.add}j}
            character_data=[-1,{'name':args.add}]
            pickle.dump(character_data,f)
            f.close()
            await session.send("成功添加")
            return
        else:
            f = open(filename,'rb')
            character_data=pickle.load(f)
            f.close()
            f = open(filename,'wb')
            character_data.append({'name':args.add})
            pickle.dump(character_data,f)
            f.close()
            await session.send("成功添加")
            return
    
    if args.list:
        if not os.path.isfile(filename):
            await session.send("无角色信息")
            return
        else:
            f = open(filename,'rb')
            character_data=pickle.load(f)
            f.close()
            name_report=""
            for i in range(len(character_data)):
                if i==0:
                    name_report=name_report+"默认角色："+character_data[character_data[0]]['name']
                else:
                    name_report=name_report+'\n'+str(i)+". "+character_data[i]['name']
            await session.send(name_report)
            return

    if args.switch:
        if not os.path.isfile(filename):
            await session.send("无角色信息")
            return
        else:
            if not re.match(r'[0-9]', args.switch):
                await session.send('请使用角色对应的数字序号，具体的序号请使用char -l list 命令查询')
                return
            f = open(filename,'rb')
            character_data=pickle.load(f)
            f.close()
            character_data[0]=int(args.switch)
            f=open(filename,'wb')
            pickle.dump(character_data,f)
            f.close()
            await session.send("已成功修改默认角色")
            return

    



# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
# @location.args_parser
# async def _(session: CommandSession):
    # # 去掉消息首尾的空白符
    # stripped_arg = session.current_arg_text.strip()

    # if session.is_first_run:
        # # 该命令第一次运行（第一次进入命令会话）
        # if stripped_arg:
            # # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # # 例如用户可能发送了：天气 南京
            # session.state['city'] = stripped_arg
        # return

    # if not stripped_arg:
        # # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        # session.pause('要查询的城市名称不能为空呢，请重新输入')

    # # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    # session.state[session.current_key] = stripped_arg


async def get_weather_of_city(city: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    return f'{city}的天气是……'

# def get_qq(session):
    # qq=session.ctx.get('user_id')
    # return qq


@on_natural_language(keywords={'名字'},only_to_me=False)
async def _(session: NLPSession):
    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'location')
