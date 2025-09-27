from manage_clients.v1.views import ClientsViewSet, TypeDocumentsViewSet, PaymentTypesViewSet, PurchasesViewSet, ClientReadViewSet, DataExportView, RetainCustomersViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'clients', ClientsViewSet, basename='clients')
router.register(r'type-documents', TypeDocumentsViewSet, basename='type-documents')
router.register(r'payment-types', PaymentTypesViewSet, basename='payment-types')
router.register(r'purchases', PurchasesViewSet, basename='purchases')

urlpatterns = [
    path('search-client/', ClientReadViewSet.as_view(), name='client-read'),
    path('data-export/', DataExportView.as_view(), name='data-export'),
    path('retain-customers/', RetainCustomersViewSet.as_view(), name='retain-customers'),
] + router.urls