from django.urls import path, include
from drf_spectacular.views import ( 
    SpectacularAPIView,
    SpectacularSwaggerView,
)



urlpatterns = [
    #path('', include(router.urls)),    
    
    # Swagger UI
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
]


