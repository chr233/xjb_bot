'''
# @Author       : Chr_
# @Date         : 2021-10-27 16:52:43
# @LastEditors  : Chr_
# @LastEditTime : 2021-10-31 00:13:15
# @Description  :
'''

from tortoise.models import Model
from tortoise import fields


class Base_Posts(Model):
    '''基础稿件模型'''

    id = fields.IntField(pk=True)
    message_id =fields.IntField(unique=True,index=True)
    anymouse = fields.BooleanField(default=False)  # 是否匿名
    author = fields.ForeignKeyField(
        model_name='models.Users',  on_delete=fields.CASCADE)  # 投稿人
    operater = fields.CharField(max_length=255, default='')  # 审核人
    real_author = fields.CharField(max_length=255, default='')  # 转发消息的原作者
    describe = fields.CharField(max_length=255)  # 描述
    media_content = fields.TextField()  # 文件列表
    tags = fields.TextField()  # 标签列表
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Mate:
        abstract = True


class Review_Posts(Base_Posts):
    '''待审核稿件模型,允许投票'''

    agree = fields.IntField(default=0)  # 通过
    disagree = fields.IntField(default=0)  # 拒绝

    vote_count = fields.IntField(default=0)  # 投票总数
    vote_percent = fields.FloatField(default=0)  # 总评分

    class Mate:
        table = "posts_review"


class Rejected_Posts(Base_Posts):
    '''未过审稿件模型,记录原因'''

    reason = fields.CharField(max_length=255, default='')  # 拒稿原因

    class Mate:
        table = "posts_rejected"


class Accepted_Posts(Base_Posts):
    '''过审稿件模型,允许评分'''

    like = fields.IntField(default=0)  # 好评数
    gress = fields.IntField(default=0)  # 生草数
    dislike = fields.IntField(default=0)  # 差评数

    rating_count = fields.IntField(default=0)  # 评价总数
    rating_score = fields.FloatField(default=0)  # 总评分

    class Mate:
        table = "posts_accpeted"


class Accepted_NSFW_Posts(Base_Posts):
    '''过审NSFW稿件模型
    只会在特定时间自动发送'''

    class Mate:
        table = "posts_accepted_nsfw"
