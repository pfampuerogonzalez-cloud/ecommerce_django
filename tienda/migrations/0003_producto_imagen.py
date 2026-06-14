from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0002_rename_prodcuto_producto"),
    ]

    operations = [
        migrations.AddField(
            model_name="producto",
            name="imagen",
            field=models.ImageField(blank=True, null=True, upload_to="productos/"),
        ),
    ]
