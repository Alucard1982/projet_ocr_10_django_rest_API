from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Project, Issue, Comments


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class CommentsSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'description', 'author', 'created_time')


class IssueSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    user_assigner = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ('id', 'description', 'priority', 'status', 'author', 'user_assigner', 'comments')


class ProjectSerializer(serializers.ModelSerializer):
    issues = IssueSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)
    contributor = UserSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'type', 'author', 'contributor', 'issues', 'comments')
