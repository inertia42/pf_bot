from nonebot import on_command, CommandSession,get_bot
from nonebot import on_natural_language, NLPSession, IntentCommand
import re
from nonebot.helpers import render_expression as __

from .data_source import get_name_of_data ,convert_html_to_image
from datetime import timedelta
SESSION_RUN_TIMEOUT = timedelta(seconds=30)

bot = get_bot()
__plugin_name__ = '数据查找'
__plugin_usage__ = r"""
查找法术

.c [法术名称]
"""


@on_command('c', aliases=(),only_to_me=False)
async def finder(session: CommandSession):
    qun=session.ctx['group_id']
    keyword = session.get('keyword', prompt='请输入关键词')
    finder_name = await get_name_of_data(keyword)
    convert_html_to_image(finder_name)
    #await session.send(message="[CQ:image,file=out.jpg]")
    await session.send(__(("[CQ:image,file=out.jpg]",), **session.ctx))
    #await bot.send_msg(group_id=qun,message="[CQ:image,file=out.jpg]")
        # await session.send('请重新输入关键词')


@finder.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    stripped_arg = re.split(r'\s+',stripped_arg)

    if session.is_first_run:
        if stripped_arg:
            session.state['keyword'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('请重新输入')
    session.state[session.current_key] = stripped_arg


# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
