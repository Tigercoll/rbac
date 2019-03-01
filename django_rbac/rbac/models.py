from django.db import models

# Create your models here.

class  User(models.Model):
    """用户表"""
    username = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=37,verbose_name='密码')
    roles = models.ManyToManyField(to='Roles')
    class Meta:
        verbose_name='用户表'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.username

class Roles(models.Model):
    """角色表"""
    title = models.CharField(max_length=37,verbose_name='角色名称')
    permission = models.ManyToManyField(to='Permission')
    class Meta:
        verbose_name='角色表'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title
class Permission(models.Model):
    """权限表"""
    title = models.CharField(max_length=37,verbose_name='权限名')
    url = models.CharField(max_length=37,verbose_name='链接')

    class Meta:
        verbose_name='权限表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title