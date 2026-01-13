from django.urls import path, include
from drf_spectacular.views import ( 
    SpectacularAPIView,
    SpectacularSwaggerView,
)



urlpatterns = [
    #path('auth/', include('user.urls')),
    path('chat/', include('chat.urls')),  
    path('notifications/', include('notification.urls')),
    
    # Swagger UI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
]


