'''
# @Author       : Chr_
# @Date         : 2022-02-12 19:25:26
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-17 09:14:44
# @Description  : 
'''


from aiogram.types.callback_query import CallbackQuery
from aiogram.types.input_media import InputMedia, MediaGroup
from aiogram.types.message import ParseMode
from aiogram.utils.markdown import escape_md, quote_html

from loguru import logger

from models.post import Posts, Post_Status
from buttons.submit import SubmitPostKey, gen_submit_keyboard
from buttons.review import RKH
from utils.fetch_tags import text_fatch_tagid

from config import CFG


async def handle_submit_post_callback(query: CallbackQuery):
    '''
    处理投稿按钮回调
    '''
    bot = query.bot
    msg = query.message

    chat_id = msg.chat.id
    msg_id = msg.message_id

    user = query.user

    post = await Posts.get_or_none(action_mid=msg_id)

    if not post:
        # 未找到投稿记录
        await query.answer('投稿不存在')
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text='投稿不存在',
            reply_markup=None
        )
        return

    elif post.status != Post_Status.Padding:
        # 投稿已经被处理
        await query.answer('请不要重复操作')
        status = Post_Status.describe(post.status)

        text = (
            f'稿件状态: `{status}`\n'
            '更多帮助: /help'
        )

        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=msg_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=None
        )
        return

    else:
        # 开始处理 data
        data = query.data

        if data == SubmitPostKey.anymouse:
            # 匿名/取消匿名
            anymouse = not post.anymouse
            post.anymouse = anymouse

            await query.answer('已开启匿名模式' if anymouse else '已关闭匿名模式')

            kbd = gen_submit_keyboard(anymouse)
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg_id, reply_markup=kbd)

        elif data == SubmitPostKey.cancel:
            # 取消投稿
            await query.answer('投稿已取消')

            post.update_from_dict({
                'caption': '',
                'status': Post_Status.Cancel,
                'source': '',
                'files': ''
            })
            await post.save()

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text='投稿已取消',
            )

        elif data == SubmitPostKey.post:
            # 投稿
            files = post.files

            if len(files) <= 1:
                # 单文件或者纯文本投稿, 直接转发消息到审核群
                review_mid = await bot.forward_message(
                    chat_id=CFG.Review_Group,
                    from_chat_id=chat_id,
                    message_id=post.origin_mid
                )

            else:
                # 多文件投稿, 需要创建媒体组
                media = MediaGroup()

                cap = post.raw_caption

                for file in files:
                    media.attach(InputMedia(
                        type=file.file_type,
                        media=file.file_id,
                        caption=cap
                    ))
                    cap = None

                review_mids = await bot.send_media_group(
                    chat_id=CFG.Review_Group,
                    media=media
                )

                # 只取第一个消息对象
                review_mid = review_mids[0]

            tagnum = text_fatch_tagid(post.raw_caption)

            kbd = RKH.gen_review_keyboard(tagnum)

            status = Post_Status.describe(Post_Status.Reviewing)

            anymouse = post.anymouse
            nm = "是" if anymouse else "否"

            text = (
                f'投稿人: {user.md_link()}\n\n'
                f'状态: `{status}`\n'
                f'匿名: `{nm}`\n'
                '更多帮助: /help'
            )

            manage_mid = await bot.send_message(
                chat_id=CFG.Review_Group,
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=kbd
            )

            post.update_from_dict({
                'anymouse_mode': anymouse,
                'status': Post_Status.Reviewing,
                'anymouse': anymouse,
                'review_mid': review_mid,
                'manage_mid': manage_mid,
                'tag': tagnum
            })

            await query.answer('稿件投递成功')

            user.prefer_anymouse = anymouse
            user.post_count += 1
            await user.save()

            text = (
                f'状态: `{status}`\n'
                f'匿名: `{nm}`\n'
                f'采用数: `{user.accept_count}`\n'
                f'总投稿: `{user.post_count}`\n'
                '更多帮助: /help'
            )

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=text,
                parse_mode=ParseMode.MARKDOWN
            )

        else:

            logger.debug(f'未知操作: {query.data}')

            await query.answer('未知操作')
            await bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=msg_id,
                reply_markup=None
            )
            return

        await post.save()
