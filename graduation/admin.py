from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(GeneralUser)
admin.site.register(AdminUser)
admin.site.register(District)
admin.site.register(Transportation)
admin.site.register(Place)
admin.site.register(TouristArea)
admin.site.register(GuideCourse)
admin.site.register(GuideCourseLike)
admin.site.register(AddGuideCourse)
admin.site.register(StoreCategory)
admin.site.register(StoreSubCategory)
admin.site.register(Store)
admin.site.register(GourmetCategory)
admin.site.register(Gourmet)
admin.site.register(Restaurant)
admin.site.register(StoreGourmet)
admin.site.register(Stamp)
admin.site.register(StampRally)
admin.site.register(PlaceLike)