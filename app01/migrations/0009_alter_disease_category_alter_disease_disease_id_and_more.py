# Generated by Django 4.1 on 2023-03-29 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_project_alter_department_department_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disease',
            name='category',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='disease',
            name='disease_id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='disease',
            name='introduction',
            field=models.TextField(),
        ),
    ]
