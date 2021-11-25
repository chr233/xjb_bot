'''
# @Author       : Chr_
# @Date         : 2021-11-02 14:25:18
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-26 01:24:31
# @Description  : 审核投稿
'''

from aiogram.types import chat
from aiogram.types import InputFile
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.input_media import InputMedia, MediaGroup
from aiogram.types.message import ParseMode
from aiogram.utils.markdown import escape_md
from buttons.review import RKH, ReviewPostKey

from models.post import Posts, Post_Status, PublicPosts

from config import CFG
from utils.emojis import NO, YES


async def handle_review_post_callback(query: CallbackQuery):

    data = query.data
    bot = query.bot

    chat_id = query.message.chat.id
    msg_id = query.message.message_id

    user = query.user

    try:
        cmd, selected = data.split(' ')
        selected = int(selected)
    except ValueError:
        cmd = data.strip()
        selected = 0
        # return

    print(f'cmd: {cmd}, selected: {selected}')

    post = await Posts.get_or_none(manage_mid=msg_id)

    if not post:
        await query.answer('投稿不存在')
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text='投稿不存在',
        )
        return

    if post.status != Post_Status.Reviewing:
        await query.answer('请不要重复操作')
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=msg_id,
        )

    if cmd == ReviewPostKey.tag:

        keyboard = await RKH.get_tag_keyboard_short(selected)

        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=msg_id,
            reply_markup=keyboard
        )

    else:

        if cmd == ReviewPostKey.reject:
            return

            # await RejectPosts.create(
            #     post = post,
            #     reviewer = user,

            # )

        if cmd == ReviewPostKey.accept:
            caption = []

            tags = await RKH.get_tag(selected)

            if tags:
                caption.append(escape_md(tags))

            cap = post.caption

            if cap:
                caption.append(cap)

            if len(caption) > 0:
                caption.append('')

            src = post.source
            if src:
                caption.append(f'from [{src.name[:15]}]({src.url})')
            else:
                if not post.anymouse:
                    caption.append(f'via {post.tags} ')
                # else:
                    # source = ''

            files = post.files

            caption = ('\n'.join(caption)).strip()

            if not files:  # 纯文本消息
                post_mid = await bot.send_message(
                    chat_id=CFG.Accept_Channel,
                    text=caption,
                    parse_mode=ParseMode.MARKDOWN_V2,
                )

            elif len(files) == 1:
                file = files[0]
                ftype = file.file_type

                if ftype == 'photo':
                    post_mid = await bot.send_photo(
                        chat_id=CFG.Accept_Channel,
                        photo=file.file_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN_V2
                    )

                elif ftype == 'video':
                    post_mid = await bot.send_video(
                        chat_id=CFG.Accept_Channel,
                        video=file.file_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
                elif ftype == 'audio':
                    post_mid =await bot.send_audio(
                        chat_id=CFG.Accept_Channel,
                        audio=file.file_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
                elif ftype == 'document':
                    post_mid =await bot.send_document(
                        chat_id=CFG.Accept_Channel,
                        document=file.file_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN_V2
                    )
                else:
                    post_mid = await bot.send_document(
                        chat_id=CFG.Accept_Channel,
                        document=file.file_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN_V2
                    )

            else:
                media = MediaGroup()

                for file in files:
                    media.attach(InputFile(
                        type=file.file_type,
                        media=file.file_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN_V2
                    ))
                    caption = None

                post_mids = await bot.send_media_group(
                    chat_id=CFG.Review_Group,
                    media=media
                )

                # 只取第一个消息对象
                post_mid = post_mids[0]

            post.tags = ''
            post.status = Post_Status.Accepted
            await user.save()

            await PublicPosts.create(
                message_id=post_mid.message_id,
                post=post,
                reviewer=user,
            )

            p_user = await post.poster.get()

            print(p_user)

        user.review_count += 1
        await user.save()
        await post.save()
