from django.db import models
from django.db.models import Sum

STATUS_CHOICES = [
    (1, 'Activo'),
    (0, 'Inactivo'),
]

class TypeDocument(models.Model):
    """ Tipo de documento, cc, nit, passport, etc. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documento'
        ordering = ['id']
        db_table = 'type_documents'

class Client(models.Model):
    """ Cliente """
    id = models.AutoField(primary_key=True)
    type_document = models.ForeignKey(TypeDocument, on_delete=models.CASCADE)
    document = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    status = models.BooleanField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_total_amount(self):
        """
        Calcula el total de compras del cliente
        """
        total = self.purchases.aggregate(total=Sum('amount'))['total']
        return total if total is not None else 0

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']
        db_table = 'clients'

class PaymentType(models.Model):
    """ Tipo de pago, credit card, debit card, cash, etc. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tipo de pago'
        verbose_name_plural = 'Tipos de pago'
        ordering = ['id']
        db_table = 'payment_types'

class Purchase(models.Model):
    """ Compra realizada y tipo de pago """
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='purchases')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.first_name + ' ' + self.client.last_name
    
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id']
        db_table = 'purchases'