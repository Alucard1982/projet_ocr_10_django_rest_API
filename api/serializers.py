from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Project, Issue, Comments, Contributeur


class UserSerializer(serializers.ModelSerializer):
    """permet de serializer ou de déserializer le user en fonction du verbe de la requete"""

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


"""class ContributeurSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Contributeur
        fields = ('user', 'role')"""


class CommentsSerializer(serializers.ModelSerializer):
    """permet de serializer ou de déserializer le commentaire en fonction du verbe de la requete"""

    author = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'description', 'author', 'created_time')


class IssueSerializer(serializers.ModelSerializer):
    """permet de serializer ou de déserializer l'issue' en fonction du verbe de la requete"""

    comments = CommentsSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    user_assigner = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ('id', 'description', 'priority', 'status', 'author', 'user_assigner', 'comments')


class ProjectSerializer(serializers.ModelSerializer):
    """permet de serializer ou de déserializer le projet en fonction du verbe de la requete"""

    issues = IssueSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)
    contributor = UserSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        user = validated_data['author']
        project.contributor.add(user)
        return project

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'type', 'author', 'contributor', 'issues', 'comments')
