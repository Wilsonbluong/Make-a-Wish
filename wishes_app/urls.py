from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wishes', views.wishes),
    path('wishes/new', views.new_wishes),
    path('add_wishes', views.add_wishes),
    path('edit/<int:wish_id>', views.edit),
    path('wishes/<int:wish_id>/update', views.update),
    path('wishes/<int:wish_id>/grant', views.grant),
    path('wishes/<int:wish_id>/delete', views.delete),
    path('wishes/<int:wish_id>/like', views.like),
    path('logout', views.logout),
]
