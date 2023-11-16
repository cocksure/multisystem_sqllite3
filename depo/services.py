from django.core.exceptions import ValidationError


def validate_outgoing(instance):
    if instance.warehouse and not instance.warehouse.can_export:
        raise ValidationError("Невозможно расходовать!")
    if instance.warehouse and not instance.warehouse.is_active:
        raise ValidationError("Невозможно расходовать для неактивного склада.")


def validate_movement_outgoing(instance):
    if not instance.to_warehouse:
        raise ValidationError('Выберите склад в поле "to_warehouse", так как тип - перемещения.')
    if instance.to_warehouse == instance.warehouse:
        raise ValidationError('Нельзя перемещать товары на тот же самый склад.')


def process_incoming(incoming):
    if incoming.from_warehouse:
        incoming.type = 'Перемешения'
    else:
        incoming.type = 'По накладной'


def validate_incoming(instance):
    if instance.warehouse and not instance.warehouse.can_import:
        raise ValidationError('Невозможно создать приход для склада, который не может импортировать.')
    if instance.warehouse and not instance.warehouse.is_active:
        raise ValidationError("Невозможно создать приход для неактивного склада.")

    if instance.type == 'По накладной' and not instance.invoice:
        raise ValidationError('Необходимо указать номер инвойса.')
