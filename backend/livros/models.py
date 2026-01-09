from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class StatusLivro(models.Model):
    nome = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} ({self.user.username})"


class Livro(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    year = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=50, default='Por ler')


    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    StatusLivro = models.ForeignKey(
        StatusLivro,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title




