from rest_framework import generics
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, )
from rest_framework.permissions import IsAuthenticated
# from .permissions import IsOwnerProfileOrReadOnly

from django.contrib.auth.models import User
from api.models import Project, Issue, Comments

from .serializers import UserSerializer, ProjectSerializer, IssueSerializer, CommentsSerializer


class UserProfileListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]


class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ContributorListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return User.objects.filter(project__id=id_project)


class ContributorDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return User.objects.filter(project__id=id_project)


class IssueListCreateView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return Issue.objects.filter(project__id=id_project)


class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return Issue.objects.filter(project__id=id_project)


class CommentsListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return Comments.objects.filter(issue__project__id=id_project)


class CommentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsSerializer

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        return Comments.objects.filter(issue__project__id=id_project)
