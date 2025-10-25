"""
Script para generar todas las visualizaciones de Tendencia vs Ruido
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import seaborn as sns

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Crear directorio para imágenes
output_dir = 'public/images/tendencia'
os.makedirs(output_dir, exist_ok=True)

# Configurar seed para reproducibilidad
np.random.seed(42)

print("Generando visualizaciones...")

# ============================================================================
# 1. GRÁFICO: TENDENCIA VS RUIDO (COMPARACIÓN LADO A LADO)
# ============================================================================
print("1. Tendencia vs Ruido - Comparación...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Datos con tendencia
tiempo = np.arange(0, 100)
tendencia = 0.5 * tiempo
ruido = np.random.normal(0, 5, 100)
datos_con_tendencia = tendencia + ruido

# Gráfico 1: Datos con tendencia
ax1.plot(tiempo, datos_con_tendencia, 'o-', alpha=0.5, color='steelblue', 
         markersize=4, linewidth=1, label='Datos observados')
ax1.plot(tiempo, tendencia, 'r--', linewidth=3, label='Tendencia real')
ax1.set_xlabel('Tiempo', fontsize=12, fontweight='bold')
ax1.set_ylabel('Valor', fontsize=12, fontweight='bold')
ax1.set_title('CON TENDENCIA ✅\n(Patrón direccional claro)', 
              fontsize=13, fontweight='bold', color='green')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Gráfico 2: Solo ruido
solo_ruido = np.random.normal(50, 10, 100)
ax2.plot(tiempo, solo_ruido, 'o-', alpha=0.5, color='gray', 
         markersize=4, linewidth=1, label='Datos observados')
ax2.axhline(y=50, color='orange', linestyle='--', linewidth=3, label='Media constante')
ax2.set_xlabel('Tiempo', fontsize=12, fontweight='bold')
ax2.set_ylabel('Valor', fontsize=12, fontweight='bold')
ax2.set_title('SOLO RUIDO ❌\n(Sin patrón direccional)', 
              fontsize=13, fontweight='bold', color='red')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/01_tendencia_vs_ruido.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 2. GRÁFICO: PROMEDIO MÓVIL
# ============================================================================
print("2. Promedio Móvil...")

plt.figure(figsize=(14, 6))

# Usar los datos con tendencia del ejemplo anterior
datos_df = pd.DataFrame({'valor': datos_con_tendencia})
datos_df['MA_7'] = datos_df['valor'].rolling(window=7).mean()
datos_df['MA_15'] = datos_df['valor'].rolling(window=15).mean()

plt.plot(tiempo, datos_con_tendencia, 'o', alpha=0.3, color='lightblue', 
         markersize=3, label='Datos originales')
plt.plot(tiempo, datos_df['MA_7'], linewidth=2.5, label='Promedio Móvil (7)', color='blue')
plt.plot(tiempo, datos_df['MA_15'], linewidth=2.5, label='Promedio Móvil (15)', color='purple')
plt.plot(tiempo, tendencia, 'r--', linewidth=3, label='Tendencia real', alpha=0.7)
plt.xlabel('Tiempo', fontsize=12, fontweight='bold')
plt.ylabel('Valor', fontsize=12, fontweight='bold')
plt.title('Promedio Móvil Revela la Tendencia Subyacente', fontsize=14, fontweight='bold')
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, alpha=0.3)

plt.savefig(f'{output_dir}/02_promedio_movil.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 3. GRÁFICO: RATIO SEÑAL-RUIDO (COMPARACIÓN)
# ============================================================================
print("3. Ratio Señal-Ruido...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Serie 1: SNR Alto (tendencia clara)
tiempo_snr = np.arange(0, 50)
tendencia_clara = 2 * tiempo_snr
datos_snr_alto = tendencia_clara + np.random.normal(0, 5, 50)

axes[0, 0].plot(tiempo_snr, datos_snr_alto, 'o-', alpha=0.6, color='green', markersize=5)
axes[0, 0].plot(tiempo_snr, tendencia_clara, 'r--', linewidth=2)
axes[0, 0].set_title('🟢 SNR ALTO (> 3.0)\nTendencia Clara', fontsize=12, fontweight='bold', color='green')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_ylabel('Valor', fontweight='bold')

# Serie 2: SNR Medio (tendencia moderada)
tendencia_media = 1 * tiempo_snr
datos_snr_medio = tendencia_media + np.random.normal(0, 10, 50)

axes[0, 1].plot(tiempo_snr, datos_snr_medio, 'o-', alpha=0.6, color='orange', markersize=5)
axes[0, 1].plot(tiempo_snr, tendencia_media, 'r--', linewidth=2)
axes[0, 1].set_title('🟡 SNR MEDIO (1.0-3.0)\nTendencia Moderada', fontsize=12, fontweight='bold', color='orange')
axes[0, 1].grid(True, alpha=0.3)

# Serie 3: SNR Bajo (ruido dominante)
datos_snr_bajo = np.random.normal(25, 15, 50)

axes[1, 0].plot(tiempo_snr, datos_snr_bajo, 'o-', alpha=0.6, color='red', markersize=5)
axes[1, 0].axhline(y=25, color='gray', linestyle='--', linewidth=2)
axes[1, 0].set_title('🔴 SNR BAJO (< 1.0)\nDominado por Ruido', fontsize=12, fontweight='bold', color='red')
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].set_xlabel('Tiempo', fontweight='bold')
axes[1, 0].set_ylabel('Valor', fontweight='bold')

# Serie 4: Tabla de interpretación
axes[1, 1].axis('off')
tabla_data = [
    ['SNR > 3.0', '🟢 Alta', 'Tendencia clara'],
    ['SNR 1.0-3.0', '🟡 Media', 'Requiere análisis'],
    ['SNR < 1.0', '🔴 Baja', 'Ruido dominante']
]
tabla = axes[1, 1].table(cellText=tabla_data, 
                          colLabels=['Ratio', 'Confianza', 'Interpretación'],
                          cellLoc='center',
                          loc='center',
                          colWidths=[0.3, 0.25, 0.45])
tabla.auto_set_font_size(False)
tabla.set_fontsize(11)
tabla.scale(1, 3)

# Estilo de la tabla
for i in range(len(tabla_data) + 1):
    for j in range(3):
        cell = tabla[(i, j)]
        if i == 0:
            cell.set_facecolor('#4472C4')
            cell.set_text_props(weight='bold', color='white')
        else:
            cell.set_facecolor('#E7E6E6' if i % 2 == 0 else 'white')

axes[1, 1].set_title('Interpretación del SNR', fontsize=12, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(f'{output_dir}/03_ratio_señal_ruido.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 4. GRÁFICO: CASO PRÁCTICO - ANÁLISIS DE VENTAS
# ============================================================================
print("4. Caso Práctico - Análisis de Ventas...")

meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
         'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
ventas = [100, 105, 103, 108, 110, 107, 112, 115, 113, 118, 120, 117]

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Gráfico 1: Ventas originales
axes[0, 0].plot(range(len(meses)), ventas, 'o-', linewidth=2.5, markersize=10, 
                color='steelblue', markerfacecolor='lightblue', markeredgewidth=2)
axes[0, 0].set_xticks(range(len(meses)))
axes[0, 0].set_xticklabels(meses, rotation=45)
axes[0, 0].set_ylabel('Ventas (miles)', fontsize=11, fontweight='bold')
axes[0, 0].set_title('Ventas Mensuales Observadas', fontsize=12, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

# Gráfico 2: Con promedio móvil
ventas_df = pd.DataFrame({'mes': meses, 'ventas': ventas})
ventas_df['MA_3'] = ventas_df['ventas'].rolling(window=3).mean()

axes[0, 1].plot(range(len(meses)), ventas, 'o-', alpha=0.5, linewidth=1.5, 
                markersize=6, label='Ventas reales', color='lightblue')
axes[0, 1].plot(range(len(meses)), ventas_df['MA_3'], 's-', linewidth=3, 
                markersize=8, label='Promedio Móvil (3 meses)', color='darkblue')
axes[0, 1].set_xticks(range(len(meses)))
axes[0, 1].set_xticklabels(meses, rotation=45)
axes[0, 1].set_ylabel('Ventas (miles)', fontsize=11, fontweight='bold')
axes[0, 1].set_title('Suavizado con Promedio Móvil', fontsize=12, fontweight='bold')
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(True, alpha=0.3)

# Gráfico 3: Con regresión lineal
x = np.arange(len(ventas))
slope, intercept, r_value, p_value, std_err = linregress(x, ventas)
tendencia_lineal = slope * x + intercept

axes[1, 0].scatter(range(len(meses)), ventas, s=100, alpha=0.7, 
                   color='steelblue', edgecolors='black', linewidth=2, zorder=3)
axes[1, 0].plot(range(len(meses)), tendencia_lineal, 'r--', linewidth=3, 
                label=f'Tendencia: +{slope:.2f} miles/mes')
axes[1, 0].set_xticks(range(len(meses)))
axes[1, 0].set_xticklabels(meses, rotation=45)
axes[1, 0].set_ylabel('Ventas (miles)', fontsize=11, fontweight='bold')
axes[1, 0].set_title(f'Análisis de Tendencia (R²={r_value**2:.3f})', 
                     fontsize=12, fontweight='bold')
axes[1, 0].legend(fontsize=10)
axes[1, 0].grid(True, alpha=0.3)

# Gráfico 4: Residuos
residuos = np.array(ventas) - tendencia_lineal
axes[1, 1].bar(range(len(meses)), residuos, alpha=0.7, 
               color=['green' if r > 0 else 'red' for r in residuos],
               edgecolor='black', linewidth=1.5)
axes[1, 1].axhline(y=0, color='black', linestyle='-', linewidth=2)
axes[1, 1].set_xticks(range(len(meses)))
axes[1, 1].set_xticklabels(meses, rotation=45)
axes[1, 1].set_ylabel('Residuo (miles)', fontsize=11, fontweight='bold')
axes[1, 1].set_title('Residuos (Desviaciones de la Tendencia)', fontsize=12, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/04_caso_practico_ventas.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 5. GRÁFICO: ANÁLISIS COMPLETO (4 PANELES)
# ============================================================================
print("5. Análisis Completo en 4 Paneles...")

# Generar datos de ejemplo
np.random.seed(123)
tiempo_completo = np.arange(0, 60)
tendencia_completa = 0.8 * tiempo_completo + 10
datos_completos = tendencia_completa + np.random.normal(0, 4, 60)

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Panel 1: Datos originales con tendencia
x_comp = np.arange(len(datos_completos))
slope_c, intercept_c, r_value_c, p_value_c, std_err_c = linregress(x_comp, datos_completos)
tendencia_est = slope_c * x_comp + intercept_c
residuos_c = datos_completos - tendencia_est

axes[0, 0].plot(tiempo_completo, datos_completos, 'o-', alpha=0.6, 
                color='steelblue', markersize=4, label='Datos observados')
axes[0, 0].plot(tiempo_completo, tendencia_est, 'r--', linewidth=3, 
                label=f'Tendencia (R²={r_value_c**2:.3f})')
axes[0, 0].set_title('1️⃣ Datos y Tendencia Estimada', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Tiempo', fontweight='bold')
axes[0, 0].set_ylabel('Valor', fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(True, alpha=0.3)

# Panel 2: Promedio móvil
df_comp = pd.DataFrame({'valor': datos_completos})
df_comp['MA'] = df_comp['valor'].rolling(window=7).mean()

axes[0, 1].plot(tiempo_completo, datos_completos, 'o', alpha=0.3, 
                color='lightblue', markersize=3, label='Datos originales')
axes[0, 1].plot(tiempo_completo, df_comp['MA'], linewidth=3, 
                color='darkblue', label='Promedio Móvil (7)')
axes[0, 1].set_title('2️⃣ Suavizado con Promedio Móvil', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Tiempo', fontweight='bold')
axes[0, 1].set_ylabel('Valor', fontweight='bold')
axes[0, 1].legend(fontsize=10)
axes[0, 1].grid(True, alpha=0.3)

# Panel 3: Residuos (deben ser aleatorios)
axes[1, 0].scatter(tiempo_completo, residuos_c, alpha=0.6, s=50, 
                   color='purple', edgecolors='black', linewidth=0.5)
axes[1, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1, 0].fill_between(tiempo_completo, -2*np.std(residuos_c), 2*np.std(residuos_c), 
                         alpha=0.2, color='yellow', label='±2σ')
axes[1, 0].set_title('3️⃣ Residuos (Deben ser Aleatorios)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Tiempo', fontweight='bold')
axes[1, 0].set_ylabel('Residuo', fontweight='bold')
axes[1, 0].legend(fontsize=10)
axes[1, 0].grid(True, alpha=0.3)

# Panel 4: Histograma de residuos (debe ser normal)
axes[1, 1].hist(residuos_c, bins=15, alpha=0.7, color='teal', 
                edgecolor='black', linewidth=1.5)
axes[1, 1].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Media=0')
axes[1, 1].set_title('4️⃣ Distribución de Residuos\n(Debe ser Normal)', 
                     fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Residuo', fontweight='bold')
axes[1, 1].set_ylabel('Frecuencia', fontweight='bold')
axes[1, 1].legend(fontsize=10)
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/05_analisis_completo.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 6. GRÁFICO: EJEMPLOS DE CONFUSIÓN (3 ESCENARIOS)
# ============================================================================
print("6. Ejemplos de Confusión...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Escenario 1: Reversión a la media
tiempo_rev = np.arange(0, 20)
datos_reversion = [100, 120, 105, 98, 102, 115, 100, 95, 103, 108, 
                   100, 110, 98, 105, 100, 112, 99, 103, 100, 105]

axes[0].plot(tiempo_rev, datos_reversion, 'o-', linewidth=2, markersize=8, 
             color='coral', markerfacecolor='white', markeredgewidth=2)
axes[0].axhline(y=np.mean(datos_reversion), color='blue', linestyle='--', 
                linewidth=3, label=f'Media = {np.mean(datos_reversion):.1f}')
axes[0].set_title('❌ REVERSIÓN A LA MEDIA\n(Ruido, NO Tendencia)', 
                  fontsize=11, fontweight='bold', color='red')
axes[0].set_xlabel('Tiempo', fontweight='bold')
axes[0].set_ylabel('Valor', fontweight='bold')
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.3)

# Escenario 2: Muestra pequeña engañosa
tiempo_peq = np.arange(0, 8)
muestra_pequeña = [10, 12, 15, 14, 18, 20, 19, 22]

axes[1].plot(tiempo_peq, muestra_pequeña, 'o-', linewidth=2, markersize=10, 
             color='orange', markerfacecolor='yellow', markeredgewidth=2)
axes[1].set_title('⚠️ MUESTRA PEQUEÑA (n=8)\n(Insuficiente para conclusiones)', 
                  fontsize=11, fontweight='bold', color='orange')
axes[1].set_xlabel('Tiempo', fontweight='bold')
axes[1].set_ylabel('Valor', fontweight='bold')
axes[1].grid(True, alpha=0.3)
axes[1].text(0.5, 0.05, 'n < 30 = Cuidado!', transform=axes[1].transAxes,
             fontsize=12, fontweight='bold', color='red', 
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
             ha='center')

# Escenario 3: Cambio brusco vs tendencia
tiempo_cambio = np.arange(0, 30)
datos_cambio = np.concatenate([
    np.ones(15) * 50 + np.random.normal(0, 3, 15),
    np.ones(15) * 70 + np.random.normal(0, 3, 15)
])

axes[2].plot(tiempo_cambio, datos_cambio, 'o-', linewidth=2, markersize=6, 
             color='purple', alpha=0.7)
axes[2].axvline(x=14.5, color='red', linestyle='--', linewidth=3, label='Cambio brusco')
axes[2].set_title('⚠️ CAMBIO BRUSCO\n(NO es tendencia gradual)', 
                  fontsize=11, fontweight='bold', color='darkorange')
axes[2].set_xlabel('Tiempo', fontweight='bold')
axes[2].set_ylabel('Valor', fontweight='bold')
axes[2].legend(fontsize=9)
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/06_ejemplos_confusion.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 7. GRÁFICO: PERSISTENCIA TEMPORAL
# ============================================================================
print("7. Persistencia Temporal...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Tendencia persistente
meses_pers = np.arange(1, 13)
tendencia_pers = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155]

ax1.plot(meses_pers, tendencia_pers, 'o-', linewidth=3, markersize=12, 
         color='green', markerfacecolor='lightgreen', markeredgewidth=2)
ax1.set_xlabel('Mes', fontsize=12, fontweight='bold')
ax1.set_ylabel('Valor', fontsize=12, fontweight='bold')
ax1.set_title('✅ TENDENCIA PERSISTENTE\n(Dirección consistente)', 
              fontsize=13, fontweight='bold', color='green')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(meses_pers)

# Anotaciones
for i, val in enumerate(tendencia_pers):
    if i % 2 == 0:
        ax1.annotate(f'{val}', xy=(meses_pers[i], val), 
                    xytext=(0, 10), textcoords='offset points',
                    ha='center', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

# Ruido fluctuante
ruido_fluct = [100, 105, 98, 103, 99, 102, 95, 103, 100, 97, 102, 99]

ax2.plot(meses_pers, ruido_fluct, 'o-', linewidth=3, markersize=12, 
         color='red', markerfacecolor='lightcoral', markeredgewidth=2)
ax2.axhline(y=np.mean(ruido_fluct), color='blue', linestyle='--', 
            linewidth=3, label=f'Media = {np.mean(ruido_fluct):.1f}')
ax2.set_xlabel('Mes', fontsize=12, fontweight='bold')
ax2.set_ylabel('Valor', fontsize=12, fontweight='bold')
ax2.set_title('❌ FLUCTUACIÓN ALEATORIA\n(Sin dirección consistente)', 
              fontsize=13, fontweight='bold', color='red')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(meses_pers)

plt.tight_layout()
plt.savefig(f'{output_dir}/07_persistencia_temporal.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"\n✅ ¡Todas las visualizaciones generadas exitosamente en '{output_dir}'!")
print("\nArchivos creados:")
print("  1. 01_tendencia_vs_ruido.png")
print("  2. 02_promedio_movil.png")
print("  3. 03_ratio_señal_ruido.png")
print("  4. 04_caso_practico_ventas.png")
print("  5. 05_analisis_completo.png")
print("  6. 06_ejemplos_confusion.png")
print("  7. 07_persistencia_temporal.png")
