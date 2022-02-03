# Generated by Django 4.0.1 on 2022-02-03 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=45)),
                ('openDt', models.IntegerField()),
                ('clip', models.CharField(default='', max_length=100)),
                ('star', models.FloatField()),
                ('genre', models.IntegerField()),
            ],
            options={
                'db_table': 'movies',
            },
        ),
    ]