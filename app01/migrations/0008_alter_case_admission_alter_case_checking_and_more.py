# Generated by Django 4.1 on 2023-04-27 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_remove_case_admission_pic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='admission',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='case',
            name='checking',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='case',
            name='diagnostic_result',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='case',
            name='treatment',
            field=models.TextField(default=''),
        ),
    ]
