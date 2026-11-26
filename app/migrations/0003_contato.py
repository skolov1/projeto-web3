from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_servico_imagem"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="Contato",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("nome", models.CharField(max_length=100)),
                        ("email", models.EmailField(max_length=254)),
                        ("telefone", models.CharField(blank=True, max_length=20)),
                        ("mensagem", models.TextField()),
                    ],
                    options={"db_table": "contato_contato"},
                ),
            ],
            database_operations=[],
        ),
    ]