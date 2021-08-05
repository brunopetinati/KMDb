from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .serializers import (
    MovieSerializer,
    CriticismSerializer,
    CommentSerializer
)
from .models import Movie, Criticism, Comment
from .permissions import IsAdmin, IsCritic, IsUser

# para implementar método de busca, necessário definir lookup_fields em MovieView
class MultipleFieldLookUpMixin:
    def get_queryset(self):

        # queryset é o campo passado em MovieView
        queryset = self.queryset
        lookup_filter = {}

        for lookup_field in self.lookup_fields:
            #caso exista um campo no body json
            if self.request.data.get(lookup_field): 
                lookup_filter[f'{lookup_field}__icontains'] = self.request.data.get(lookup_field)

        # json_body : {"title":"liberdade"}
        # ipdb => lookup_field => {'title_icontains': 'liberdade'}
        # isso tudo é a mesma coisa de fazer Movie.objects.filter(title_icontains='liberdade'), só que de uma maneira "implícita"

        queryset = queryset.filter(**lookup_filter)

        return queryset     
        return super().get_queryset()


# ListCreateAPIView é classe genérica que já tem todos os comportamentos de GET e POST prontos
class MovieView(MultipleFieldLookUpMixin, generics.ListCreateAPIView):
    # verifica token
    authentication_classes = [TokenAuthentication]
    # permissão personalizada
    permission_classes = [IsAdmin]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_fields = ['title']

# essa classe já retorna o filme pelo ID, e também deleta, sendo necessário Token de Admin. Ver urls.py
class MovieRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # alterar pk para 'movie_id'
    lookup_url_kwarg = 'movie_id'

# tem rotas POST e PUT
class CriticReviewView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Movie.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCritic]
    serializer_class = CriticismSerializer
    lookup_url_kwarg = 'movie_id'

# os relacionamentos entre as tabelas não são feitos automaticamente pelas generics.Views.
# dessa forma, é feito um override do método create do serializer. Ou, sobrescreve-se o método create
# do CreateAPIView aqui mesmo =>

# cada crítico poderá fazer apenas uma avaliação
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # tenta encontrar o filme pela URL
            movie = Movie.objects.get(id=kwargs['movie_id'])
            # tenta encontrar uma crítica já criada para tal filme
            critic = Criticism.objects.filter(movie=movie, critic=request.user)

            if len(critic) == 0:
                critic = Criticism.objects.create(
                    stars = request.data['stars'],
                    review = request.data['review'],
                    spoilers = request.data['spoilers'],
                    critic = request.user,
                    movie = movie
                )

                serializer = CriticismSerializer(critic)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            else:
                return Response({'detail':'You have already created a critic for this movie.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except ObjectDoesNotExist:
            return Response({'detail':'Not found.'}, status=status.HTTP_404_NOT_FOUND)


# fazemos um override do método update do UpdateAPIView
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # self.perform_update(serializer)

        movie = Movie.objects.get(id=kwargs['movie_id'])

        try:
            critic = Criticism.objects.get(movie=movie, critic=request.user)

        except ObjectDoesNotExist:
            return Responde({'detail':'Not found'}, status=status.HTTP_404_NOT_FOUND)

        critic.stars = request.data['stars']
        critic.review = request.data['review']
        critic.spoilers = request.data['spoilers']
        critic.save()
        serializer = CriticismSerializer(critic)
    

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
class CommentReviewView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]
    lookup_url_kwarg = 'movie_id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)


        try:
            movie = Movie.objects.get(id=kwargs['movie_id'])
        except ObjectDoesNotExist:
            return Responde({'detail':'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        # para criar um comentário, é necessário o comentário, o filme e o usuário
        comment = Comment.objects.create(comment=request.data['comment'], user=request.user, movie=movie)
        serializer = CommentSerializer(comment)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)

        movie = Movie.objects.get(id=kwargs['movie_id'])

        try:
            comment = Comment.objects.get(id=request.data['comment_id'],movie=movie, user=request.user)
        except ObjectDoesNotExist:
            return Response({'detail':'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        comment.comment = request.data['comment']
        comment.save()
        serializer = CommentSerializer(comment)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
