# Generated by Django 5.1.1 on 2024-10-05 01:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_users_permission_lvl'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='users',
            new_name='User',
        ),
    ]
