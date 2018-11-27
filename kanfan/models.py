from django.db import models
from django.contrib.auth.models import User
from kanfan.util.validators import YearValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Account(models.Model):
    auth_user_id=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.auth_user_id.username

class Bangumi(models.Model):
    title=models.CharField(
        _('番剧名'),
        max_length=200,
        unique=True,
        help_text=_('番剧名称'),
        error_messages={
            'unique': _("该番剧已经存在"),
        },
    )
    rss=models.URLField(
        _('rss订阅链接'),
        unique=True,
        help_text=_('rss链接'),
        error_messages={
            'unique': _("该rss链接已经存在"),
        },
    )
    STATES_CHOICE = (
        (1, '播出中'),
        (2, '已完结'),
    )
    state=models.IntegerField(choices=STATES_CHOICE)
    SEASONS_CHOICE = (
        (1, '春'),
        (2, '夏'),
        (3, '秋'),
        (4, '冬'),
    )
    season = models.IntegerField(choices=SEASONS_CHOICE)
    yearValidator = YearValidator()
    year = models.IntegerField(validators=[yearValidator])
    creator = models.ForeignKey(Account,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Episode(models.Model):
    title = models.CharField(
        _('单集名'),
        max_length=200,
        unique=True,
        help_text=_('单集名称'),
        error_messages={
            'unique': _("该集已经存在"),
        },
    )
    file = models.FilePathField(max_length=500)
    torrent = models.FilePathField(max_length=500)
    magnet = models.TextField()
    STATES_CHOICE = (
        (1, '正在准备视频文件'),
        (2, '视频文件准备完毕'),
        (3,'视频文件不存在'),
    )
    state = models.IntegerField(choices=STATES_CHOICE)
    bangumi_id = models.ForeignKey(Bangumi,null=True,on_delete=models.SET_NULL)
    subtitle_file = models.FilePathField(max_length=500)
    subtitle_torrent = models.FilePathField(max_length=500)
    subtitle_magnet = models.TextField()

    def __str__(self):
        return self.title

class Follow(models.Model):
    account_id = models.ForeignKey(Account,null=True,on_delete=models.SET_NULL)
    bangumi_id = models.ForeignKey(Bangumi,null=True,on_delete=models.SET_NULL)
    STATES_CHOICE = (
        (1, '追番中'),
        (2, '已补完'),
    )
    state = models.IntegerField(choices=STATES_CHOICE)
    last_episode_id = models.ForeignKey(Episode,null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.account_id.auth_user_id.username+' '+self.get_state_display()+' '+self.bangumi_id.title