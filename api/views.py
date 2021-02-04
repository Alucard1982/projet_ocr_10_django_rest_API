from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from api.models import Project, Issue, Comments

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from api.permissions import IsAuthor, IsContributor, IsComments, IsIssue

from .serializers import UserSerializer, ProjectSerializer, IssueSerializer, CommentsSerializer


class UserProfileListCreateView(generics.ListAPIView):
    try:
        queryset = User.objects.all()
    except User.DoesNotExist:
        raise Http404
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserProfileDetailView(generics.RetrieveDestroyAPIView):
    try:
        queryset = User.objects.all()
    except User.DoesNotExist:
        raise Http404
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsContributor]


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        try:
            return Project.objects.filter(contributor=user)
        except Project.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthor, IsAuthenticated]
    queryset = Project.objects.all()


class ContributorListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        try:
            return User.objects.filter(project__id=id_project)
        except User.DoesNotExist:
            raise Http404


class AddContributor(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, *args, **kwargs, ):
        id_project = self.kwargs.get('id_project')
        try:
            project = Project.objects.get(pk=id_project)
        except Project.DoesNotExist:
            raise Http404
        return Response(project.contributor.add(self.request.user))


class ContributorDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        try:
            return User.objects.filter(project__id=id_project).filter(project__contributor=self.request.user)
        except User.DoesNotExist:
            raise Http404


class IssueListCreateView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsIssue]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        id_project = self.kwargs.get('id_project')
        try:
            return Issue.objects.filter(project__contributor=user).filter(project__id=id_project)
        except Issue.DoesNotExist:
            raise Http404

    def perform_create(self, serializer, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        try:
            projects = Project.objects.get(pk=id_project)
        except Project.DoesNotExist:
            raise Http404
        serializer.save(author=self.request.user, project=projects, user_assigner=self.request.user)


class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthor, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        try:
            return Issue.objects.filter(project__id=id_project)
        except Issue.DoesNotExist:
            raise Http404


class CommentsListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsComments]

    def get_queryset(self, *args, **kwargs):
        id_project = self.kwargs.get('id_project')
        id_issue = self.kwargs.get('pk')
        user = self.request.user
        try:
            return Comments.objects.filter(issue__project__contributor=user).filter(
                issue__project__id=id_project).filter(issue__pk=id_issue)
        except Comments.DoesNotExist:
            raise Http404

    def perform_create(self, serializer, *args, **kwargs):
        id_issue = self.kwargs.get('pk')
        try:
            issues = Issue.objects.get(pk=id_issue)
        except Issue.DoesNotExist:
            raise Http404
        serializer.save(author=self.request.user, issue=issues)


class CommentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    try:
        queryset = Comments.objects.all()
    except Comments.DoesNotExist:
        raise Http404

    """def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj"""

