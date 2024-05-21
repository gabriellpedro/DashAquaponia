from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'DashAquaponia'

router = routers.DefaultRouter()
router.register(r'DashModel', views.DashModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.IndexView.as_view(), name="index"),
    path('login/', views.LoginCadastroView, name="login"),
    path('home', views.HomeView.as_view(), name="home"),    

    path('dashpadrao/', views.DashAlfacePadrao.as_view(), name="dashpadrao"),    
    path('dash/', views.DashModificar.as_view(), name="dash"),
    path('servicos/', views.ServicosView.as_view(), name="servicos"),
    path('registro/', views.CadastroDash.as_view(), name="registro"),


    path('perfil/', views.PerfilView, name="perfil"),
    path('logout/', views.logoutView, name="logout"),
    # path('CrescimentoAlface/', views.DashAlface, name="dash"),
    
]