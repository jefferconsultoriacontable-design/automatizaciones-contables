const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType, PageBreak, Header, Footer,
  PageNumber, VerticalAlign, TabStopType
} = require("docx");
const fs = require("fs");

// ---------- Theme ----------
const NAVY = "1F3864";
const RED_DARK = "7A1F1F";
const RED_LIGHT = "F6E1E1";
const NAVY_LIGHT = "D9E2F3";
const GRAY_LIGHT = "F2F2F2";
const TEXT = "1A1A1A";
const FONT = "Calibri";

const PAGE_WIDTH = 12240; // Letter (Carta)
const PAGE_HEIGHT = 15840;
const MARGIN = 1080; // 0.75"
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN * 2; // 10080

// ---------- Helpers ----------
function cellBorders() {
  const line = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
  return { top: line, bottom: line, left: line, right: line };
}

function headerCell(text, width, fill = NAVY) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill, color: "auto" },
    verticalAlign: VerticalAlign.CENTER,
    borders: cellBorders(),
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    children: [new Paragraph({
      children: [new TextRun({ text, bold: true, color: "FFFFFF", font: FONT, size: 18 })]
    })]
  });
}

function bodyCell(text, width, opts = {}) {
  const { bold = false, shade = null, align = AlignmentType.LEFT, italics = false, color = TEXT, size = 18 } = opts;
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, fill: shade, color: "auto" } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    borders: cellBorders(),
    margins: { top: 80, bottom: 80, left: 110, right: 110 },
    children: [new Paragraph({
      alignment: align,
      children: [new TextRun({ text, bold, italics, font: FONT, size, color })]
    })]
  });
}

function sectionHeading(text, num) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 160 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 4 } },
    children: [new TextRun({ text: `${num}. ${text}`, bold: true, color: NAVY, font: FONT, size: 26 })]
  });
}

function subHeading(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 220, after: 100 },
    children: [new TextRun({ text, bold: true, color: NAVY, font: FONT, size: 21 })]
  });
}

function bodyText(text, opts = {}) {
  const { italics = false, spacing = { before: 0, after: 140 }, bold = false } = opts;
  return new Paragraph({
    spacing,
    alignment: AlignmentType.JUSTIFIED,
    children: [new TextRun({ text, italics, bold, font: FONT, size: 20, color: TEXT })]
  });
}

function bullet(runs, opts = {}) {
  const children = typeof runs === "string"
    ? [new TextRun({ text: runs, font: FONT, size: 20, color: TEXT })]
    : runs;
  return new Paragraph({
    spacing: { after: 120 },
    bullet: { level: 0 },
    alignment: AlignmentType.JUSTIFIED,
    children
  });
}

function boldRun(text) { return new TextRun({ text, bold: true, font: FONT, size: 20, color: NAVY }); }
function normRun(text) { return new TextRun({ text, font: FONT, size: 20, color: TEXT }); }

function fieldLine(label, value) {
  return new Paragraph({
    spacing: { after: 90 },
    tabStops: [{ type: TabStopType.LEFT, position: 2600 }],
    children: [
      new TextRun({ text: `${label}:`, bold: true, font: FONT, size: 20, color: NAVY }),
      new TextRun({ text: "\t" }),
      new TextRun({ text: value, font: FONT, size: 20, color: TEXT })
    ]
  });
}

function alertBox(text) {
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    rows: [new TableRow({ children: [new TableCell({
      width: { size: CONTENT_WIDTH, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: RED_LIGHT, color: "auto" },
      borders: { top: { style: BorderStyle.SINGLE, size: 12, color: RED_DARK }, bottom: { style: BorderStyle.SINGLE, size: 12, color: RED_DARK }, left: { style: BorderStyle.SINGLE, size: 12, color: RED_DARK }, right: { style: BorderStyle.SINGLE, size: 12, color: RED_DARK } },
      margins: { top: 140, bottom: 140, left: 180, right: 180 },
      children: [new Paragraph({
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({ text, bold: true, font: FONT, size: 20, color: RED_DARK })]
      })]
    })]})]
  });
}

// ---------- Cover ----------
const cover = [
  new Paragraph({ spacing: { before: 500, after: 0 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 200, after: 40 },
    children: [new TextRun({ text: "COMPANY SERVICE FOOD SAS", bold: true, font: FONT, size: 30, color: NAVY })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 500 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: NAVY, space: 8 } },
    children: [new TextRun({ text: "NIT 900.148.334-6", font: FONT, size: 20, color: "595959" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 400, after: 100 },
    children: [new TextRun({ text: "INFORME DE HALLAZGOS DE EMPALME Y", bold: true, font: FONT, size: 32, color: NAVY })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 100 },
    children: [new TextRun({ text: "AUDITORÍA CONTABLE Y TRIBUTARIA PRELIMINAR", bold: true, font: FONT, size: 32, color: NAVY })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 700 },
    children: [new TextRun({ text: "Análisis del Balance de Prueba General — Enero a Junio de 2026", font: FONT, size: 22, color: "595959", italics: true })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 500 },
    children: [new TextRun({ text: "CONFIDENCIAL — USO INTERNO / COMITÉ GERENCIAL", bold: true, font: FONT, size: 18, color: RED_DARK })]
  }),
  fieldLine("Elaborado por", "Jeffer Daniel Pacheco — Contador Público, Contador Externo"),
  fieldLine("Marco técnico", "NIIF para Pymes / Estatuto Tributario Nacional (DIAN)"),
  fieldLine("Fecha de corte analizado", "30 de junio de 2026"),
  fieldLine("Fecha de emisión", "2 de septiembre de 2026"),
  fieldLine("Destinatario", "Comité Gerencial de COMPANY SERVICE FOOD SAS"),
  new Paragraph({ spacing: { before: 700, after: 0 }, children: [] }),
  alertBox("Este documento contiene un diagnóstico preliminar de empalme. No constituye una opinión de auditoría bajo Normas Internacionales de Auditoría (NIA); su propósito es identificar riesgos materiales que ameritan verificación documental adicional antes de la aceptación formal de los saldos por parte del contador entrante."),
  new Paragraph({ children: [new PageBreak()] })
];

// ---------- 1. Dictamen Preliminar ----------
const dictamen = [
  sectionHeading("Dictamen Preliminar del Empalme", 1),
  bodyText("En desarrollo del contrato de prestación de servicios profesionales suscrito con COMPANY SERVICE FOOD SAS, el suscrito Contador Público recibió del contador saliente el balance de prueba general correspondiente al periodo enero-junio de 2026, como base para el proceso de empalme y aceptación de los saldos contables."),
  subHeading("1.1 Calidad formal de la información recibida"),
  bodyText("Desde el punto de vista aritmético, el balance de prueba se encuentra cuadrado: el total de movimientos débito es igual al total de movimientos crédito ($53.257.171.557) y la ecuación patrimonial (Activo = Pasivo + Patrimonio + Resultado del ejercicio) se verifica de forma exacta a la fecha de corte. Sin embargo, el cuadre aritmético únicamente certifica la partida doble; no certifica la razonabilidad, la existencia real de los saldos, ni el cumplimiento normativo de las cifras, tal como se desarrolla en la Sección 2 de este informe."),
  subHeading("1.2 Riesgos legales de aceptación sin salvedades"),
  bodyText("El suscrito advierte que la aceptación pura y simple de los saldos heredados, sin dejar constancia expresa de las inconsistencias detectadas, expondría su responsabilidad profesional personal frente a terceros y ante la DIAN por hechos anteriores a su vinculación. En consecuencia, se recomienda a Gerencia:"),
  bullet([normRun("Suscribir el "), boldRun("Acta de Recepción de Empalme \"con salvedades expresas\""), normRun(", relacionando cada hallazgo de la Sección 2, en concordancia con los deberes de diligencia profesional del Contador Público (Ley 43 de 1990, art. 37).")]),
  bullet([normRun("Dejar constancia escrita de que la "), boldRun("responsabilidad del contador entrante inicia en la fecha de corte del empalme"), normRun(" hacia adelante, sin perjuicio de la obligación de reportar, corregir y regularizar hacia el futuro las partidas heredadas identificadas como críticas.")]),
  bullet([normRun("Requerir la firma conjunta del contador saliente en el acta, como respaldo documental de la entrega de la información y de los soportes físicos y magnéticos correspondientes.")]),
  subHeading("1.3 Conclusión preliminar"),
  bodyText("El nivel de riesgo identificado en el balance de prueba —particularmente el manejo de efectivo, los saldos con partes relacionadas y la ausencia de depreciación— justifica catalogar este empalme como de \"alta complejidad\" y sustenta ante Gerencia la necesidad de una consultoría de saneamiento contable y de controles internos adicional al alcance ordinario de la contabilidad mensual.", { spacing: { after: 60 } }),
];

// ---------- 2. Matriz de Anomalías ----------
function matrizTable() {
  const w1 = 2150, w2 = 2680, w3 = 2600, w4 = 2650;
  const rows = [
    ["1105 — Caja General\n-$547.206.895",
     "Saldo negativo en efectivo: contable e imposible físicamente. Los créditos (egresos, $2.237,1M) superaron los débitos (ingresos, $1.689,9M) en el semestre.",
     "Viola la esencia económica del activo \"efectivo\" (Marco Conceptual NIIF, párr. 4.4). Indica egresos registrados sin el correspondiente ingreso de caja soportado, o caja auxiliar no oficializada.",
     "Riesgo de apropiación indebida de recursos; base para el rechazo de costos y gastos sin soporte idóneo ante la DIAN (Art. 771-2 E.T.)."],
    ["1325 — CxC Socios y Accionistas\n$1.699.371.815",
     "Préstamo vigente a socio(s), con abonos mínimos en el semestre ($46,2M) y sin causación de ningún rendimiento financiero.",
     "Incumple NIIF Sección 33 \"Partes Relacionadas\" (revelación) y el reconocimiento del rendimiento financiero implícito en préstamos entre partes relacionadas.",
     "Renta presuntiva por préstamos a socios (Art. 35 E.T.): la DIAN puede adicionar intereses presuntos como ingreso gravable; riesgo de recalificación como distribución encubierta de utilidades."],
    ["Grupo 15 — Propiedad, Planta y Equipo\n$3.953.737.800 (bruto)",
     "No existe ninguna subcuenta de depreciación acumulada (159X) ni gasto de depreciación registrado en el periodo, pese a tratarse de activos productivos en uso.",
     "Incumple NIIF Sección 17 (depreciación sistemática obligatoria). Activo y utilidad del periodo sobreestimados.",
     "Pérdida de la deducción fiscal por depreciación (Art. 128 y 137 E.T.) del año gravable; riesgo de rechazo si se registra extemporáneamente sin metodología técnica soportada."],
    ["2335 y 2380 — Cuentas por Pagar\nSaldo débito: $15,0M y $8,9M",
     "Dos cuentas de naturaleza crédito (pasivo con terceros) cierran el semestre con saldo deudor, lo que indica pagos en exceso o partidas sin conciliar.",
     "Viola la naturaleza contable del pasivo; evidencia de conciliaciones de proveedores y acreedores no realizadas de forma periódica.",
     "Riesgo de pagos duplicados o a terceros no plenamente identificados; posible salida de recursos sin control, correlacionada con el faltante de caja."],
    ["Grupo 14 — Inventarios\n$2.536.794.257",
     "Saldo inicial = saldo final; movimiento de solo $96.000 en 6 meses, pese a $6.977,7M de costos de producción causados en el mismo periodo.",
     "Incompatible con NIIF Sección 13: el inventario debe rotar con el costo de ventas. Indica ausencia de kárdex / inventario permanente real.",
     "Costo de ventas no confiable para efectos de renta líquida gravable; riesgo de determinación errónea del costo fiscal (Art. 62 a 69 E.T.)."],
    ["1330 y 1345 — Anticipos y Cartera de Consorcios\n$2.435.455.522 y $2.328.424.147",
     "Saldos represados de alto valor sin evidencia de depuración o rotación normal a la fecha de corte.",
     "Incumple NIIF Sección 11 (evaluación periódica de deterioro de valor, no evidenciada en el periodo).",
     "Riesgo de cartera de difícil cobro no provisionada, y de anticipos que en la práctica corresponden a gastos ya causados pendientes de legalizar."],
    ["5195 — Gastos Diversos (Admón.)\n$1.239.904.766 (57% del gasto de administración)",
     "Una sola subcuenta \"cajón de sastre\" concentra más de la mitad del gasto administrativo total ($2.175,9M) del semestre.",
     "Incumple el principio de representación fiel y desagregación de partidas (NIIF Sección 3); impide la trazabilidad real del gasto.",
     "Alto riesgo de gastos no deducibles por falta de soporte idóneo y relación de causalidad (Art. 107 y 771-2 E.T.) ante una eventual fiscalización."],
    ["2404 — Impuesto de Renta Corriente\nSaldo débito: $348.054.000",
     "Cuenta de pasivo por impuesto de renta corriente cierra con saldo deudor, naturaleza contraria a la que le corresponde.",
     "Posible confusión entre \"anticipo de renta\" (cuenta 1355) y \"pasivo por renta corriente\" (cuenta 2404); indicio de doble registro o clasificación cruzada.",
     "Riesgo de error en la determinación del saldo real a pagar o a favor frente a la DIAN en la próxima declaración de renta."],
    ["Resultado Operacional del Semestre\n-$520.548.532 (pérdida)",
     "Pese a un margen bruto positivo del 23,6% ($2.157,7M sobre ingresos de $9.135,4M), los gastos operativos ($2.678,3M) absorben la utilidad bruta y generan pérdida operacional.",
     "Exige la evaluación de indicios de deterioro de activos y de la hipótesis de negocio en marcha (NIIF Sección 3.9 y Sección 27).",
     "Combinado con la caja negativa, constituye una señal de alerta de continuidad del negocio (going concern) de escalamiento inmediato a Gerencia."],
  ];
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [w1, w2, w3, w4],
    rows: [
      new TableRow({ tableHeader: true, children: [
        headerCell("Cuenta / Saldo", w1), headerCell("Hallazgo", w2),
        headerCell("Riesgo Contable (NIIF)", w3), headerCell("Riesgo Fiscal / Financiero", w4)
      ]}),
      ...rows.map((r, i) => new TableRow({ children: [
        bodyCell(r[0], w1, { bold: true, shade: i % 2 ? GRAY_LIGHT : null }),
        bodyCell(r[1], w2, { shade: i % 2 ? GRAY_LIGHT : null }),
        bodyCell(r[2], w3, { shade: i % 2 ? GRAY_LIGHT : null }),
        bodyCell(r[3], w4, { shade: i % 2 ? GRAY_LIGHT : null })
      ]}))
    ]
  });
}

const matriz = [
  sectionHeading("Matriz de Anomalías Críticas Detectadas", 2),
  bodyText("La siguiente matriz resume los nueve hallazgos de mayor materialidad identificados a partir del balance de prueba, ordenados según su aparición en el catálogo de cuentas. Cada hallazgo se soporta directamente en las cifras del corte enero-junio de 2026 y debe verificarse contra la documentación soporte antes de la aceptación definitiva del empalme.", { spacing: { after: 160 } }),
  matrizTable(),
];

// ---------- 3. Puntos de Impacto para Gerencia ----------
const impacto = [
  sectionHeading("Puntos de Impacto para la Gerencia", 3),
  bodyText("Los siguientes hallazgos deben revelarse de inmediato al comité gerencial, tanto para deslindar la responsabilidad profesional del contador entrante frente a hechos anteriores a su vinculación, como para justificar el alcance y el costo de la consultoría de saneamiento propuesta."),
  bullet([boldRun("Riesgo de continuidad del negocio: "), normRun("la pérdida operacional de $520.548.532 en el semestre, combinada con el saldo negativo de $547.206.895 en la cuenta de Caja (1105), configura una señal de alerta de liquidez que debe escalarse de inmediato a la Junta o al comité gerencial.")]),
  bullet([boldRun("Exposición fiscal por préstamos a socios: "), normRun("los $1.699.371.815 prestados a socios sin causación de rendimientos financieros exponen a la compañía a un mayor impuesto de renta por la vía de la renta presuntiva de intereses (Art. 35 E.T.), y podrían interpretarse como distribución indirecta de utilidades ante una fiscalización.")]),
  bullet([boldRun("Deducciones fiscales no aprovechadas: "), normRun("la ausencia de depreciación acumulada sobre $3.953.737.800 en activos fijos representa una deducción fiscal perdida (Art. 128 E.T.) y una sobreestimación simultánea del patrimonio y de la utilidad reportada a los socios.")]),
  bullet([boldRun("Necesidad de deslinde formal de responsabilidad: "), normRun("los hallazgos descritos son anteriores a la fecha de posesión del suscrito; se requiere el Acta de Empalme con salvedades, firmada por Gerencia y por el contador saliente, antes de asumir el control operativo pleno de los libros.")]),
  bullet([boldRun("Autorización requerida para actuar: "), normRun("se solicita a Gerencia autorización formal y por escrito para ejecutar arqueos sorpresivos, circularizar a terceros (clientes, socios, proveedores) y aplicar controles temporales de doble firma sobre los desembolsos de caja, mientras se sanean los controles internos.")]),
];

// ---------- 4. Plan de Acción ----------
const plan = [
  sectionHeading("Plan de Acción y Primeros Pasos", 4),
  bodyText("Acciones a iniciar de forma inmediata, sin previo aviso a los responsables operativos de caja y tesorería, con el fin de preservar la evidencia:"),
  bullet([boldRun("Arqueo de caja sorpresivo "), normRun("e inventario físico de fondos fijos y caja menor, con acta firmada por el responsable de caja, un testigo y el contador entrante.")]),
  bullet([boldRun("Conciliaciones bancarias "), normRun("de las tres cuentas activas (Davivienda Aho. 4084, Banco Falabella 5396 y Banco Falabella 5385) con corte al 30 de junio de 2026, identificando partidas conciliatorias pendientes.")]),
  bullet([boldRun("Solicitud formal de soportes documentales "), normRun("(facturas, recibos, comprobantes de egreso) del 100% de los movimientos de la cuenta 5195 \"Gastos Diversos\" superiores a un umbral de materialidad sugerido de $5.000.000 por transacción.")]),
  bullet([boldRun("Circularización (confirmación de saldos) "), normRun("a: (i) el o los socios deudores de la cuenta 1325; (ii) los principales clientes y consorcios/uniones temporales de la cuenta 1345; y (iii) los proveedores y contratistas con anticipos pendientes en la cuenta 1330.")]),
  bullet([boldRun("Recálculo técnico de la depreciación "), normRun("acumulada de los activos fijos desde su fecha de adquisición, y registro del ajuste contable correspondiente bajo NIIF Sección 17.")]),
  bullet([boldRun("Recálculo del rendimiento financiero presuntivo "), normRun("(Art. 35 E.T.) sobre el saldo del préstamo a socios, para determinar el eventual mayor ingreso gravable del periodo.")]),
  bullet([boldRun("Depuración de las cuentas 2335 y 2380 "), normRun("(cuentas por pagar con saldo débito), identificando partida por partida el origen del pago en exceso o la reclasificación pendiente.")]),
];

// ---------- 5. Calendario de Trabajo ----------
function calendarioTable() {
  const w1 = 1400, w2 = 4180, w3 = 2200, w4 = 2300;
  const rows = [
    ["Semana 1\nDiagnóstico y control inmediato",
     "Arqueo sorpresivo de caja y fondos; conciliación bancaria de las 3 cuentas activas (corte 30-jun); solicitud de soportes del 100% de la cuenta 5195 > $5.000.000; control temporal de doble firma sobre desembolsos de caja menor.",
     "Contador Externo y Auxiliar Contable",
     "Acta de arqueo, conciliaciones bancarias firmadas, listado de partidas sin soporte de 5195."],
    ["Semana 2\nConfirmaciones y circularización",
     "Envío de cartas de confirmación de saldos al/los socio(s) deudor(es) (1325), a los principales clientes/consorcios (1345) y a proveedores con anticipos (1330); conteo físico selectivo de inventarios.",
     "Contador Externo, con visto bueno de Gerencia",
     "Cartas de circularización enviadas y respondidas; acta de conteo físico de inventarios."],
    ["Semana 3\nAnálisis técnico y cálculos",
     "Cálculo retroactivo de depreciación NIIF/fiscal de PP&E; cálculo del rendimiento presuntivo Art. 35 E.T. sobre el préstamo a socios; análisis de antigüedad de saldos (aging) de cartera y anticipos; depuración de 2335 y 2380.",
     "Contador Externo",
     "Papel de trabajo de depreciación, cálculo de interés presuntivo, informe de aging de cartera y anticipos."],
    ["Semana 4\nConsolidación y entrega",
     "Preparación de los asientos de ajuste y reclasificación propuestos; redacción del Informe Final de Empalme con salvedades; suscripción del Acta de Recepción; presentación de hallazgos y plan de remediación al comité gerencial.",
     "Contador Externo y Gerencia",
     "Informe final de empalme, Acta de Recepción con salvedades, plan de remediación aprobado por Gerencia."],
  ];
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [w1, w2, w3, w4],
    rows: [
      new TableRow({ tableHeader: true, children: [
        headerCell("Semana", w1), headerCell("Actividades Clave", w2),
        headerCell("Responsable", w3), headerCell("Entregable", w4)
      ]}),
      ...rows.map((r, i) => new TableRow({ children: [
        bodyCell(r[0], w1, { bold: true, shade: i % 2 ? GRAY_LIGHT : null }),
        bodyCell(r[1], w2, { shade: i % 2 ? GRAY_LIGHT : null }),
        bodyCell(r[2], w3, { shade: i % 2 ? GRAY_LIGHT : null, align: AlignmentType.CENTER }),
        bodyCell(r[3], w4, { shade: i % 2 ? GRAY_LIGHT : null })
      ]}))
    ]
  });
}

const calendario = [
  sectionHeading("Calendario de Trabajo — Cronograma de 4 Semanas", 5),
  bodyText("Cronograma propuesto para la ejecución del contrato de consultoría de saneamiento contable, a partir de la fecha de aprobación de este informe por parte de Gerencia.", { spacing: { after: 160 } }),
  calendarioTable(),
  new Paragraph({ spacing: { before: 400, after: 40 }, children: [
    new TextRun({ text: "_____________________________________", font: FONT, size: 20 })
  ]}),
  new Paragraph({ spacing: { after: 10 }, children: [
    new TextRun({ text: "Jeffer Daniel Pacheco", bold: true, font: FONT, size: 20, color: TEXT })
  ]}),
  new Paragraph({ spacing: { after: 10 }, children: [
    new TextRun({ text: "Contador Público — Contador Externo", font: FONT, size: 19, color: "595959" })
  ]}),
  new Paragraph({ children: [
    new TextRun({ text: "Fecha: 2 de septiembre de 2026", italics: true, font: FONT, size: 19, color: "808080" })
  ]}),
];

// ---------- Header / Footer ----------
const header = new Header({
  children: [
    new Paragraph({
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_WIDTH }],
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF", space: 4 } },
      children: [
        new TextRun({ text: "COMPANY SERVICE FOOD SAS", font: FONT, size: 16, color: NAVY, bold: true }),
        new TextRun({ text: "\tInforme de Hallazgos de Empalme — Confidencial", font: FONT, size: 16, color: "808080", italics: true })
      ]
    })
  ]
});

const footer = new Footer({
  children: [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ text: "Página ", font: FONT, size: 16, color: "808080" }),
        new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: "808080" }),
        new TextRun({ text: " de ", font: FONT, size: 16, color: "808080" }),
        new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 16, color: "808080" })
      ]
    })
  ]
});

// ---------- Document ----------
const doc = new Document({
  creator: "Jeffer Daniel Pacheco",
  title: "Informe de Hallazgos de Empalme y Auditoría Preliminar - COMPANY SERVICE FOOD SAS",
  styles: {
    default: {
      document: { run: { font: FONT, size: 20, color: TEXT } }
    }
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
          margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN }
        }
      },
      children: cover
    },
    {
      properties: {
        page: {
          size: { width: PAGE_WIDTH, height: PAGE_HEIGHT },
          margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN }
        }
      },
      headers: { default: header },
      footers: { default: footer },
      children: [
        ...dictamen,
        ...matriz,
        ...impacto,
        ...plan,
        ...calendario
      ]
    }
  ]
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync("/home/claude/Informe_Hallazgos_Empalme_COMPANY_SERVICE_FOOD.docx", buffer);
  console.log("done");
});

