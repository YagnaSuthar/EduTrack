from django.contrib import admin
from django.urls import path,include
from dashboard.views import CustomPasswordResetView,CustomePasswordResetDoneView
from django.conf import settings
from django.conf.urls.static import static
from student.views import CustomSignupView,register_school_admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('student.urls')),
    path('dashboard-home/',include('dashboard.urls')),
    
    
    # Register as school admin page url
    path('register/', register_school_admin, name='register_school_admin'),
    # Allauth library account url handling
    path('accounts/password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/password/reset/done/', CustomePasswordResetDoneView.as_view(), name='account_reset_password_done'),
    
    
    
    path('accounts/', include('allauth.urls')),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    
    
    
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
