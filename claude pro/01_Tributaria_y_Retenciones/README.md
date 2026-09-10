# 01 · Tributaria y retenciones

Herramientas de cálculo y preparación tributaria colombiana. **UVT 2026: $52.374.**

> Las tarifas, bases mínimas y topes son parámetros en archivos `.json`, no están escritos
> dentro del código. Cuando cambie la norma o la UVT, editas el JSON y todo se recalcula.
> Antes de usar cualquier resultado en una declaración real, valídalo contra la norma vigente
> y contra el acuerdo municipal de ICA que aplique.

---

## calculadora_retenciones/

Motor de retefuente, reteIVA, reteICA y autorretención especial en renta.

| Archivo | Qué es |
|---|---|
| `retenciones.py` | El motor. Clase `Calculadora` con el método `calcular()` |
| `tarifas_2026.json` | UVT, 18 conceptos de retefuente con su base mínima, reteIVA, reteICA por actividad y autorretención |
| `procesar_lote.py` | Toma un CSV/Excel de facturas y calcula todo en bloque |
| `facturas_ejemplo.csv` | 12 facturas de prueba que cubren los casos difíciles |

**Uso individual:**

```python
from retenciones import Calculadora

c = Calculadora()
r = c.calcular(
    base_gravable=12_000_000,
    concepto="compras_generales_declarante",
    actividad_ica="comercio_al_por_mayor_y_menor",
)
print(r.resumen())
```

**Uso masivo:**

```bash
python procesar_lote.py facturas_ejemplo.csv
python procesar_lote.py "C:/ruta/facturas_marzo.xlsx" --salida salidas/marzo.xlsx
```

Genera un Excel con hojas *Detalle*, *Por proveedor* y *Por concepto*.

**Lo que ya tiene resuelto** (y suele fallar cuando se calcula a mano):

- No practica retención si la base no alcanza el mínimo en UVT del concepto — y lo dice en la observación.
- Cambia automáticamente a la tarifa de no declarante cuando marcas `declarante = NO`.
- Excluye a grandes contribuyentes y autorretenedores.
- Régimen Simple: no retefuente ni reteICA (Art. 911 ET), con la advertencia de validar el reteIVA caso a caso.
- Distingue la base mínima de reteIVA entre compras (27 UVT) y servicios (4 UVT).

Para ver todos los conceptos disponibles: `Calculadora().conceptos()`.

---

## exogena_formato_1001/

Prepara el formato 1001 (pagos o abonos en cuenta y retenciones practicadas) desde el libro auxiliar.

```bash
python generar_1001.py libro_auxiliar.csv --anio 2026
```

Clasifica cada cuenta PUC en su concepto 1001 según `conceptos_1001.json`, acumula por
tercero, cruza las retenciones de las cuentas 2365 / 2367 / 2368, agrupa lo que no supera
el tope en **cuantías menores (NIT 222222222)** y exporta tres hojas: *Formato 1001*,
*Control* y *Cuentas sin concepto*.

Esa última hoja es la más valiosa: te dice qué cuentas de gasto o costo quedaron sin
clasificar y, por lo tanto, sin reportar. Revísala siempre antes de presentar.

---

## Pendientes que puedes agregar

- Tabla de retención en la fuente por rentas de trabajo (Art. 383 ET) con depuración de la base.
- Calendario tributario del año con vencimientos por último dígito del NIT.
- Formatos 1003 (retenciones que le practicaron), 1005 (IVA descontable) y 1007 (ingresos).
