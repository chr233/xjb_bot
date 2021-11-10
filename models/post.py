'''
# @Author       : Chr_
# @Date         : 2021-10-27 16:52:43
# @LastEditors  : Chr_
# @LastEditTime : 2021-11-10 14:14:54
# @Description  : 用户投稿
'''

from tortoise.models import Model
from tortoise import fields
from enum import IntEnum


from custom import custom_fields


class Post_Status(IntEnum):
    '''
    稿件状态
    '''
    Default = 0    # 默认状态
    Padding = 1    # 未投稿,等待确认
    Reviewing = 2  # 已投稿,待审核
    Rejected = 3   # 投稿未过审
    Accepted = 4   # 已过审并发布
    Wating = 5     # 已过审但是等待发布(色图排期)

    def __str__(self) -> str:
        return self.name


class Posts(Model):
    '''投稿稿件模型'''

    id = fields.IntField(pk=True)

    origin_mid = fields.IntField(unique=True, index=True)  # 投稿的原消息ID
    action_mid = fields.IntField(unique=True, index=True)  # 投稿动作消息ID
    review_mid = fields.IntField(unique=True, index=True)  # 审核群消息ID
    manage_mid = fields.IntField(unique=True, index=True)  # 审核动作消息ID

    anymouse = fields.BooleanField(default=False)  # 是否匿名

    poster: fields.ForeignKeyRelation["Users"] = fields.ForeignKeyField(
        model_name='models.Users', related_name='posts',
        on_delete=fields.CASCADE
    )  # 投稿人

    status = fields.IntEnumField(
        enum_type=Post_Status, default=Post_Status.Default
    )  # 稿件状态

    caption = fields.CharField(max_length=255, default='')  # 文字说明

    tags = fields.CharField(max_length=255, default='')  # 标签列表

    source = custom_fields.LinkObjField(default='')  # 消息来源,为空代表消息来自投稿者
    files = custom_fields.FileObjField(default='')  # 文件列表

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

    # 评价
    like = fields.IntField(default=0)  # 好评数
    gress = fields.IntField(default=0)  # 生草数
    mars = fields.IntField(default=0)  # 火星数
    dislike = fields.IntField(default=0)  # 差评数

    rating_count = fields.IntField(default=0)  # 评价总数
    rating_score = fields.FloatField(default=0)  # 总评分

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
