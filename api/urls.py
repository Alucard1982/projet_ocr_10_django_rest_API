from django.urls import path
from api import views

urlpatterns = [
    path('profile/', views.UserProfileListCreateView.as_view()),
    path('profile/<int:pk>', views.UserProfileDetailView.as_view()),

    path('project/', views.ProjectListCreateView.as_view()),
    path('project/<int:pk>', views.ProjectDetailView.as_view()),

    path('project/<int:id_project>/users/', views.ContributorListView.as_view()),
    path('project/<int:id_project>/users/<int:pk>', views.ContributorDetailView.as_view()),
    path('project/<int:id_project>/add_users/', views.AddContributor.as_view()),

    path('project/<int:id_project>/issue/', views.IssueListCreateView.as_view()),
    path('project/<int:id_project>/issue/<int:pk>', views.IssueDetailView.as_view()),

    path('project/<int:id_project>/issue/<int:pk>/comments/', views.CommentsListCreateView.as_view()),
    path('project/<int:id_project>/issue/<int:pk>/comments/<int:id>', views.CommentsDetailView.as_view()),
]
