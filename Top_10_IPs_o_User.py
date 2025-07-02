import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, filedialog

# === OCULTAR VENTANA PRINCIPAL DE TKINTER ===
Tk().withdraw()

# === SELECCIONAR CSV DE INCIDENTES ===
ruta_csv = filedialog.askopenfilename(
    title="Selecciona el archivo CSV de incidentes FortiSIEM",
    filetypes=[("CSV files", "*.csv")]
)

# === CARGAR Y PROCESAR DATOS ===
df = pd.read_csv(ruta_csv)
df['Origen'] = df['Origen'].fillna('Desconocido')  # Ajusta el nombre de columna según tu archivo

# === CALCULAR TOP 10 DE IPs/USUARIOS CON MÁS INCIDENTES ===
top_origen = df['Origen'].value_counts().head(10)

# === VISUALIZACIÓN CON SEABORN ===
plt.figure(figsize=(10, 6))
sns.set_style("whitegrid")
ax = sns.barplot(x=top_origen.values, y=top_origen.index, palette="flare")
plt.title('Top 10 IPs/Usuarios con Más Incidentes', fontsize=14)
plt.xlabel('Número de Incidentes')
plt.ylabel('Origen (IP o Usuario)')
plt.tight_layout()
plt.show()

# === GUARDAR GRÁFICO COMO IMAGEN ===
ruta_guardado = filedialog.asksaveasfilename(
    defaultextension=".png",
    title="Guardar gráfico como imagen",
    filetypes=[("PNG files", "*.png")]
)
if ruta_guardado:
    plt.savefig(ruta_guardado, format='png')
    print(f"Gráfico guardado en: {ruta_guardado}")
