# Marca personal: plan de contenido y portafolio

## La tesis

Hay muchos contadores y hay muchos programadores. Contadores colombianos que automatizan
su propio trabajo y lo explican en público hay muy pocos. Ese cruce es tu posicionamiento;
todo lo que publiques debería reforzarlo.

## Qué publicar (y qué no)

| Funciona | No funciona |
|---|---|
| Un problema real que resolviste, con el antes y el después en tiempo | Frases motivacionales sobre productividad |
| El error que cometiste y cómo lo detectaste | Publicar solo logros |
| Una herramienta que otro contador pueda usar hoy | Anunciar proyectos que aún no existen |
| Explicar una norma con un caso numérico | Copiar el texto de la norma |
| Capturas del resultado, no del código | Muros de código sin contexto |

Nunca publiques datos de tu empleador ni de clientes: cifras, nombres, NIT, capturas de su
software. Todo ejemplo va con datos simulados. Es criterio profesional y, además, es lo que
te permite publicar sin pedir permiso.

## Estructura de un post que funciona

```
1. El problema, en una línea concreta y con número
   "Conciliar 149 movimientos bancarios me tomaba 3 horas cada mes."

2. Qué hiciste, sin jerga
   "Escribí un script que cruza el extracto contra el auxiliar en dos pasadas."

3. El resultado, medible
   "Ahora son 40 segundos, y las partidas conciliatorias salen clasificadas."

4. Lo que aprendiste — esta es la parte que la gente guarda
   "El cruce por referencia solo resuelve el 70%. Lo demás sale al cruzar por valor
    con tolerancia de fecha: ahí aparecen las partidas en tránsito."

5. Una pregunta abierta
   "¿Cómo manejas tú las partidas en tránsito del cierre?"
```

Sin hashtags de relleno (tres bastan), sin emojis en cada línea, sin "sígueme para más".

## Calendario sostenible

Una publicación por semana, cuatro semanas por ciclo:

| Semana | Tipo | Ejemplo con lo que ya tienes |
|---|---|---|
| 1 | Herramienta | Calculadora de retenciones con UVT 2026 parametrizada |
| 2 | Aprendizaje técnico | Por qué los códigos PUC se leen como texto y no como número |
| 3 | Caso normativo | Cartera sin deterioro: qué dice NIIF 9 y cómo se calcula |
| 4 | Reflexión de oficio | Qué cambia en el trabajo del contador cuando automatiza el cierre |

Cuatro publicaciones al mes durante seis meses te dan 24 piezas: eso ya es un cuerpo de
trabajo que habla por ti en una entrevista o ante un cliente.

## Portafolio

Estructura mínima de cada proyecto publicado, sea en GitHub o en tu sitio:

```
nombre-del-proyecto/
├── README.md          <- problema, solución, cómo se ejecuta, captura del resultado
├── datos_ejemplo/     <- datos simulados, nunca reales
├── src/               <- el código
└── salidas/           <- un ejemplo del resultado
```

El README es el proyecto para quien lo visita: si en 30 segundos no entiende qué problema
resuelve y cómo se ejecuta, el código no existe. Empieza siempre por el problema, no por
la tecnología.

## Orden de publicación sugerido

1. **Kit de pandas para contadores** — es material didáctico, se comparte solo y no expone nada.
2. **Calculadora de retenciones** — utilidad inmediata para cualquier colega.
3. **Conciliación bancaria automatizada** — es el que más impresiona, porque todos sufren esa tarea.
4. **Analizador de balance con alertas NIIF** — el que mejor demuestra criterio profesional, no solo código.

## Medida de éxito

No son los seguidores. Son: cuántos colegas usan algo tuyo, cuántas conversaciones de
trabajo o consultoría empiezan porque alguien leyó una publicación, y cuánto tiempo te
ahorras tú mismo con lo que construyes. Los tres se pueden contar.
