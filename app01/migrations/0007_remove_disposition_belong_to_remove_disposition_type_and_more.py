# Generated by Django 4.1 on 2023-03-29 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_exam_candidate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disposition',
            name='belong_to',
        ),
        migrations.RemoveField(
            model_name='disposition',
            name='type',
        ),
        migrations.AddField(
            model_name='disposition',
            name='disposition_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='disposition',
            name='disposition_id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='disposition',
            name='introduction',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='permission',
            field=models.BigIntegerField(default=2),
        ),
    ]
