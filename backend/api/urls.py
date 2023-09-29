"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from gerund import views


router = routers.DefaultRouter()
router.register(r'outgoing_messages', views.OutgoingVariationView, 'outgoing_messages')
router.register(r'answers', views.AnswerView, 'answers')
router.register(r'incoming_embeddings', views.IncomingEmbeddingView, 'incoming_embeddings')
router.register(r'questions', views.QuestionView, 'questions')
router.register(r'scripts', views.ScriptView, 'scripts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api/', include(router.urls)),
]
