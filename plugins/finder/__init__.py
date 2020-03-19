from nonebot import on_command, CommandSession,get_bot,logger
from nonebot import on_natural_language, NLPSession, IntentCommand
import re
from nonebot.helpers import render_expression as __


from .moudle import get_name_of_data ,convert_html_to_image
from datetime import timedelta
SESSION_RUN_TIMEOUT = timedelta(seconds=10) # 会话过时时间

__plugin_name__ = '数据查找'
__plugin_usage__ = r"""
查找法术

.c [法术名称]
"""


@on_command('c', aliases=(),only_to_me=False)
async def finder(session: CommandSession):
    keyword = session.get('keyword', prompt='请输入关键词') # 提取关键词
    try:
        if session.state['name']:
            pass
    except:
        session.state['name'] = None
    if not session.state['name']:
        session.state['name'] = await get_name_of_data(keyword) # 搜索可匹配的数据
        await check_the_list(session)
    img_name = convert_html_to_image(session) # 将所选的数据转换成图片
    img_name = re.sub(r'&','&amp;',img_name)
    img_name = re.sub(r',','&#44;',img_name)
    img_name = re.sub(r'\]','&#93;',img_name)
    img_name = re.sub(r"\[",'&#91;',img_name)
    await session.send(message=r"[CQ:image,file=pf_finder/%s.jpg]"%img_name)
    #await session.send(__(("[CQ:image,file=pf_finder/%s.jpg]"%img_name,), **session.ctx)) # 发送图片
    logger.info('Send a image')


@finder.args_parser
async def _(session: CommandSession):
    stripped_arg_raw = session.current_arg_text.strip() # 清除空格
    stripped_arg = re.split(r'\s+',stripped_arg_raw) # 将输入的关键词按空格分割
    logger.debug("The keyword is splited to"+str(stripped_arg))

    if session.is_first_run:
        if stripped_arg[-1]:
            session.state['keyword'] = stripped_arg   # 将关键词赋给session
        return
    if not stripped_arg_raw:
        session.pause('请重新输入')
    try:
        if session.state['name']:
            pass
    except:
        session.state['name'] = None
    if not session.state['name']:
        session.state['keyword'] = stripped_arg
    elif len(stripped_arg)==1 and re.match(r'\d+$',stripped_arg_raw): 
        if int(stripped_arg_raw) > len(session.state['name']):
            session.pause('超出上限，请重新输入')
        session.state['final'] = session.state['name'][int(stripped_arg_raw)-1]
    else:
        session.pause('请重新输入')
    
async def check_the_list(session:CommandSession):
    data_name = session.state['name']
    data_len = len(data_name)
    if data_len == 0:
        session.finish('未查找到相关内容，请更换关键词后再次尝试。')
    elif data_len == 1:
        session.state['final']=data_name[0]
        return 
    else:
        reply="查找到了%d项结果\n"%data_len
        for i,name in enumerate(data_name):
            reply+="%d.%s\n"%(i+1,name['name'])
            if i == 12:
                reply+="匹配项太多，请更换关键词后重新查询"
                session.finish(reply)
        reply+="请直接输入需要查询的序号"
        session.pause(reply)
    