from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.db.models import F
from .models import incoming, outgoing, stock


@receiver(pre_save, sender=outgoing.Outgoing)
def set_outgoing_status(sender, instance, **kwargs):
    # Проверяем, был ли установлен type в значение "перемешения"
    if instance.outgoing_type == 'перемешения':
        instance.status = 'В ожидании'
    else:
        instance.status = 'Принят'

# @receiver(post_delete, sender=IncomingMaterial)
# def update_stock_after_IncomingMaterial_deletion(sender, instance, **kwargs):
#     material = instance.material
#     warehouse = instance.incoming.warehouse if hasattr(instance, 'incoming') else None
#     if warehouse:
#         Stock.objects.filter(material=material, warehouse=warehouse).update(amount=F('amount') - instance.amount)
#
#
# @receiver(post_delete, sender=OutgoingMaterial)
# def update_stock_after_OutgoingMaterial_deletion(sender, instance, **kwargs):
#     material = instance.material
#     warehouse = instance.outgoing.warehouse if hasattr(instance, 'outgoing') else None
#     if warehouse:
#         Stock.objects.filter(material=material, warehouse=warehouse).update(amount=F('amount') + instance.amount)
#
#
# @receiver(post_save, sender=IncomingMaterial)
# def update_stock_after_IncomingMaterial_save(sender, instance, **kwargs):
#     material = instance.material
#     warehouse = instance.incoming.warehouse if hasattr(instance, 'incoming') else None
#     if warehouse:
#         Stock.objects.filter(material=material, warehouse=warehouse).update(amount=F('amount') - instance.amount)
#
#
# @receiver(post_save, sender=OutgoingMaterial)
# def update_stock_after_OutgoingMaterial_save(sender, instance, **kwargs):
#     material = instance.material
#     warehouse = instance.outgoing.warehouse if hasattr(instance, 'outgoing') else None
#     if warehouse:
#         Stock.objects.filter(material=material, warehouse=warehouse).update(amount=F('amount') + instance.amount)
