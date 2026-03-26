from django.contrib import admin
from .models import Article


@admin.register(Article)                        # современный и удобный способ
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "get_excerpt",
        "created_date",
    )
    list_display_links = ("title",)             # кликабельное название
    list_filter = ("author", "created_date")    # фильтры справа
    search_fields = ("title", "text")           # поиск
    date_hierarchy = "created_date"             # иерархия по датам
    ordering = ("-created_date",)

    # Опционально — более красивое отображение формы редактирования
    fieldsets = (
        (None, {
            "fields": ("title", "author")
        }),
        ("Содержание", {
            "fields": ("text",),
            "classes": ("wide",),
        }),
        ("Даты", {
            "fields": ("created_date",),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("created_date",)         # нельзя редактировать