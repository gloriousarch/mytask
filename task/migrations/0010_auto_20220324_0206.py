# Generated by Django 2.2.26 on 2022-03-24 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_auto_20220323_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='picture',
            field=models.ImageField(blank=True, upload_to='task_image'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_reward',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_title',
            field=models.CharField(max_length=30),
        ),
    ]