from django.contrib import admin
from django.urls import path,include
from dashboard.views import CustomPasswordResetView,CustomePasswordResetDoneView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('student.urls')),
    path('dashboard-home/',include('dashboard.urls')),
    
    
    
    
    
    
    
    
    
    # Allauth library account url handling
    path('accounts/password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/password/reset/done/', CustomePasswordResetDoneView.as_view(), name='account_reset_password_done'),

    path('accounts/', include('allauth.urls')),
]
