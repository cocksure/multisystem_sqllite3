from apps.info.views import material, warehouse
from apps.info.views import infos
from rest_framework import routers

app_name = 'info'
router = routers.DefaultRouter()

router.register(r'specification', infos.SpecificationViewSetView)
router.register(r'unit', infos.UnitViewSetView)
router.register(r'firm', infos.FirmViewSetView)
router.register(r'device', infos.DeviceViewSetView)
router.register(r'currency', infos.CurrencyViewSetView)
router.register(r'dealer', infos.DealerViewSetView)
router.register(r'brand', infos.BrandViewSetView)

router.register(r'material/group', material.MaterialGroupViewSetView)
router.register(r'material/type', material.MaterialTypeViewSetView)
router.register(r'material', material.MaterialViewSetView)

router.register(r'warehouse', warehouse.WarehouseViewSetView)

urlpatterns = []

urlpatterns += router.urls
