from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from employee_app.views import CustomTokenObtainPairView


def home(request):
    return JsonResponse({
        "message": "EMS Backend is running successfully"
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Employee app APIs
    path('api/', include('employee_app.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    