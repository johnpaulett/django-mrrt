from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ReportTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "template_uid",
                    models.TextField(
                        help_text="A unique alphanumeric identifier (OID) included in any report instance generated using the template"
                    ),
                ),
                (
                    "title",
                    models.TextField(
                        help_text="A human readable name for the template. There is enforced correspondence with the title element in the head."
                    ),
                ),
                ("content", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
            ],
            options={
                "swappable": "MRRT_REPORTTEMPLATE_MODEL",
            },
        ),
        migrations.AddConstraint(
            model_name="reporttemplate",
            constraint=models.UniqueConstraint(
                fields=("template_uid",), name="unique_template_uid"
            ),
        ),
    ]
