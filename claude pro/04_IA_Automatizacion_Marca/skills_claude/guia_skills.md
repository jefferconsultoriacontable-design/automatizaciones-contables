# Skills de Claude: qué son y cómo hacerte una

Un **prompt** lo escribes cada vez. Un **skill** es un instructivo guardado que Claude carga
solo cuando la conversación lo amerita. La diferencia práctica: dejas de repetir tus reglas
de trabajo en cada chat, y todas tus respuestas salen con el mismo criterio.

## Cuándo vale la pena convertir un prompt en skill

Cuando se cumplen las tres:

1. Es un procedimiento de varios pasos, no una pregunta suelta.
2. Lo repites — mínimo una vez al mes.
3. Tienes un criterio propio sobre cómo debe hacerse (tu formato, tus validaciones, tu marco normativo).

Análisis de balance, revisión de cierre, cálculo de retenciones y redacción de políticas
contables califican. "¿Qué dice el artículo 383?" no: eso es una pregunta.

## Anatomía de un skill

```
mi-skill/
├── SKILL.md              <- lo único obligatorio
└── referencias/          <- opcional: tablas, formatos, ejemplos
    └── tarifas.md
```

El `SKILL.md` tiene dos partes:

```markdown
---
name: analisis-balance-niif
description: Analiza un balance de prueba colombiano bajo NIIF. Úsalo cuando el
  usuario adjunte un balance, un auxiliar o pregunte por ajustes, indicadores o
  hallazgos de cierre.
---

# Instrucciones (el cuerpo)
...
```

**La `description` decide si el skill se activa o no.** Es la parte que más se subestima:
escribe *cuándo* usarlo, con las palabras que tú realmente usas al pedirlo, no un resumen
elegante de lo que hace.

## Reglas para escribir el cuerpo

| Sí | No |
|---|---|
| Pasos numerados en orden de ejecución | Párrafos de contexto general |
| Formato de salida explícito (tablas, secciones) | "Responde de forma profesional" |
| Qué validar antes de entregar | Suponer que la validación se hace sola |
| Qué hacer cuando falten datos | Dejar que invente supuestos en silencio |
| Ejemplos concretos de entrada y salida | Descripciones abstractas |

Un skill largo no es mejor. Si pasa de dos páginas, casi siempre es que mezcla dos
procedimientos: sepáralos.

## Cómo crear el tuyo

Pídeselo a Claude directamente: *"conviértelo en un skill"* después de haber hecho el
trabajo bien una vez en el chat. Es el mejor momento, porque ya existe el ejemplo real de
la salida que quieres. Claude te muestra una tarjeta para revisar y guardar.

Después, cada vez que uses el skill y algo salga distinto a lo que esperabas, pide que se
actualice. Un skill que no cambia en seis meses o está perfecto o no lo estás usando.

## Ejemplo listo

En esta misma carpeta está `SKILL_ejemplo_analisis_balance.md`: un skill completo de
análisis de balance de prueba bajo NIIF, con el formato de salida y las validaciones que
usarías en un cierre real. Léelo como modelo de estructura, no para copiarlo tal cual —
su valor está en que refleje *tu* criterio profesional.

## Skills vs. artifacts vs. proyectos en Python

- **Skill** — cómo debe trabajar Claude. Se activa solo, no produce archivos por sí mismo.
- **Artifact** — una página o herramienta publicada con su enlace, que abres y compartes.
- **Proyecto en Python** — el cálculo corre en tu equipo, con tus archivos, sin depender de un chat.

Los tres se combinan: el skill define el criterio, el proyecto en Python hace el cálculo
pesado y reproducible, y el artifact es lo que le muestras al cliente o a gerencia.
