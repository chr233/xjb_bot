'''
# @Author       : Chr_
# @Date         : 2021-10-27 16:52:43
# @LastEditors  : Chr_
# @LastEditTime : 2022-02-21 16:28:22
# @Description  : 用户投稿
'''

from tortoise.models import Model
from tortoise import fields
from enum import IntEnum

from custom import custom_fields


class Post_Types(IntEnum):
    '''
    稿件类型
    '''
    Default = 0     # 默认类型
    Text = 1        # 文字
    Media = 2       # 单图
    MediaGroup = 3  # 多图


class Post_Status(IntEnum):
    '''
    稿件状态
    '''
    Default = 0    # 默认状态
    Padding = 1    # 未投稿,等待确认
    Cancel = 2     # 已取消
    Reviewing = 3  # 已投稿,待审核
    Rejected = 4   # 投稿未过审
    Accepted = 5   # 已过审并发布
    Wating = 6     # 已过审但是等待发布(色图排期)
    Retract = 7     # 已撤回

    @staticmethod
    def describe(value) -> str:
        if value == 0:
            return '未知'
        elif value == 1:
            return '等待确认'
        elif value == 2:
            return '已取消'
        elif value == 3:
            return '等待审核'
        elif value == 4:
            return '未通过'
        elif value == 5:
            return '已采用'
        elif value == 6:
            return '已采用,色图排期'
        elif value == 6:
            return '已撤回'
        else:
            return '未知'


class Posts(Model):
    '''投稿稿件模型'''

    id = fields.IntField(pk=True)

    origin_cid = fields.IntField()  # 投稿的原会话ID
    origin_mid = fields.IntField(unique=True, index=True)  # 投稿的原消息ID
    action_mid = fields.IntField(unique=True, index=True)  # 投稿动作消息ID
    review_mid = fields.IntField(unique=True, index=True)  # 审核群消息ID
    manage_mid = fields.IntField(unique=True, index=True)  # 审核动作消息ID

    anymouse = fields.BooleanField(default=False)  # 是否匿名

    forward = fields.BooleanField(default=False)  # 是否为转发

    poster: fields.ForeignKeyRelation["Users"] = fields.ForeignKeyField(
        model_name='models.Users', related_name='posts',
        on_delete=fields.CASCADE
    )  # 投稿人

    status = fields.IntEnumField(
        enum_type=Post_Status, default=Post_Status.Default
    )  # 稿件状态

    post_type = fields.IntEnumField(
        enum_type=Post_Types, default=Post_Types.Default
    )  # 稿件类型

    caption = fields.TextField(max_length=2048, default='')  # 文字说明
    raw_caption = fields.TextField(max_length=2048, default='')  # 投稿原文

    tags = fields.IntField(default=0)  # 未发布前储存投稿人链接
    # 标签列表, 纯文本储存, 逗号分隔

    files = custom_fields.FileObjField(default='')  # 文件列表

    source_name = fields.CharField(max_length=255,default='')  # 消息来源名称
    source_id = fields.CharField(max_length=255,default='')  # 消息来源链接

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    public_post: fields.ReverseRelation["PublicPosts"]
    reject_post: fields.ReverseRelation["RejectPosts"]
    wanan_list: fields.ReverseRelation["Wanan_Posts"]

    class Mate:
        table = "posts"

    def __str__(self) -> str:
        return f'@{self.id} {self.status} {self.caption}'


class PublicPosts(Model):
    '''通过审核并发布的稿件模型'''

    id = fields.IntField(pk=True)

    message_id = fields.IntField(unique=True, index=True)  # 频道广播消息ID

    post: fields.OneToOneRelation["Posts"] = fields.OneToOneField(
        model_name='models.Posts', related_name='public_post', to_field='id',
        on_delete=fields.CASCADE
    )  # 被审核的原消息ID

    reviewer: fields.ForeignKeyRelation["Users"] = fields.ForeignKeyField(
        model_name='models.Users', related_name='reviews',
        on_delete=fields.CASCADE
    )  # 审核人

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    ratings: fields.ReverseRelation["Ratings"]

    class Mate:
        table = "public_posts"

    def __str__(self) -> str:
        return f'@{self.id} [{self.like} / {self.dislike} , {self.gress} , {self.mars}]'


class RejectPosts(Model):
    '''被拒绝的稿件模型'''

    id = fields.IntField(pk=True)

    post: fields.OneToOneRelation["Posts"] = fields.OneToOneField(
        model_name='models.Posts', related_name='reject_post', to_field='id',
        on_delete=fields.CASCADE
    )  # 被审核的原消息ID

    reviewer: fields.ForeignKeyRelation["Users"] = fields.ForeignKeyField(
        model_name='models.Users', related_name='reviews_reject',
        on_delete=fields.CASCADE
    )  # 审核人

    reason = fields.CharField(max_length=255, default='')  # 拒绝理由

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Mate:
        table = "reject_posts"

    def __str__(self) -> str:
        return f'@{self.id} {self.reason}'


class Wanan_Posts(Model):
    '''晚安稿件发送队列,发送后记得在该表中删除'''

    id = fields.IntField(pk=True)

    post: fields.OneToOneRelation["Posts"] = fields.OneToOneField(
        model_name='models.Posts', related_name='wanan_list', to_field='id',
        on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Mate:
        table = "wanan_list"

    def __str__(self) -> str:
        return f'@{self.id} {self.reason}'
