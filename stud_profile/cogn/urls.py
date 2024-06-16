from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.faculty, name='faculty'),
    path('group/<int:group_id>/', views.stud, name='stud'),
    path('student/<int:student_id>', views.profile, name='profile'),
    path('contacts', views.contacts, name='contacts'),

    #path('cognitive_profile/', views.plot_cognitive_profile, name='cognitive_profile')

]
