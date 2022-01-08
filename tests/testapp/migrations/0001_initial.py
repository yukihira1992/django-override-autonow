from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutoFieldsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_auto_now', models.DateField(auto_now=True, null=True)),
                ('date_auto_now_add', models.DateField(auto_now_add=True, null=True)),
                ('datetime_auto_now', models.DateTimeField(auto_now=True, null=True)),
                ('datetime_auto_now_add', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AutoFieldsModel2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_auto_now', models.DateField(auto_now=True, null=True)),
                ('date_auto_now_add', models.DateField(auto_now_add=True, null=True)),
                ('datetime_auto_now', models.DateTimeField(auto_now=True, null=True)),
                ('datetime_auto_now_add', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
