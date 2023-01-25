from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('del/<int:id>', views.delete, name='deletePass'),
    path('reg/<int:id>', views.regen, name="regen"),
    path('addPass/', views.addPass, name='addPass')
]
