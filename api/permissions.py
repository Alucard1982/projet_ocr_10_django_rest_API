from rest_framework import permissions
from django.contrib.auth.models import User
from api.models import Project, Issue, Comments
import logging

logger = logging.getLogger(__name__)


class IsAuthor(permissions.BasePermission):
    """Permet d'acceder à la donner qui se l'utilisateur courant est l'auteur  """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsContributor(permissions.BasePermission):
    """Permet d'acceder à la donner que si c'est l'utilisateur courant """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsIssue(permissions.BasePermission):
    """Permet de  voir si les contributeurs font bien partie du projet et peuvent donc accéder à l'issue"""

    def has_permission(self, request, view):
        id_project = view.kwargs.get('id_project')
        projects = Project.objects.filter(contributor=request.user).filter(pk=id_project)
        return projects


class IsComments(permissions.BasePermission):
    """Permet de voir si les contributeurs font bien partie du projet et peuvent donc accéder au commentaire"""

    def has_permission(self, request, view):
        # Instance must have an attribute named `owner`.
        id_issue = view.kwargs.get('pk')
        id_project = view.kwargs.get('id_project')
        issues = Issue.objects.filter(project__contributor=request.user).filter(
            project__id=id_project).filter(pk=id_issue)
        return issues

