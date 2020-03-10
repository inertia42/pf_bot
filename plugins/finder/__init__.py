from nonebot import on_command, CommandSession,get_bot
from nonebot import on_natural_language, NLPSession, IntentCommand
import re
from nonebot.helpers import render_expression as __

from .data_source import get_name_of_data ,convert_html_to_image
from datetime import timedelta
SESSION_RUN_TIMEOUT = timedelta(seconds=30) # 会话过时时间

__plugin_name__ = '数据查找'
__plugin_usage__ = r"""
查找法术

.c [法术名称]
"""


@on_command('c', aliases=(),only_to_me=False)
async def finder(session: CommandSession):
    keyword = session.get('keyword', prompt='请输入关键词') # 提取关键词
    finder_name = await get_name_of_data(keyword) # 搜索可匹配的数据
    convert_html_to_image(finder_name) # 将所选的数据转换成图片
    #await session.send(message="[CQ:image,file=out.jpg]")
    await session.send(__(("[CQ:image,file=out.jpg]",), **session.ctx)) # 发送图片


@finder.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip() # 清除空格
    stripped_arg = re.split(r'\s+',stripped_arg) # 将输入的关键词按空格分割

    if session.is_first_run:
        if stripped_arg:
            session.state['keyword'] = stripped_arg   # 将关键词赋给session
        return

    if not stripped_arg:
        session.pause('请重新输入')
    session.state[session.current_key] = stripped_arg
