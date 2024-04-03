from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.home, name="home"),
    path('search',views.search, name="search"),
    path('chatbot',views.chatbot, name="chatbot"),
    path('search_compound',views.search_compound, name="search_compound"),
    path('team',views.team, name="team"),
    path('journal',views.journal, name="journal"),
    path('app',views.predict, name="app"),
    path('manual_app',views.ml_ops, name="manual_app"),
    path('view_pdf/<str:orang>/', views.view_pdf, name='view_pdf'),
    path('inputan_user/', views.inputan_user, name='inputan_user'),
    
]