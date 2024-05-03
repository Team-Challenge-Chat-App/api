from rest_framework.routers import DefaultRouter

from tc_chat.chats import views

router = DefaultRouter()
router.register("groups", views.ChatGroupViewSet)
urlpatterns = [] + router.urls
