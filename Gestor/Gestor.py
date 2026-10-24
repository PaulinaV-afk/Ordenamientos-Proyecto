import json
import glob

def ejecutar_gestor():
    # Buscar todos los archivos JSON de resultados en la carpeta
    archivos = glob.glob("resultados_*.json")
    
    if not archivos:
        print("No se encontraron archivos JSON de resultados. Ejecuta los benchmarks de los lenguajes primero.")
        return

    datos_totales = []
    for archivo in archivos:
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos_totales.extend(json.load(f))
        except Exception as e:
            print(f"Error al leer {archivo}: {e}")

    if not datos_totales:
        print("Los archivos JSON están vacíos.")
        return

    print("=" * 70)
    print("           REPORTE GENERAL Y COMPARATIVO DE BENCHMARK           ")
    print("=" * 70 + "\n")

    # 1. TIEMPO TOTAL DE EJECUCIÓN
    tiempos_lang = {}
    tiempos_alg = {}
    for d in datos_totales:
        lang = d["lenguaje"]
        alg = d["algoritmo"]
        t = d["tiempo_ms"]
        tiempos_lang[lang] = tiempos_lang.get(lang, 0) + t
        tiempos_alg[alg] = tiempos_alg.get(alg, 0) + t

    print("⏱️ 1. TIEMPO TOTAL DE EJECUCIÓN:")
    print("   [Por Lenguaje]")
    for lang, tiempo in sorted(tiempos_lang.items(), key=lambda x: x[1]):
        print(f"      - {lang}: {tiempo:,.2f} ms")
    
    print("\n   [Por Algoritmo]")
    for alg, tiempo in sorted(tiempos_alg.items(), key=lambda x: x[1]):
        print(f"      - {alg}: {tiempo:,.2f} ms")

    # 2. NÚMERO DE COMPARACIONES
    comp_alg = {}
    for d in datos_totales:
        alg = d["algoritmo"]
        comp_alg[alg] = comp_alg.get(alg, 0) + d["comparaciones"]

    print("\n" + "-" * 70)
    print("🔍 2. NÚMERO TOTAL DE COMPARACIONES (Acumulado global):")
    for alg, comp in sorted(comp_alg.items(), key=lambda x: x[1]):
        print(f"      - {alg}: {comp:,} comparaciones")

    # 3. NÚMERO DE INTERCAMBIOS
    inter_alg = {}
    for d in datos_totales:
        alg = d["algoritmo"]
        inter_alg[alg] = inter_alg.get(alg, 0) + d["intercambios"]

    print("\n" + "-" * 70)
    print("🔄 3. NÚMERO TOTAL DE INTERCAMBIOS / MOVIMIENTOS (Acumulado global):")
    for alg, inter in sorted(inter_alg.items(), key=lambda x: x[1]):
        print(f"      - {alg}: {inter:,} intercambios")

    # RESUMEN DE GANADORES
    lang_ganador = min(tiempos_lang, key=tiempos_lang.get)
    alg_ganador = min(tiempos_alg, key=tiempos_alg.get)

    print("\n" + "=" * 70)
    print("🏆 CONCLUSIONES FINALES:")
    print(f"   * Lenguaje más rápido en total: **{lang_ganador}**")
    print(f"   * Algoritmo más rápido en total: **{alg_ganador}**")
    print("=" * 70)

if __name__ == "__main__":
    ejecutar_gestor()