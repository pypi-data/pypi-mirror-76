# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from xyz_util import modelutils

class Comment(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "评论"
        ordering = ('-create_time', )

    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="comments")
    content_type = models.ForeignKey(ContentType, verbose_name=ContentType._meta.verbose_name, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_name = models.CharField("名称", max_length=256, db_index=True, null=True, blank=True)
    content = models.TextField("内容")
    context = models.TextField("上下文", blank=True, default='')
    anchor = models.CharField("锚点", max_length=256, blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)
    is_active = models.BooleanField("有效", default=True)
    reply_count = models.PositiveIntegerField('回贴数', blank=True, default=0, editable=False)

    def save(self, **kwargs):
        if not self.object_name:
            self.object_name = unicode(self.content_object)
        return super(Comment, self).save(**kwargs)

    def __unicode__(self):
        return "%s 评论 %s" % (self.user.get_full_name(), self.content_object)



class Favorite(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "收藏"
        ordering = ('-create_time',)

    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="comment_favorites")
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField(null=True, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_name = models.CharField("名称", max_length=256, db_index=True, null=True, blank=True)
    notes = modelutils.JSONField("笔记", blank=True, default={})
    notes_count = models.PositiveSmallIntegerField('笔记数', blank=True, default=1)
    create_time = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)
    is_active = models.BooleanField("有效", default=True)

    def save(self, **kwargs):
        if not self.object_name:
            self.object_name = unicode(self.content_object)
        if not self.notes:
            self.notes = {}
        self.notes_count = len([n for n in self.notes.values() if n['is_active']])
        self.is_active = self.notes_count > 0
        return super(Favorite, self).save(**kwargs)

    def __unicode__(self):
        return "%s 收藏 %s" % (self.user.get_full_name(), self.object_name)
