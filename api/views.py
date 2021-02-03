from django.contrib.auth.models import User
from rest_framework.decorators import api_view

from api.models import Project, Issue, Comments

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from api.permissions import IsAuthor, IsContributor

from .serializers import UserSerializer, ProjectSerializer, IssueSerializer, CommentsSerializer


class UserProfileListCreateView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserProfileDetailView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsContributor]


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Project.objects.filter(contributor=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthor, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Project.objects.filter(contributor=user)


class ContributorListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return User.objects.filter(project__id=id_project)


class AddContributor(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, *args, **kwargs, ):
        id_project = self.kwargs.get('id_project')
        project = Project.objects.get(pk=id_project)
        return Response(project.contributor.add(self.request.user))


class ContributorDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return User.objects.filter(project__id=id_project)


class IssueListCreateView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        id_project = self.kwargs.get('id_project')
        return Issue.objects.filter(project__contributor=user).filter(project__id=id_project)

    def perform_create(self, serializer, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        projects = Project.objects.get(pk=id_project)
        serializer.save(author=self.request.user, project=projects)


class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthor, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return Issue.objects.filter(project__id=id_project)


class CommentsListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        user = self.request.user
        return Comments.objects.filter(issue__project__contributor=user).filter(issue__project__id=id_project)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthor, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return Comments.objects.filter(issue__project__id=id_project)