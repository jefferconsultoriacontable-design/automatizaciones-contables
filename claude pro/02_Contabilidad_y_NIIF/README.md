# 02 · Contabilidad y NIIF

Cuatro herramientas de cierre y control. Todas leen CSV o Excel y entregan un libro de
Excel (o Word) listo para archivar como papel de trabajo.

---

## conciliacion_bancaria/

```bash
python conciliar.py datos_ejemplo/libros_banco.csv datos_ejemplo/extracto.csv --saldo-inicial 185000000
```

Cruza en dos pasadas: primero por número de comprobante, y a lo que quede suelto le aplica
un **segundo cruce por valor con tolerancia de fecha** (`--dias 5`), que es como aparecen las
partidas en tránsito. Después clasifica lo no cruzado en solo-en-libros, solo-en-extracto y
diferencia de valor, y hace la prueba aritmética:

```
saldo extracto + partidas solo en libros − partidas solo en extracto = saldo en libros
```

Si el descuadre no da cero, el archivo te dice exactamente qué partidas lo explican.
Salida: hojas *Resumen*, *Partidas conciliatorias* y *Detalle del cruce*.

---

## analisis_balance_prueba/

```bash
python analizar_balance.py balance_prueba.csv
```

Tres bloques:

- **Validaciones aritméticas** — partida doble, coherencia de saldo inicial + movimientos = saldo final cuenta por cuenta, y ecuación contable.
- **Indicadores** — razón corriente, prueba ácida, capital de trabajo, endeudamiento, apalancamiento, márgenes, rotación y días de cartera e inventario.
- **Alertas técnicas** — con la norma citada: saldos contrarios a la naturaleza, cartera sin deterioro (NIIF 9 / Sección 11), inventario sin ajuste a VNR (NIC 2 / Sección 13), PPE sin depreciación del período (NIC 16 / Sección 17), cuentas puente sin depurar, ausencia de impuesto diferido (NIC 12 / Sección 29), provisiones (NIC 37) y beneficios a empleados (NIC 19).

Las reglas de alerta están escritas en la función `alertas()`: agrega las tuyas ahí, es la parte
que más valor gana cuando la ajustas a la empresa donde trabajas.

---

## informe_mensual_gerencia/

```bash
python generar_informe.py balance_prueba.csv --empresa "MI EMPRESA S.A.S." --nit 900123456 --mes "Marzo 2026"
python generar_informe.py marzo.csv --comparativo febrero.csv
```

Arma un Word de siete secciones: resumen ejecutivo, situación financiera (con variación contra
el mes anterior si pasas `--comparativo`), estado de resultados, indicadores con su lectura,
situación tributaria, hallazgos con recomendación, y compromisos del próximo cierre.

Los hallazgos no son texto fijo: se disparan según los datos (razón corriente bajo 1,
endeudamiento sobre 60 %, cartera sobre 60 días, resultado operacional negativo, falta de
deterioro o de depreciación, saldos a favor sin gestionar).

Requiere `pip install python-docx`.

---

## empalme_contable/

```bash
python crear_checklist_empalme.py --empresa "MI EMPRESA S.A.S." --entrega "Contador saliente" --recibe "Tu nombre"
```

Genera un Excel con **67 ítems en 10 áreas** (legal, estados financieros, conciliaciones,
depuración de saldos, tributaria, nómina, tesorería y activos, sistemas y accesos, procesos,
cierre), lista desplegable de estado, hoja de resumen con fórmulas vivas, matriz de 8 riesgos
típicos y un **modelo de acta de entrega y recibo** para firmar.

El punto del empalme no es recibir archivos: es dejar por escrito el estado real de la
contabilidad a la fecha de corte, para que las contingencias del período anterior no queden
a nombre de quien recibe. Por eso el acta incluye una sección de salvedades declaradas.
