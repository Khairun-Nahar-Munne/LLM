# migrations/0002_add_description_to_hotel.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('properties', '0001_initial'),  # Assuming 'properties' is your app name
    ]

    operations = [
        migrations.RunSQL(
            sql='''
            ALTER TABLE hotels 
            ADD COLUMN IF NOT EXISTS description TEXT;
            ''',
            reverse_sql='''
            ALTER TABLE hotels 
            DROP COLUMN IF EXISTS description;
            '''
        ),
    ]