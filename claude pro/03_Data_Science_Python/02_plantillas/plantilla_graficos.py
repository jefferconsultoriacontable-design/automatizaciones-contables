"""
PLANTILLA DE GRAFICOS PARA INFORMES CONTABLES (matplotlib)

    python plantilla_graficos.py ../01_kit_pandas_contable/datos/libro_auxiliar.csv

Genera cuatro PNG en salidas/ listos para pegar en Word o PowerPoint:
    01_ventas_por_mes.png        barras, una serie, valores rotulados
    02_top_gastos.png            barras horizontales ordenadas
    03_ingresos_vs_costos.png    dos lineas en un solo eje, con rotulo al final
    04_composicion_gasto.png     barras apiladas por centro de costo

Reglas de diseno aplicadas (sirven para cualquier grafico que hagas despues)
---------------------------------------------------------------------------
- Un solo eje Y. Nunca dos escalas en el mismo grafico: si necesitas comparar
  dos magnitudes distintas, son dos graficos.
- Paleta fija y validada para daltonismo; los colores se asignan en orden,
  nunca se reciclan ni se reordenan al filtrar.
- Rotulos directos en vez de leyenda cuando hay una o dos series.
- Rejilla tenue y solo horizontal; sin bordes de caja; sin efectos 3D.
- Los valores se muestran en millones para que se lean de un vistazo.
- Ordena siempre por magnitud lo que sea categorico (no alfabeticamente).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

# paleta categorica validada (contraste y separacion para daltonismo)
AZUL, NARANJA, TEAL, MORADO, ROJO = "#1F6FD0", "#C96A00", "#00A19A", "#8B5CF6", "#D62828"
PALETA = [AZUL, NARANJA, TEAL, MORADO, ROJO]
TINTA, TINTA_SUAVE, REJILLA = "#1F2328", "#5A6472", "#E3E7EC"

plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "font.size": 10,
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.titlecolor": TINTA,
    "axes.labelcolor": TINTA_SUAVE,
    "axes.edgecolor": REJILLA,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "xtick.color": TINTA_SUAVE,
    "ytick.color": TINTA_SUAVE,
    "grid.color": REJILLA,
    "grid.linewidth": 0.8,
    "legend.frameon": False,
})

SAL = Path("salidas")


def millones(x, _=None) -> str:
    return f"{x/1e6:,.0f}M"


def encabezado(ax, titulo, subtitulo=None, con_leyenda=False):
    """Titulo, subtitulo y espacio para la leyenda, medidos en puntos: asi la
    separacion es la misma sin importar el alto de la figura."""
    alto = 48 if con_leyenda else (30 if subtitulo else 12)
    ax.set_title(titulo, loc="left", pad=alto)
    if subtitulo:
        ax.annotate(subtitulo, xy=(0, 1), xycoords="axes fraction",
                    xytext=(0, alto - 22), textcoords="offset points",
                    fontsize=9, color=TINTA_SUAVE, va="bottom")


def base(ax, titulo, subtitulo=None, eje_y=True, con_leyenda=False):
    encabezado(ax, titulo, subtitulo, con_leyenda)
    if eje_y:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(millones))
        ax.grid(axis="y", alpha=0.9)
        ax.set_axisbelow(True)
    return ax


def guardar(fig, nombre):
    SAL.mkdir(parents=True, exist_ok=True)
    ruta = SAL / nombre
    fig.savefig(ruta)
    plt.close(fig)
    print("  ", ruta)


# --------------------------------------------------------------------------- #
def grafico_barras_mes(serie: pd.Series, titulo: str, nombre: str):
    fig, ax = plt.subplots(figsize=(8, 4.2))
    x = [str(p) for p in serie.index]
    barras = ax.bar(x, serie.values, color=AZUL, width=0.62)
    for b, v in zip(barras, serie.values):                       # rotulo directo
        ax.annotate(millones(v), (b.get_x() + b.get_width() / 2, v),
                    ha="center", va="bottom", fontsize=9, color=TINTA, xytext=(0, 3),
                    textcoords="offset points")
    base(ax, titulo, f"Total del periodo: {millones(serie.sum())}")
    ax.set_ylim(0, serie.max() * 1.18)
    ax.spines["bottom"].set_color(REJILLA)
    guardar(fig, nombre)


def grafico_barras_h(serie: pd.Series, titulo: str, nombre: str, color=NARANJA):
    serie = serie.sort_values()
    fig, ax = plt.subplots(figsize=(8, 0.42 * len(serie) + 1.8))
    ax.barh(serie.index, serie.values, color=color, height=0.62)
    for i, v in enumerate(serie.values):
        ax.annotate(millones(v), (v, i), va="center", fontsize=9, color=TINTA,
                    xytext=(5, 0), textcoords="offset points")
    encabezado(ax, titulo)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(millones))
    ax.grid(axis="x", alpha=0.9)
    ax.set_axisbelow(True)
    ax.set_xlim(0, serie.max() * 1.15)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", labelbottom=False, length=0)
    guardar(fig, nombre)


def grafico_lineas(df: pd.DataFrame, titulo: str, nombre: str):
    fig, ax = plt.subplots(figsize=(8, 4.4))
    x = [str(p) for p in df.index]
    for i, col in enumerate(df.columns):
        ax.plot(x, df[col], color=PALETA[i], linewidth=2.2, marker="o", markersize=6,
                markeredgecolor="white", markeredgewidth=1.2, label=col)
        ax.annotate(f" {col}", (x[-1], df[col].iloc[-1]), color=PALETA[i],
                    fontsize=9.5, va="center", fontweight="bold")   # rotulo al final
    base(ax, titulo, "Un solo eje: las dos series son comparables entre si",
         con_leyenda=True)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncols=len(df.columns), fontsize=9)
    ax.margins(x=0.16)
    guardar(fig, nombre)


def grafico_apilado(tabla: pd.DataFrame, titulo: str, nombre: str):
    fig, ax = plt.subplots(figsize=(8, 4.4))
    x = [str(p) for p in tabla.index]
    acum = None
    for i, col in enumerate(tabla.columns):
        ax.bar(x, tabla[col], bottom=acum, color=PALETA[i], width=0.6,
               label=str(col), edgecolor="white", linewidth=2)      # separacion de 2px
        acum = tabla[col] if acum is None else acum + tabla[col]
    base(ax, titulo, "Composicion por centro de costo", con_leyenda=True)
    ax.legend(fontsize=9, ncols=len(tabla.columns), loc="lower left",
              bbox_to_anchor=(0, 1.0))
    ax.spines["bottom"].set_color(REJILLA)
    guardar(fig, nombre)


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("auxiliar", help="Libro auxiliar en CSV")
    args = ap.parse_args()

    aux = pd.read_csv(args.auxiliar, dtype={"codigo_puc": str})
    aux["fecha"] = pd.to_datetime(aux["fecha"])
    aux["mes"] = aux["fecha"].dt.to_period("M")

    print("Graficos generados:")

    ventas = aux[aux.codigo_puc.str.startswith("41")].groupby("mes")["credito"].sum()
    grafico_barras_mes(ventas, "Ventas por mes", "01_ventas_por_mes.png")

    gastos = (aux[aux.codigo_puc.str.startswith(("5", "6"))]
              .groupby("nombre_cuenta")["debito"].sum().nlargest(8))
    grafico_barras_h(gastos, "Principales costos y gastos del periodo", "02_top_gastos.png")

    comp = pd.DataFrame({
        "Ingresos": aux[aux.codigo_puc.str.startswith("41")].groupby("mes")["credito"].sum(),
        "Costos": aux[aux.codigo_puc.str.startswith("6")].groupby("mes")["debito"].sum(),
    }).fillna(0)
    grafico_lineas(comp, "Ingresos frente a costos", "03_ingresos_vs_costos.png")

    tabla = (aux[aux.codigo_puc.str.startswith(("5", "6"))]
             .pivot_table(index="mes", columns="centro_costo", values="debito",
                          aggfunc="sum").fillna(0))
    grafico_apilado(tabla, "Costos y gastos por centro de costo", "04_composicion_gasto.png")
