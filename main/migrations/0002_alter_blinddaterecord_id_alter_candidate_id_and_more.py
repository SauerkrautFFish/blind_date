# Generated by Django 4.2.5 on 2023-11-19 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blinddaterecord',
            name='id',
            field=models.BigAutoField(db_column='id', primary_key=True, serialize=False, verbose_name='主键'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='id',
            field=models.BigAutoField(db_column='id', primary_key=True, serialize=False, verbose_name='主键'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(db_column='id', primary_key=True, serialize=False, verbose_name='主键'),
        ),
    ]
