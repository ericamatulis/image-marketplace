from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'personal'  # here for namespacing of urls.


urlpatterns = [
    url(r'^$', views.index, name='index'),
    path("register", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("login", views.login_request, name="login"),
    path("profile", views.profile, name="profile"),
    path("your_market", views.your_market_request, name="your_market"),
    path("upload/", views.upload_request, name="upload"),
    path("edit/", views.update_request, name="edit"),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path("your_transactions/", views.transactions_request, name="your_transactions"),
    path("product/", views.product_request, name="product"),
]