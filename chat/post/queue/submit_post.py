'''
# @Author       : Chr_
# @Date         : 2022-02-12 19:25:26
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-12 19:30:11
# @Description  : 
'''


from aiogram.types.callback_query import CallbackQuery
from aiogram.types.input_media import InputMedia, MediaGroup
from aiogram.types.message import  ParseMode
from buttons.review import RKH


from models.post import Posts, Post_Status

from buttons.submit import SubmitPostKey, gen_submit_keyboard

from config import CFG


async def handle_submit_post_callback(query: CallbackQuery):
    '''
    处理投稿按钮回调
    '''
    data = query.data
    bot = query.bot

    chat_id = query.message.chat.id
    msg_id = query.message.message_id

    user = query.user

    post = await Posts.get_or_none(action_mid=msg_id)

    if not post:
        await query.answer('投稿不存在')
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text='投稿不存在',
        )
        return

    if post.status != Post_Status.Padding:
        await query.answer('请不要重复操作')
        status = Post_Status.describe(Post_Status.Reviewing)
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=msg_id,
        )

    if 'anymouse_' in data:
        anymouse = data == SubmitPostKey.anymouse_on

        kbd = gen_submit_keyboard(anymouse)

        await query.answer('已开启匿名模式' if anymouse else '已关闭匿名模式',)
        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg_id, reply_markup=kbd)
    else:

        if data == SubmitPostKey.cancel:
            await query.answer('投稿已取消')
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text='投稿已取消',
            )
            post.update_from_dict({
                'caption': '',
                'status': Post_Status.Cancel,
                'source': '',
                'files': '',
                'tags': ''
            })

        elif '_post' in data:
            if post.status == Post_Status.Padding:
                anymouse = data == SubmitPostKey.post_anymouse

                files = post.files

                if len(files) <= 1:
                    review_mid = await bot.forward_message(
                        chat_id=CFG.Review_Group,
                        from_chat_id=chat_id,
                        message_id=post.origin_mid
                    )

                else:
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

                if 'NSFW' in post.raw_caption.upper():
                    selected = 1
                else:
                    selected = 0

                keyboard = await RKH.get_tag_keyboard_short(selected)

                status = Post_Status.describe(Post_Status.Reviewing)

                manage_mid = await bot.send_message(
                    chat_id=CFG.Review_Group,
                    text=(
                        f'投稿人: {post.tags}\n'
                        f'匿名: `{"是" if anymouse else "否"}`\n'
                        '\n'
                        f'状态: `{status}`\n'
                        '更多帮助: /help'
                    ),
                    parse_mode=ParseMode.MARKDOWN_V2,
                    reply_markup=keyboard
                )

                post.update_from_dict({
                    'anymouse_mode': anymouse,
                    'status': Post_Status.Reviewing,
                    'anymouse': anymouse,
                    'review_mid': review_mid,
                    'manage_mid': manage_mid
                })

                await query.answer('稿件投递成功')

                user.prefer_anymouse = anymouse
                user.post_count += 1

                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=msg_id,
                    text=(
                        f'稿件状态: `{status}`\n'
                        f'匿名: `{"是" if post.anymouse else "否"}`\n'
                        f'采用数/总投稿: `{user.accept_count}` / `{user.post_count}`\n'
                    ),
                    parse_mode=ParseMode.MARKDOWN_V2
                )

                await user.save()

            else:
                await query.answer('请不要重复提交')
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=msg_id,
                    text=(
                        f'稿件状态: `{str(Post_Status.Reviewing)}`\n'
                        f'采用数/总投稿: `{user.accept_count}` / `{user.post_count}`\n'
                    ),
                    parse_mode=ParseMode.MARKDOWN_V2
                )
        else:
            await query.answer('未知操作')
            await bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=msg_id,
            )
            return

        await post.save()