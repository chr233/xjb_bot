'''
# @Author       : Chr_
# @Date         : 2022-02-12 19:24:27
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-21 15:06:16
# @Description  : 
'''

from aiogram.types import chat
from aiogram.types import InputFile
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.input_media import InputMedia, MediaGroup
from aiogram.types.message import ParseMode
from aiogram.utils.markdown import escape_md
from buttons.direct import DirectPostKey, DKH
from models.base_model import SourceLink

from models.post import Posts, Post_Status, PublicPosts

from config import CFG
from utils.emojis import NO, YES
from utils.fetch_tags import str_fetch_tagid, tagid_fetch_text


async def handle_direct_post_callback(query: CallbackQuery):
    '''
    处理投稿按钮回调
    '''
    bot = query.bot
    msg = query.message

    chat_id = msg.chat.id
    msg_id = msg.message_id

    user = query.user

    post = await Posts.get_or_none(manage_mid=msg_id)

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

    if post.status != Post_Status.Padding:
        # 投稿已经被处理
        await query.answer('请不要重复操作')
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=msg_id,
            reply_markup=None
        )
        return

    else:
        # 开始处理 data
        data = query.data

        anymouse = post.anymouse

        if data.startswith(DirectPostKey.tag):

            tag = str_fetch_tagid(data)

            tagnum = post.tags ^ tag
            post.tags = tagnum
            await post.save()

            kbd = await DKH.gen_direct_keyboard(tagnum, anymouse)

            await bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=msg_id,
                reply_markup=kbd
            )

        elif data == DirectPostKey.cancel:
            # 取消发布

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

        elif data == DirectPostKey.post:
            # 确认发布

            post_caption = []

            tag_str = tagid_fetch_text(post.tags)
            if tag_str:
                post_caption.append(tag_str)

            caption = post.caption
            if caption:
                post_caption.append(caption)

            if len(post_caption) > 0:
                post_caption.append('')

            source =SourceLink(name= post.source_name,id=post.source_id)

            s_link = source.md_link()
            u_link = user.md_link()

            if post.forward:
                if not anymouse:
                    post_caption.append(f'from {s_link} via {u_link}')
                else:
                    post_caption.append(f'from {s_link}')

            elif not anymouse:
                post_caption.append(f'via {u_link} ')

            files = post.files

            text = ('\n'.join(post_caption)).strip()

            if not files:  # 纯文本消息
                post_mid = await bot.send_message(
                    chat_id=CFG.Accept_Channel,
                    text=text,
                    parse_mode=ParseMode.MARKDOWN,
                )

            elif len(files) == 1:
                file = files[0]
                ftype = file.file_type

                # if ftype == 'photo':
                #     post_mid = await bot.send_photo(
                #         chat_id=CFG.Accept_Channel,
                #         photo=file.file_id,
                #         caption=post_caption,
                #         parse_mode=ParseMode.MARKDOWN
                #     )

                # elif ftype == 'video':
                #     post_mid = await bot.send_video(
                #         chat_id=CFG.Accept_Channel,
                #         video=file.file_id,
                #         caption=post_caption,
                #         parse_mode=ParseMode.MARKDOWN
                #     )
                # elif ftype == 'audio':
                #     post_mid = await bot.send_audio(
                #         chat_id=CFG.Accept_Channel,
                #         audio=file.file_id,
                #         caption=post_caption,
                #         parse_mode=ParseMode.MARKDOWN
                #     )
                # elif ftype == 'document':
                #     post_mid = await bot.send_document(
                #         chat_id=CFG.Accept_Channel,
                #         document=file.file_id,
                #         caption=post_caption,
                #         parse_mode=ParseMode.MARKDOWN
                #     )
                # else:
                #     post_mid = await bot.send_document(
                #         chat_id=CFG.Accept_Channel,
                #         document=file.file_id,
                #         caption=post_caption,
                #         parse_mode=ParseMode.MARKDOWN
                #     )

            else:
                ...
                # media = MediaGroup()

                # for file in files:
                #     media.attach(InputFile(
                #         type=file.file_type,
                #         media=file.file_id,
                #         caption=post_caption,
                #         parse_mode=ParseMode.MARKDOWN
                #     ))
                #     post_caption = None

                # post_mids = await bot.send_media_group(
                #     chat_id=CFG.Review_Group,
                #     media=media
                # )

                # # 只取第一个消息对象
                # post_mid = post_mids[0]

            post.status = Post_Status.Accepted
            await post.save()

            await PublicPosts.create(
                message_id=post_mid.message_id,
                post=post,
                reviewer=user,
            )

            user.accept_count += 1
            user.review_count += 1
            await user.save()
