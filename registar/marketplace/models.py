from django.db import models
from django.utils.translation import gettext_lazy as _


class Marketplace(models.Model):
    class Meta:
        managed = False
        default_permissions = ()

        permissions = ( 
            ("view_shop_marketplace", _("Can view a shop on the marketplace")),
            ("use_shop_from_marketplace", _("Can use a shop from the marketplace")),
        )
