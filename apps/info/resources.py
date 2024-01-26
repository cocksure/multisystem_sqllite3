from import_export import resources

from apps.info import models


class MaterialResource(resources.ModelResource):
    class Meta:
        model = models.Material
        fields = ('id', 'code', 'name', 'group', 'type', 'unit', 'color')