from django.contrib import admin

from .models import Favorite


# Register your models here.


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tmdb_id",
        "poster_path",
        "user",
    )

    list_filter = [
        "user",
    ]

    search_fields = [
        "name",
    ]
    pass


admin.site.register(Favorite, FavoriteAdmin)
