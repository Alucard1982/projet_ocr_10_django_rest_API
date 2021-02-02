from rest_framework import generics

from django.contrib.auth.models import User
from api.models import Project, Issue, Comments

from rest_framework.permissions import IsAuthenticated
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


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthor, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Project.objects.filter(contributor=user)


class ContributorListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return User.objects.filter(project__id=id_project)


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


class CommentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthor, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return Comments.objects.filter(issue__project__id=id_project)
