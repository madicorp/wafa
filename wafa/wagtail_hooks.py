# Register Photologue models inside Wagtail admin using ModelAdmin
try:
    from wagtail.contrib.modeladmin.options import (
        ModelAdmin,
        ModelAdminGroup,
        modeladmin_register,
    )
except Exception:  # Fallback if modeladmin is unavailable in analysis
    ModelAdmin = None
    ModelAdminGroup = None
    def modeladmin_register(arg):  # type: ignore
        return arg

try:
    from photologue.models import Photo, Gallery, PhotoEffect, PhotoSize, Watermark
except Exception:  # pragma: no cover - photologue should be installed per settings
    Photo = Gallery = PhotoEffect = PhotoSize = Watermark = None

# If modeladmin is available, provide a dedicated Photologue menu in Wagtail admin
if ModelAdmin and ModelAdminGroup and Photo is not None:

    class PhotoAdmin(ModelAdmin):
        model = Photo
        menu_label = "Photos"
        add_to_settings_menu = False
        exclude_from_explorer = True
        list_display = ("title", "date_added", "is_public")
        search_fields = ("title", "slug", "caption")
        list_filter = ("is_public", "date_added")


    class GalleryAdmin(ModelAdmin):
        model = Gallery
        menu_label = "Galleries"
        add_to_settings_menu = False
        exclude_from_explorer = True
        list_display = ("title", "date_added", "is_public")
        search_fields = ("title", "slug", "description")
        list_filter = ("is_public", "date_added")


    class PhotoEffectAdmin(ModelAdmin):
        model = PhotoEffect
        menu_label = "Effects"
        add_to_settings_menu = False
        exclude_from_explorer = True
        list_display = ("name",)
        search_fields = ("name",)


    class PhotoSizeAdmin(ModelAdmin):
        model = PhotoSize
        menu_label = "Sizes"
        add_to_settings_menu = False
        exclude_from_explorer = True
        list_display = ("name", "width", "height")
        search_fields = ("name",)


    class WatermarkAdmin(ModelAdmin):
        model = Watermark
        menu_label = "Watermarks"
        add_to_settings_menu = False
        exclude_from_explorer = True
        list_display = ("name",)
        search_fields = ("name",)


    class PhotologueGroup(ModelAdminGroup):
        menu_label = "Photologue"
        menu_icon = "image"  # Wagtail icon name
        items = (
            PhotoAdmin,
            GalleryAdmin,
            PhotoEffectAdmin,
            PhotoSizeAdmin,
            WatermarkAdmin,
        )

    modeladmin_register(PhotologueGroup)

else:
    # No ModelAdmin; we'll rely on Snippet ViewSets if available, with a later fallback.
    pass

# Admin ViewSets: group related snippets under a dedicated submenu in the main admin
try:
    # Wagtail 5+ viewsets API
    from wagtail.snippets.views.snippets import SnippetViewSet
    from wagtail.admin.viewsets.base import ViewSetGroup
    from wagtail import hooks
except Exception:
    SnippetViewSet = None
    ViewSetGroup = None

if SnippetViewSet and ViewSetGroup:
    # Try importing our models; guard if optional apps are missing
    try:
        from advertising.models import Advertising
    except Exception:
        Advertising = None
    try:
        from photologue.models import Photo as PLPhoto, Gallery as PLGallery, PhotoEffect as PLEffect, PhotoSize as PLSize, Watermark as PLWatermark
    except Exception:
        PLPhoto = PLGallery = PLEffect = PLSize = PLWatermark = None

    # Define SnippetViewSets for each model we want to group
    viewsets = []

    if Advertising is not None:
        class AdvertisingViewSet(SnippetViewSet):
            model = Advertising
            menu_label = "Advertising"
            icon = "snippet"
        viewsets.append(AdvertisingViewSet)

    if PLPhoto is not None:
        class PhotoViewSet(SnippetViewSet):
            model = PLPhoto
            menu_label = "Photos"
            icon = "image"
        viewsets.append(PhotoViewSet)

    if PLGallery is not None:
        class GalleryViewSet(SnippetViewSet):
            model = PLGallery
            menu_label = "Galleries"
            icon = "image"
        viewsets.append(GalleryViewSet)

    if PLEffect is not None:
        class PhotoEffectViewSet(SnippetViewSet):
            model = PLEffect
            menu_label = "Effects"
            icon = "cog"
        viewsets.append(PhotoEffectViewSet)

    if PLSize is not None:
        class PhotoSizeViewSet(SnippetViewSet):
            model = PLSize
            menu_label = "Sizes"
            icon = "site"
        viewsets.append(PhotoSizeViewSet)

    if PLWatermark is not None:
        class WatermarkViewSet(SnippetViewSet):
            model = PLWatermark
            menu_label = "Watermarks"
            icon = "pick"
        viewsets.append(WatermarkViewSet)

    if viewsets:
        # Build separate groups: one for Photologue, one for Advertising.
        photologue_items = tuple(
            vs for vs in viewsets
            if vs.__name__ in ("PhotoViewSet", "GalleryViewSet", "PhotoEffectViewSet", "PhotoSizeViewSet", "WatermarkViewSet")
        )
        advertising_items = tuple(
            vs for vs in viewsets
            if vs.__name__ == "AdvertisingViewSet"
        )

        if photologue_items:
            class PhotologueGroup(ViewSetGroup):
                menu_label = "Photologue"
                menu_icon = "image"
                items = photologue_items

            @hooks.register('register_admin_viewset')
            def register_photologue_group():
                # Return an instance to satisfy environments expecting instance-based registration
                return PhotologueGroup()

        if advertising_items:
            class AdvertisingGroup(ViewSetGroup):
                menu_label = "Advertising"
                menu_icon = "snippet"
                items = advertising_items

            @hooks.register('register_admin_viewset')
            def register_advertising_group():
                # Return an instance to satisfy environments expecting instance-based registration
                return AdvertisingGroup()
else:
    # Fallback: if viewsets API is unavailable, register snippets directly
    try:
        from wagtail.snippets.models import register_snippet  # type: ignore
        # Advertising
        from advertising.models import Advertising  # type: ignore
        register_snippet(Advertising)
        # Photologue models (if available)
        try:
            from photologue.models import Photo as PLPhoto, Gallery as PLGallery, PhotoEffect as PLEffect, PhotoSize as PLSize, Watermark as PLWatermark  # type: ignore
            if PLPhoto is not None:
                register_snippet(PLPhoto)
            if PLGallery is not None:
                register_snippet(PLGallery)
            if PLEffect is not None:
                register_snippet(PLEffect)
            if PLSize is not None:
                register_snippet(PLSize)
            if PLWatermark is not None:
                register_snippet(PLWatermark)
        except Exception:
            pass
    except Exception:
        # As a last resort, do nothing; Wagtail admin will still be usable.
        pass
