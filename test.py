try:
    import vpython as vp
    print(f"✅ vpython {vp.__version__} instalado correctamente")
except ImportError as e:
    print(f"❌ Error importando vpython: {e}")
    print("Posibles causas:")
    print("1. Paquete corrupto")
    print("2. Dependencias faltantes")
    print("3. Problema de PATH")