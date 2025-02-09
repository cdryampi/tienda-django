from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # ✅ Rutas que no deben ser afectadas por el idioma
    path("cart/", include("cart.urls")),  # Evita que tenga `/es/cart/`
    path("payments/", include("payments.urls")),  # Evita `/es/payments/`
    path("i18n/", include("django.conf.urls.i18n")),  # Cambio de idioma manual
]

# ✅ Rutas que sí necesitan soporte de idioma
urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    path("productos/", include("product.urls")),
    path("secure_admin/", admin.site.urls, name="admin"),
    path("accounts/", include("accounts.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls"), name="ck_editor_5_upload_file"),
)

# ✅ Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
