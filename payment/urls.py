from django.urls import path
from .views import (
    # ProductPreview, 
    # home,
    CreateCheckOutSession, 
    StripeWebhookView
)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('webhook/', csrf_exempt(StripeWebhookView.as_view()), name='stripe-webhook'),
    # path("checkout/home/", home, name="home"),
    # path('product/<int:pk>/', ProductPreview.as_view(), name="product"),
    path('create-checkout-session/<pk>/', csrf_exempt(CreateCheckOutSession.as_view()), name='checkout_session'),
]