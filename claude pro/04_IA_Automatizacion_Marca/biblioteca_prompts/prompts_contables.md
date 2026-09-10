# Biblioteca de prompts contables

Prompts probados para trabajo contable, tributario y financiero. Copia, reemplaza lo que
está `[entre corchetes]` y adjunta el archivo cuando aplique.

## Cómo está construido un buen prompt aquí

Los cuatro que rinden más, en orden de impacto:

1. **Rol específico** — "Contador Público Senior especialista en NIIF para PYMES" rinde más que "experto contable".
2. **Contexto normativo** — dile el marco (NIIF Plenas / PYMES, grupo 1-2-3), el país y el año.
3. **Formato de salida** — tabla, asiento débito/crédito, memorando, lista de verificación.
4. **Qué hacer con lo que falta** — "si faltan datos, explicita los supuestos en vez de inventar cifras".

Un prompt sin el punto 4 produce respuestas que parecen seguras y no lo son.

---

## 1 · Análisis de balance de prueba

```
Actúa como Contador Público Senior y auditor especialista en NIIF para PYMES.
Analiza el balance de prueba adjunto de una empresa colombiana del sector [sector],
correspondiente a [periodo].

Estructura tu respuesta así:
1. Diagnóstico ejecutivo (máximo 5 viñetas)
2. Análisis normativo: cita la NIC/NIIF o sección aplicable a cada hallazgo
3. Cifras y ajustes propuestos en tabla, con asientos débito/crédito
4. Notas técnicas: deterioro, pasivos contingentes, revelaciones e impacto fiscal

Verifica la ecuación contable (Activo = Pasivo + Patrimonio) antes de concluir.
Si faltan cifras, explicita los supuestos que tomaste; no inventes datos.
```

## 2 · Revisión de una operación antes de contabilizarla

```
Operación: [describe la operación, valor, partes y documentos soporte].
Marco: NIIF para PYMES, Colombia, año gravable [año].

Dime, en este orden:
1. Reconocimiento: qué se reconoce, cuándo y por qué valor
2. Medición inicial y posterior, con la sección aplicable
3. Asiento contable completo (cuenta PUC, débito, crédito)
4. Efecto tributario: IVA, retenciones aplicables, deducibilidad en renta
5. Revelaciones exigidas en notas
6. Los tres errores más frecuentes al registrar esta operación
```

## 3 · Cierre mensual: qué revisar antes de cerrar

```
Voy a cerrar el mes de [mes] de una empresa [sector, tamaño, grupo NIIF].
Dame una lista de verificación de cierre ordenada por riesgo, no por orden alfabético.
Para cada punto: qué revisar, contra qué documento se cruza, y cuál es la consecuencia
de no hacerlo (contable, tributaria o de auditoría).
Marca con [CRÍTICO] lo que no puede quedar pendiente.
```

## 4 · Conciliación de una diferencia

```
Tengo una diferencia de [valor] entre [fuente A] y [fuente B] en [cuenta o proceso].
Adjunto ambos archivos.

Antes de proponer un ajuste:
1. Lista las 8 causas más probables de esta diferencia, ordenadas por frecuencia real
2. Dime qué prueba concreta descarta cada causa
3. Solo cuando la causa esté identificada, propón el ajuste con su asiento

No propongas un ajuste "de cuadre" contra una cuenta puente.
```

## 5 · Explicar un resultado a gerencia

```
Convierte este análisis técnico en un memorando para gerencia general, que no es contable.
Máximo una página. Estructura: qué pasó, por qué pasó, qué significa en plata,
qué decisión hay que tomar y para cuándo.
Cero jerga contable sin traducir. Cada cifra en pesos, no en porcentajes solos.
```

## 6 · Redacción de política contable

```
Redacta la política contable de [tema: inventarios / PPE / deterioro de cartera / ingresos]
para una empresa colombiana del grupo [1 o 2], sector [sector].

Incluye: alcance, reconocimiento, medición inicial y posterior, bajas, estimaciones y
juicios significativos, revelaciones, y vigencia. Cita la sección o NIIF de cada apartado.
Al final, agrega las tres preguntas que la gerencia debe responder para que la política
quede definitivamente aprobada.
```

## 7 · Auditoría de un archivo de datos

```
Adjunto [archivo]. Antes de analizarlo, audítalo:
1. Filas, columnas, tipos de dato y nulos por columna
2. Duplicados exactos y duplicados por llave [llave]
3. Valores atípicos o imposibles (negativos donde no debe haber, fechas fuera de rango)
4. Sumas de control: [describe el total que debe cuadrar]
Reporta los hallazgos en tabla y dime si el archivo es utilizable tal como está.
```

## 8 · Preparación de respuesta a un requerimiento

```
Recibí un [requerimiento ordinario / emplazamiento / pliego de cargos] de la DIAN sobre
[tema], por [periodo]. Adjunto el documento.

Dame:
1. Qué está pidiendo exactamente, en lenguaje simple
2. El término legal para responder y desde cuándo cuenta
3. Los documentos que debo reunir, listados uno por uno
4. Un esquema de respuesta punto por punto
5. Los riesgos si la respuesta se presenta incompleta

Aclara qué parte de esto requiere concepto de un abogado tributarista.
```

## 9 · Cálculo con verificación obligatoria

```
Calcula [lo que necesites: retención, prestaciones, impuesto diferido].
Requisitos:
- Muestra la fórmula antes del número
- Muestra el cálculo paso a paso, no solo el resultado
- Cita la norma y la tarifa con su vigencia
- Al final, verifica el resultado por un método distinto y compara
Si los dos métodos no coinciden, dime dónde está la diferencia.
```

## 10 · Construir una herramienta en Python

```
Necesito un script en Python que [tarea], leyendo [formato de entrada] y produciendo
[formato de salida].

Condiciones:
- Las tarifas y parámetros van en un archivo JSON aparte, no dentro del código
- No modifica el archivo original: escribe uno nuevo
- Valida la entrada y avisa con un mensaje claro si falta una columna
- Comentarios en español explicando el porqué contable, no el qué del código
- Incluye un archivo de datos de ejemplo para probarlo

Explícame cómo ejecutarlo en VS Code paso a paso.
```

---

## Advertencia de uso

Ningún resultado de estos prompts se presenta ante la DIAN, una junta directiva o un
revisor fiscal sin que tú lo verifiques. La IA acelera el análisis y redacta bien;
la responsabilidad profesional y la firma siguen siendo tuyas. Verifica siempre:
tarifas vigentes, UVT del año, versión de la norma citada y aritmética de los totales.
