# Claude Pro · Espacio de proyectos profesionales

Jeffer Daniel Pacheco Peña — Contador Público
Actualizado: septiembre de 2026

Cuatro secciones. Cada proyecto es autónomo: tiene sus datos de ejemplo, se ejecuta con un
comando y entrega un archivo listo para archivar como papel de trabajo.

---

## Mapa

```
claude pro/
├── 00_INDICE.md
├── 01_Tributaria_y_Retenciones/
│   ├── calculadora_retenciones/      retefuente, reteIVA, reteICA y autorretención · UVT 2026
│   └── exogena_formato_1001/         formato 1001 desde el libro auxiliar
├── 02_Contabilidad_y_NIIF/
│   ├── conciliacion_bancaria/        cruce en dos pasadas + prueba de saldos
│   ├── analisis_balance_prueba/      validaciones, indicadores y alertas NIIF
│   ├── informe_mensual_gerencia/     informe en Word con hallazgos automáticos
│   └── empalme_contable/             checklist de 67 ítems + acta de entrega
├── 03_Data_Science_Python/
│   ├── 01_kit_pandas_contable/       15 ejercicios con datos contables + soluciones
│   ├── 02_plantillas/                plantilla de análisis y plantilla de gráficos
│   └── 03_ruta_aprendizaje.md        las cinco etapas, con entrega por etapa
└── 04_IA_Automatizacion_Marca/
    ├── biblioteca_prompts/           10 prompts contables
    ├── skills_claude/                guía + skill de ejemplo
    └── marca_personal/               plan de contenido y portafolio
```

---

## Instalación (una sola vez)

Abre una terminal en VS Code (``Ctrl + ` ``) y ejecuta:

```bash
pip install pandas openpyxl python-docx matplotlib jupyter
```

Después, en VS Code: **Archivo → Abrir carpeta →** `claude pro`. Abrir la carpeta y no el
archivo suelto es lo que hace que las rutas relativas (`datos/...`) funcionen.

---

## Qué corre con qué comando

| Necesito | Comando |
|---|---|
| Calcular retenciones de un lote de facturas | `python procesar_lote.py facturas.csv` |
| Preparar el formato 1001 | `python generar_1001.py libro_auxiliar.csv --anio 2026` |
| Conciliar el banco | `python conciliar.py libros.csv extracto.csv --saldo-inicial 0` |
| Revisar un balance de prueba | `python analizar_balance.py balance.csv` |
| Armar el informe a gerencia | `python generar_informe.py balance.csv --mes "Marzo 2026"` |
| Generar el checklist de empalme | `python crear_checklist_empalme.py --empresa "..."` |
| Explorar un archivo nuevo | `python plantilla_analisis_contable.py archivo.xlsx` |
| Hacer los gráficos del informe | `python plantilla_graficos.py libro_auxiliar.csv` |
| Estudiar pandas | abrir `01_kit_pandas_contable/01_ejercicios.ipynb` |

Cada script escribe su resultado en una subcarpeta `salidas/` y **nunca modifica el archivo
de entrada**.

---

## Convenciones del espacio

- **Parámetros afuera del código.** Tarifas, UVT y conceptos viven en archivos `.json`. Cuando cambie la norma, editas el JSON y no tocas la lógica.
- **Códigos como texto.** PUC y NIT se leen con `dtype=str`: como número pierden los ceros a la izquierda y ningún cruce funciona.
- **Redondear antes de comparar.** Los flotantes arrastran error binario; toda comparación de totales va a dos decimales.
- **Datos simulados.** Ningún archivo de este espacio contiene información real de un empleador o cliente. Mantenlo así: es lo que te permite publicar y compartir sin pedir permiso.
- **Verificación profesional.** Estas herramientas aceleran el trabajo y no lo reemplazan. Antes de usar cualquier resultado en una declaración, un informe o un dictamen: valida tarifas vigentes, UVT del año y la aritmética de los totales.

---

## Datos de ejemplo

Todos los proyectos comparten los mismos datos simulados de **COMERCIALIZADORA ANDINA S.A.S.**
(enero–marzo 2026): libro auxiliar de 1.268 movimientos con partida doble exacta, balance de
prueba de 30 cuentas, 41 facturas de proveedores y un extracto bancario de 149 movimientos con
partidas en tránsito, GMF, comisiones y una nota débito. Están en
`03_Data_Science_Python/01_kit_pandas_contable/datos/` y se pueden regenerar con
`generar_datos.py`.

---

## Siguientes proyectos naturales

1. Retención en la fuente por rentas de trabajo (Art. 383 ET) con depuración de la base.
2. Cartera por edades con cálculo de deterioro esperado bajo NIIF 9.
3. Software de inventarios con causación de costos.
4. Tablero mensual en HTML que consolide indicadores, conciliación y estado tributario.
