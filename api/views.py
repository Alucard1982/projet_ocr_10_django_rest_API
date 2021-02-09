from django.http import Http404

from django.contrib.auth.models import User
from api.models import Project, Issue, Comments, Contributeur

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from api.permissions import IsAuthor, IsContributor, IsComments, IsIssue

from .serializers import UserSerializer, ProjectSerializer, IssueSerializer, CommentsSerializer, ContributeurSerializer


class UserProfileListCreateView(generics.ListAPIView):
    """permet de recuperer les users"""

    try:
        queryset = User.objects.all()
    except User.DoesNotExist:
        raise Http404
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserProfileDetailView(generics.RetrieveAPIView):
    """ permet de récuperer un user en fonction de l'id """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    try:
        queryset = User.objects.all()
    except User.DoesNotExist:
        raise Http404


class ProjectListCreateView(generics.ListCreateAPIView):
    """récupere tout les projets dans lequel on est contributeur, permet de créer un projet"""

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        """override le queryset"""
        try:
            return Project.objects.filter(contributor=self.request.user)
        except Project.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        """override le save de l'objet en bdd"""
        serializer.save(author=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """get,update,delete un projets en fonction de l'id.Il n'y a que l'auteur du projet qui peut y accéder"""

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthor, IsAuthenticated]
    try:
        queryset = Project.objects.all()
    except Project.DoesNotExist:
        raise Http404


class ProjectRetrieveDetailView(generics.RetrieveAPIView):
    """get un projets en fonction de l'id.Tout les contributeurs du projet peuvent y accéder"""

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        """override le queryset"""

        try:
            return Project.objects.filter(contributor=self.request.user)
        except Project.DoesNotExist:
            raise Http404


class ContributorListView(generics.ListAPIView):
    """get les  contributeurs d'un  projets """

    serializer_class = ContributeurSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        """override le queryset"""

        id_project = self.kwargs.get('id_project')
        try:
            return Contributeur.objects.filter(project__id=id_project)
        except Contributeur.DoesNotExist:
            raise Http404


class ContributorCreateDetailView(generics.CreateAPIView):
    """ permet de d'ajouter un  contributeur à un project qui existe"""

    permission_classes = [IsAuthenticated]
    serializer_class = ContributeurSerializer

    def perform_create(self, serializer, *args, **kwargs):
        """override le save de l'objet en bdd"""

        id_project = self.kwargs.get('id_project')
        try:
            projects = Project.objects.get(pk=id_project)
        except Project.DoesNotExist:
            raise Http404
        serializer.save(project=projects, user=self.request.user)


class ContributorDetailView(generics.RetrieveDestroyAPIView):
    """ Permet de se supprimer d'un projet.Aucun autre utilisateur ne peut le faire"""

    serializer_class = ContributeurSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self, *args, **kwargs):
        """override le queryset"""

        id_project = self.kwargs.get('id_project')
        try:
            return Contributeur.objects.filter(project__id=id_project)
        except Contributeur.DoesNotExist:
            raise Http404


class IssueListCreateView(generics.ListCreateAPIView):
    """get, create les issues du projet. Il y a que les contributeurs du projet qui y on accés """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsIssue]

    def get_queryset(self, *args, **kwargs):
        """override le queryset"""

        user = self.request.user
        id_project = self.kwargs.get('id_project')
        try:
            return Issue.objects.filter(project__contributor=user).filter(project__id=id_project)
        except Issue.DoesNotExist:
            raise Http404

    def perform_create(self, serializer, *args, **kwargs):
        """override le save de l'objet en bdd"""

        id_project = self.kwargs.get('id_project')
        try:
            projects = Project.objects.get(pk=id_project)
        except Project.DoesNotExist:
            raise Http404
        serializer.save(author=self.request.user, project=projects, user_assigner=self.request.user)


class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    """get, update, delete l'issue.Il y a que l'auteur de l'issue qui  y a accés"""

    serializer_class = IssueSerializer
    permission_classes = [IsAuthor, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        """override le queryset"""

        user = self.request.user
        id_project = self.kwargs.get('id_project')
        try:
            return Issue.objects.filter(project__contributor=user).filter(project__id=id_project)
        except Issue.DoesNotExist:
            raise Http404


class IssueRetrieveDetailView(generics.RetrieveAPIView):
    """get, les issues du projets.Tou les contributeurs du projet y on accés"""

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        """override le queryset"""

        user = self.request.user
        id_project = self.kwargs.get('id_project')
        try:
            return Issue.objects.filter(project__contributor=user).filter(project__id=id_project)
        except Issue.DoesNotExist:
            raise Http404


class CommentsListCreateView(generics.ListCreateAPIView):
    """get, create un commentaire.Seul les contributeurs du projets y on accés"""

    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsComments]

    def get_queryset(self, *args, **kwargs):
        """override le queryset"""

        id_project = self.kwargs.get('id_project')
        id_issue = self.kwargs.get('pk')
        user = self.request.user
        try:
            return Comments.objects.filter(issue__project__contributor=user).filter(
                issue__project__id=id_project).filter(issue__pk=id_issue)
        except Comments.DoesNotExist:
            raise Http404

    def perform_create(self, serializer, *args, **kwargs):
        """override le save de l'objet en bdd"""

        id_issue = self.kwargs.get('pk')
        try:
            issues = Issue.objects.get(pk=id_issue)
        except Issue.DoesNotExist:
            raise Http404
        serializer.save(author=self.request.user, issue=issues)


class CommentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """get, delete, update le commentaire en fonction de l'id.Il ny a que l'auteur qui y a accés"""

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


class CommentsGetDetailView(generics.RetrieveAPIView):
    """get le commentaire en fonction de l'id.Tout les contributeurs du projet y on accés"""

    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        """override le queryset"""

        try:
            return Comments.objects.filter(issue__project__contributor=self.request.user)
        except Comments.DoesNotExist:
            raise Http404
