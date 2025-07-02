import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, filedialog

# === ABRIR VENTANA PARA SELECCIONAR EL CSV ===
Tk().withdraw()  # Oculta la ventana principal de Tkinter
ruta_csv = filedialog.askopenfilename(title="Selecciona el archivo CSV de incidentes FortiSIEM", filetypes=[("CSV files", "*.csv")])

# === CARGAR EL ARCHIVO CSV SELECCIONADO ===
df = pd.read_csv(ruta_csv)

# === PROCESAMIENTO DE DATOS ===
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Severidad'] = df['Severidad'].str.capitalize()

# === CONTEO POR SEVERIDAD ===
conteo = df.groupby(['Fecha', 'Severidad']).size().unstack(fill_value=0)
niveles = ['Crítico', 'Medio', 'Bajo']
conteo = conteo.reindex(columns=niveles, fill_value=0)

# === VISUALIZACIÓN ===
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")
sns.lineplot(data=conteo, palette="rocket", linewidth=2.5)
plt.title('Evolución de Incidentes FortiSIEM por Severidad', fontsize=14)
plt.ylabel('Número de Incidentes')
plt.xlabel('Fecha')
plt.xticks(rotation=45)
plt.legend(title='Severidad')
plt.tight_layout()
plt.show()
# === GUARDAR GRÁFICO COMO IMAGEN ===
ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png", title="Guardar gráfico como imagen", filetypes=[("PNG files", "*.png")])
if ruta_guardado:
    plt.savefig(ruta_guardado, format='png')
    print(f"Gráfico guardado en: {ruta_guardado}")  
    