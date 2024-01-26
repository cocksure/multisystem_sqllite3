from rest_framework.serializers import ValidationError as DRFValidationError

from apps.depo.models.stock import Stock


def validate_outgoing(instance):
    if instance.warehouse and not instance.warehouse.can_export:
        raise DRFValidationError("Невозможно расходовать!")
    if instance.warehouse and not instance.warehouse.is_active:
        raise DRFValidationError("Невозможно расходовать для неактивного склада.")


def validate_movement_outgoing(instance):
    if not instance:
        return

    if instance.outgoing_type == instance.OutgoingType.MOVEMENT and not instance.to_warehouse:
        raise DRFValidationError({'__all__': ['Выберите склад в поле "to_warehouse", так как тип - перемещения.']})
    if instance.to_warehouse == instance.warehouse:
        raise DRFValidationError({'__all__': ['Нельзя перемещать товары на тот же самый склад.']})

    return True


def validate_use_negative(outgoing, outgoing_material_data):
    warehouse = outgoing.warehouse
    use_negative = warehouse.use_negative

    for item in outgoing_material_data.all():
        material = item.material
        amount = item.amount

        stock, created = Stock.objects.get_or_create(material=material, warehouse=warehouse)

        if not use_negative and stock.amount < amount:
            raise DRFValidationError('Not enough stock available.')

        stock.amount -= amount
        stock.save()


def process_incoming(incoming):
    if incoming.from_warehouse:
        incoming.incoming_type = 'Перемешения'
    else:
        incoming.incoming_type = 'По накладной'


def validate_incoming(instance):
    if instance.warehouse and not instance.warehouse.can_import:
        raise DRFValidationError('Невозможно создать приход для склада, который не может импортировать.')
    if instance.warehouse and not instance.warehouse.is_active:
        raise DRFValidationError("Невозможно создать приход для неактивного склада.")

    if instance.incoming_type == 'По накладной' and not instance.invoice:
        raise DRFValidationError('Необходимо указать номер инвойса.')
