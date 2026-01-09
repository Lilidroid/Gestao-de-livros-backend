import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from livros.models import Livro, UserLivro

# -------- utilizador de teste --------
user, created = User.objects.get_or_create(username='Joao')
if created:
    user.set_password('123456')
    user.save()
    print(f'Criado utilizador: {user.username}')

# -------- livros iniciais --------
livros_data = [
    {'title': 'O Principezinho', 'author': 'Antoine de Saint-Exupéry', 'isbn': '1234567890', 'year': 1943, 'quantity': 3},
    {'title': 'Dom Quixote', 'author': 'Miguel de Cervantes', 'isbn': '0987654321', 'year': 1605, 'quantity': 2},
    {'title': 'Harry Potter e a Pedra Filosofal', 'author': 'J.K. Rowling', 'isbn': '1111111111', 'year': 1997, 'quantity': 5},
]

for l in livros_data:
    # Adiciona o ut aos livros
    livro, created = Livro.objects.get_or_create(
        isbn=l['isbn'], defaults={**l, 'user': user}
    )
    if created:
        print(f'Criado livro: {livro.title}')

# -------- estados de leitura --------
status_data = [
    ('O Principezinho', 'read'),
    ('Dom Quixote', 'reading'),
    ('Harry Potter e a Pedra Filosofal', 'to_read'),
]

for title, status in status_data:
    livro = Livro.objects.get(title=title, user=user)
    user_livro, created = UserLivro.objects.get_or_create(
        user=user, livro=livro, defaults={'status': status}
    )
    if created:
        print(f'Criado UserLivro: {user.username} - {livro.title} ({status})')


