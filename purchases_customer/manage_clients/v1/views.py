from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from manage_clients.models import Client, TypeDocument, PaymentType, Purchase
from manage_clients.v1.serializers.serializers import ClientSerializer, TypeDocumentSerializer, PaymentTypeSerializer, PurchaseSerializer
from manage_clients.v1.serializers.read_serializers import ClientReadSerializer, PurchaseByClientSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from django.http import HttpResponse
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import ValidationError, NotFound
from django.db.models import Q, Sum, Case, When, DecimalField
from django.utils import timezone
from datetime import timedelta


class ClientsViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class TypeDocumentsViewSet(ModelViewSet):
    queryset = TypeDocument.objects.all()
    serializer_class = TypeDocumentSerializer

class PaymentTypesViewSet(ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

class PurchasesViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


#========== Read views ==========
class ClientReadViewSet(RetrieveAPIView):
    """
    Vista para recuperar un cliente. No maneja listas.
    """
    queryset = Client.objects.all()
    serializer_class = ClientReadSerializer
    
    def get_object(self):
        document = self.request.query_params.get('document')
        type_document = self.request.query_params.get('type_document')
        
        if not document or not type_document:
            raise ValidationError({
                'error': 'Los parámetros document y type_document son requeridos'
            })
        
        try:
            return Client.objects.get(
                document=document,
                type_document=type_document
            )
        except Client.DoesNotExist:
            raise NotFound('Cliente no encontrado')

#========== Export data client ==========

""" Exportar en un dataframe la entrada tipo json """
class DataExportView(APIView):
    
    def post(self, request):
        #Solicita como entrada el vector de datos resultante de la cosulta
        results  = request.data

        try: 
            #Desde pandas mediante el método de DataFrame procesamos los datos del vector
            data_export = pd.DataFrame(results)

            # Crea un archivo Excel en memoria
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="info_client.xlsx"'

            #Guarda el dataframe en la respuesta de la hoja de cálculo
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                data_export.to_excel(writer, index=False, sheet_name='results')

            return response
        
        except Exception as e:

            return Response({
                'error': 'Error al generar el archivo Excel',
                'detalle': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


#========== Retain customers ==========

class RetainCustomersViewSet(ListAPIView):
    """
    Vista para fidelizar los clientes que han realizado compras mayores a 5000000. 
    """
    serializer_class = PurchaseByClientSerializer

    def get_queryset(self):
        # Calcular la fecha de hace un mes y la fecha actual
        one_month_ago = timezone.now() - timedelta(days=30)
        
        # Anotar el total de compras de cada cliente
        queryset = Client.objects.annotate(
            total_amount=Sum(
                Case(
                    When(
                        purchases__created_at__gte=one_month_ago,
                        purchases__created_at__lte=timezone.now(),
                        then='purchases__amount'
                    ),
                    default=0,
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            )
        ).filter(
            Q(total_amount__gt=5000000) &
            Q(status=1)
        ).distinct()
        
        return queryset