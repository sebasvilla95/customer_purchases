from rest_framework import serializers
from manage_clients.models import Client, TypeDocument, PaymentType, Purchase
from django.db.models import Sum

#========== Serializer for search client ==========

class ClientReadSerializer(serializers.ModelSerializer):
    type_document = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'type_document',
            'document',
            'name',
            'email',
            'phone',
            'address',
            'status',
        ]

    def get_type_document(self, obj):
        return obj.type_document.name
    
    def get_status(self, obj):
        return obj.get_status_display()

    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

#========== Serializer for retain customers ==========
class PurchaseByClientSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'address',
            'status',
            'total_amount'
        ]

    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
