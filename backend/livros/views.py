from django.contrib.auth.models import User
from rest_framework import viewsets, serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Livro, Categoria

# ---------- Serializers ----------

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']


class LivroSerializer(serializers.ModelSerializer):
    # recebe TEXTO da categoria
    categoria = serializers.CharField(required=False, allow_blank=True)
    # devolve o NOME da categoria
    categoria_nome = serializers.SerializerMethodField()

    class Meta:
        model = Livro
        fields = [
            'id', 'title', 'author', 'isbn',
            'year', 'quantity', 'status',
            'categoria',        # input (texto)
            'categoria_nome'    # output (nome)
        ]

    def get_categoria_nome(self, obj):
        return obj.categoria.nome if obj.categoria else ''

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        categoria_nome = validated_data.pop('categoria', '').strip()
        categoria_obj = None

        if categoria_nome:
            categoria_obj, _ = Categoria.objects.get_or_create(
                nome=categoria_nome,
                user=user
            )

        livro = Livro.objects.create(
            user=user,
            categoria=categoria_obj,
            **validated_data
        )
        return livro

    def update(self, instance, validated_data):
        categoria_nome = validated_data.pop('categoria', '').strip()

        if categoria_nome:
            categoria_obj, _ = Categoria.objects.get_or_create(
                nome=categoria_nome,
                user=instance.user
            )
            instance.categoria = categoria_obj

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# ---------- ViewSets ----------

class LivroViewSet(viewsets.ModelViewSet):
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Livro.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        # IMPORTANTE: permite aceder ao request no serializer
        return {'request': self.request}


class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Categoria.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------- Registrar utilizador ----------

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username', '')
    password = request.data.get('password', '')

    if not username or not password:
        return Response(
            {'error': 'Utilizador e palavra-passe obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Utilizador já existe'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password)
    return Response(
        {'success': True, 'username': user.username},
        status=status.HTTP_201_CREATED
    )


