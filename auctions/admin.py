from django.contrib import admin

from .models import Categories, User
from .models import AuctionListing
from .models import WatchList
from .models import AuctionComments
from .models import AuctionBids
from .models import ClosedAuctions

# Register your models here.

admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(WatchList)
admin.site.register(Categories)
admin.site.register(AuctionBids)
admin.site.register(AuctionComments)
admin.site.register(ClosedAuctions)