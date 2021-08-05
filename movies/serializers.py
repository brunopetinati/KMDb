from rest_framework import serializers
from .models import Movie, Comment, Criticism, Genre
from accounts.models import User



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        # extra_kwargs = {'id': {'read_only': True}}

class UserSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment']

    user = UserSetSerializer(read_only=True)

class CriticismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criticism
        fields = ['id', 'critic', 'stars', 'review', 'spoilers']

    stars = serializers.IntegerField(min_value=1, max_value=10)
    critic = UserSetSerializer(read_only=True)

class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        # se relaciona com criticism_set e comment_set que não foram definidos, então esse é o padrão
        fields = ['id', 'title', 'duration', 'genres', 'launch', 'classification', 'synopsis', 'criticism_set', 'comment_set']

        

    # trabalha-se os relacionamentos nesse override do método create
    # repare que o campo genres não foi incluído
    def create(self, validated_data):
        movie  = Movie.objects.get_or_create(
            title = validated_data['title'],
            duration = validated_data['duration'],
            launch = validated_data['launch'],
            classification = validated_data['classification'],
            synopsis = validated_data['synopsis']
        )[0]

        genres = validated_data['genres']

        for genre in genres:
            created_genre = Genre.objects.get_or_create(**genre)[0]
            movie.genres.add(created_genre)

        return movie

    # recebe uma lista de dicionários
    genres = GenreSerializer(many=True)
    criticism_set = CriticismSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    

