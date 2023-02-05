from django.urls import path
from . import views

app_name = "password"

urlpatterns = [
    path('', views.index, name="index"),
    path('del/<int:id>', views.delete, name='deletePass'),
    path('reg/<int:id>', views.regen, name="regen"),
    path('addPass/', views.addPass, name='addPass'),
]
