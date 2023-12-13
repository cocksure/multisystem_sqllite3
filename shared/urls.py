from django.urls import path

from .views import MainMenuListCreateView, SubMenuListCreateView

urlpatterns = [
    path('mainmenu/', MainMenuListCreateView.as_view(), name='mainmenu-list'),
    path('submenu/', SubMenuListCreateView.as_view(), name='submenu-list'),
]
