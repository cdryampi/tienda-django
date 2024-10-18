#tienda/core/admin/utils.py

# Campos manuales del MetadataModel
METADATA_FIELDS = (
    'meta_titulo',
    'meta_descripcion',
)

# Campos automáticos del MetaBase
METABASE_FIELDS = (
    'created_at', 
    'updated_at', 
    'is_active',
)

# Campos de auditoría, si es necesario incluirlos también
AUDIT_FIELDS = (
    'created_by',
    'updated_by',
)

SLUG = (
    'slug',
)

MEDIA = (
    'imagen',
    'file'
)