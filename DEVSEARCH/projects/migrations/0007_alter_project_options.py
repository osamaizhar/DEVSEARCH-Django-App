# Generated by Django 5.0 on 2024-02-17 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_review_owner_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total']},
        ),
    ]
