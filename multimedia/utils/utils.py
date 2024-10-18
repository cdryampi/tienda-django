from django.contrib.staticfiles import finders

def archivo_existe(ruta_relativa):
    ruta_completa = finders.find(ruta_relativa)
    print(f"Ruta completa: {ruta_completa}")
    return ruta_completa
