from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome_cat = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_cat