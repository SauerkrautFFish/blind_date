from django.db import models

# Create your models here.


class User(models.Model):
    id = models.BigIntegerField("主键", db_column="id", primary_key=True),
    account = models.CharField("", max_length=255, unique=True),
    username = models.CharField(max_length=255),
    password = models.CharField(max_length=255),
    create_time = models.DateTimeField(auto_now_add=True),

    class Meta:
        db_table = "user"


class Candidate(models.Model):
    id = models.BigIntegerField("主键", db_column="id", primary_key=True),
    user_id = models.BigIntegerField(db_index=True),
    name = models.CharField(max_length=255),
    image_url = models.CharField(max_length=255),
    create_time = models.DateTimeField(auto_now_add=True),

    class Meta:
        db_table = "candidate"


class BlindDateRecord(models.Model):
    id = models.BigIntegerField("主键", db_column="id", primary_key=True),
    candidate_id = models.BigIntegerField(db_index=True),
    user_record = models.TextField(default="[]"),
    candidate_record = models.TextField(default="[]"),
    create_time = models.DateTimeField(auto_now_add=True),
    update_time = models.DateTimeField(auto_now=True),

    class Meta:
        db_table = "blind_date_record"
