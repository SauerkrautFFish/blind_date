from datetime import datetime

from django.db import models

# Create your models here.


class User(models.Model):
    id = models.BigAutoField("主键", db_column="id", primary_key=True)
    account = models.CharField("账号", max_length=255, unique=True)
    username = models.CharField("用户名", max_length=255)
    password = models.CharField("密码", max_length=255)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "user"


class Candidate(models.Model):
    id = models.BigAutoField("主键", db_column="id", primary_key=True)
    user_id = models.BigIntegerField("用户id", default=0, db_index=True)
    name = models.CharField("相亲对象名字", max_length=255),
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "candidate"


class BlindDateRecord(models.Model):
    id = models.BigAutoField("主键", db_column="id", primary_key=True)
    candidate_id = models.BigIntegerField("相亲对象id", default=0, db_index=True)
    user_record = models.TextField("自己的记录", default="[]")
    candidate_record = models.TextField("对方的记录", default="[]")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "blind_date_record"
