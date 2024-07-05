# Generated by Django 5.0.6 on 2024-07-05 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('cover', models.CharField(choices=[('HARD', 'Hard'), ('SOFT', 'Soft')], default='HARD', max_length=4)),
                ('inventory', models.PositiveIntegerField()),
                ('daily', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField()),
                ('expected_return', models.DateField()),
                ('actual_return', models.DateField(null=True)),
                ('book_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowing_id', models.IntegerField()),
                ('session_url', models.URLField(max_length=255)),
                ('session_id', models.CharField(max_length=255)),
            ],
        ),
    ]
