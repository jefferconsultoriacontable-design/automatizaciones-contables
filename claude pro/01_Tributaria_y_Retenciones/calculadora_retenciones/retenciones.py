"""
Motor de calculo de retenciones en la fuente para Colombia.
Retefuente | ReteIVA | ReteICA | Autorretencion especial en renta

Uso rapido
----------
    from retenciones import Calculadora

    c = Calculadora()                       # carga tarifas_2026.json
    r = c.calcular(
        base_gravable=8_000_000,
        concepto="servicios_generales_declarante",
        proveedor_es_declarante=True,
        gran_contribuyente=False,
        actividad_ica="servicios_generales",
    )
    print(r.resumen())

Todas las tarifas y bases minimas viven en tarifas_2026.json: cuando cambie
la UVT o una tarifa, se edita el JSON, no el codigo.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

RUTA_TARIFAS = Path(__file__).with_name("tarifas_2026.json")


# --------------------------------------------------------------------------- #
#  Resultado
# --------------------------------------------------------------------------- #
@dataclass
class Resultado:
    base_gravable: float
    concepto: str
    descripcion_concepto: str
    iva: float = 0.0
    tarifa_retefuente: float = 0.0
    base_minima_retefuente: float = 0.0
    retefuente: float = 0.0
    tarifa_reteiva: float = 0.0
    reteiva: float = 0.0
    tarifa_reteica_por_mil: float = 0.0
    reteica: float = 0.0
    autorretencion_renta: float = 0.0
    total_retenciones: float = 0.0
    neto_a_pagar: float = 0.0
    observaciones: list[str] = field(default_factory=list)

    def resumen(self) -> str:
        L = [
            f"Concepto            : {self.descripcion_concepto}",
            f"Base gravable       : {self.base_gravable:>16,.2f}",
            f"IVA                 : {self.iva:>16,.2f}",
            f"(-) Retefuente {self.tarifa_retefuente*100:>5.2f}% : {self.retefuente:>16,.2f}",
            f"(-) ReteIVA    {self.tarifa_reteiva*100:>5.2f}% : {self.reteiva:>16,.2f}",
            f"(-) ReteICA  {self.tarifa_reteica_por_mil:>5.2f}x1000 : {self.reteica:>16,.2f}",
            f"(=) Neto a pagar    : {self.neto_a_pagar:>16,.2f}",
            f"Autorret. renta     : {self.autorretencion_renta:>16,.2f}  (no afecta el pago al proveedor)",
        ]
        if self.observaciones:
            L.append("Observaciones:")
            L += [f"  - {o}" for o in self.observaciones]
        return "\n".join(L)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["observaciones"] = " | ".join(self.observaciones)
        return d


# --------------------------------------------------------------------------- #
#  Calculadora
# --------------------------------------------------------------------------- #
class Calculadora:
    def __init__(self, ruta_tarifas: str | Path = RUTA_TARIFAS):
        with open(ruta_tarifas, encoding="utf-8") as f:
            self.t = json.load(f)
        self.uvt = self.t["uvt"]

    # ---------------------------------------------------------------- helpers
    def uvt_a_pesos(self, cantidad_uvt: float) -> float:
        return round(cantidad_uvt * self.uvt, 0)

    def conceptos(self) -> dict[str, str]:
        return {k: v["descripcion"] for k, v in self.t["retefuente"].items()}

    # ------------------------------------------------------------------ core
    def calcular(
        self,
        base_gravable: float,
        concepto: str = "compras_generales_declarante",
        *,
        iva: float | None = None,
        tarifa_iva: float | None = None,
        proveedor_es_declarante: bool = True,
        gran_contribuyente: bool = False,
        autorretenedor: bool = False,
        regimen_simple: bool = False,
        aplicar_reteiva: bool = True,
        actividad_ica: str | None = None,
        tarifa_ica_por_mil: float | None = None,
        actividad_autorretencion: str | None = None,
    ) -> Resultado:
        """Calcula todas las retenciones de una compra o servicio.

        base_gravable  : valor antes de IVA
        concepto       : llave de tarifas_2026.json -> retefuente (ver .conceptos())
        gran_contribuyente / autorretenedor : el proveedor no sufre retefuente
        regimen_simple : no se le practica retefuente ni reteICA (Art. 911 ET)
        """
        rf_cfg = self.t["retefuente"].get(concepto)
        if rf_cfg is None:
            raise KeyError(
                f"Concepto '{concepto}' no existe. Disponibles: {list(self.t['retefuente'])}"
            )

        tarifa_iva = self.t["iva_general"] if tarifa_iva is None else tarifa_iva
        iva = round(base_gravable * tarifa_iva, 2) if iva is None else iva

        r = Resultado(
            base_gravable=round(base_gravable, 2),
            concepto=concepto,
            descripcion_concepto=rf_cfg["descripcion"],
            iva=round(iva, 2),
        )

        # ---------------------------------------------------- retefuente
        base_min_rf = self.uvt_a_pesos(rf_cfg["base_uvt"])
        r.base_minima_retefuente = base_min_rf
        tarifa_rf = rf_cfg["tarifa"]

        # ajuste automatico declarante / no declarante en los conceptos que lo tienen
        if not proveedor_es_declarante and concepto.endswith("_declarante"):
            alterno = concepto.replace("_declarante", "_no_declarante")
            if alterno in self.t["retefuente"]:
                rf_cfg = self.t["retefuente"][alterno]
                tarifa_rf = rf_cfg["tarifa"]
                r.descripcion_concepto = rf_cfg["descripcion"]
                r.observaciones.append(
                    f"Proveedor no declarante: se aplico la tarifa de {tarifa_rf*100:.2f}%"
                )

        r.tarifa_retefuente = tarifa_rf
        if regimen_simple:
            r.observaciones.append(
                "Proveedor del Regimen Simple (SIMPLE): no se practica retefuente ni reteICA "
                "(Art. 911 ET); el comprador debe actuar como autorretenedor de renta. "
                "Si el proveedor SIMPLE es responsable de IVA, valide caso a caso el reteIVA."
            )
        elif gran_contribuyente or autorretenedor:
            r.observaciones.append(
                "Proveedor autorretenedor o gran contribuyente: no se le practica retefuente."
            )
        elif base_gravable < base_min_rf:
            r.observaciones.append(
                f"Base {base_gravable:,.0f} inferior a la base minima de "
                f"{rf_cfg['base_uvt']} UVT ({base_min_rf:,.0f}): no hay retefuente."
            )
        else:
            r.retefuente = round(base_gravable * tarifa_rf, 2)

        # ------------------------------------------------------- reteiva
        cfg_iva = self.t["reteiva"]
        es_servicio = "servicio" in concepto or "honorarios" in concepto or "arrendamiento" in concepto
        base_min_iva = self.uvt_a_pesos(
            cfg_iva["base_uvt_servicios"] if es_servicio else cfg_iva["base_uvt_compras"]
        )
        if aplicar_reteiva and iva > 0 and not regimen_simple:
            if base_gravable < base_min_iva:
                r.observaciones.append(
                    f"Base inferior al minimo de reteIVA ({base_min_iva:,.0f}): no se practica."
                )
            else:
                r.tarifa_reteiva = cfg_iva["tarifa"]
                r.reteiva = round(iva * cfg_iva["tarifa"], 2)

        # ------------------------------------------------------- reteica
        cfg_ica = self.t["reteica"]
        if tarifa_ica_por_mil is None and actividad_ica:
            tarifa_ica_por_mil = cfg_ica["tarifas_por_mil"].get(actividad_ica)
            if tarifa_ica_por_mil is None:
                r.observaciones.append(
                    f"Actividad ICA '{actividad_ica}' no parametrizada: no se calculo reteICA."
                )
        if tarifa_ica_por_mil and not regimen_simple:
            r.tarifa_reteica_por_mil = tarifa_ica_por_mil
            r.reteica = round(base_gravable * tarifa_ica_por_mil / 1000, 2)

        # --------------------------------------- autorretencion en renta
        if actividad_autorretencion:
            tar = self.t["autorretencion_renta"]["tarifas"].get(actividad_autorretencion)
            if tar is None:
                r.observaciones.append(
                    f"Actividad de autorretencion '{actividad_autorretencion}' no parametrizada."
                )
            else:
                r.autorretencion_renta = round(base_gravable * tar, 2)

        # ---------------------------------------------------------- totales
        r.total_retenciones = round(r.retefuente + r.reteiva + r.reteica, 2)
        r.neto_a_pagar = round(base_gravable + iva - r.total_retenciones, 2)
        return r


# --------------------------------------------------------------------------- #
#  Demostracion por consola
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    c = Calculadora()
    print(f"UVT {c.t['vigencia']}: ${c.uvt:,.0f}\n")
    print(c.t["advertencia"], "\n")

    casos = [
        ("Compra de mercancia a proveedor declarante", dict(
            base_gravable=12_000_000, concepto="compras_generales_declarante",
            actividad_ica="comercio_al_por_mayor_y_menor")),
        ("Honorarios de revisoria fiscal (persona juridica)", dict(
            base_gravable=4_500_000, concepto="honorarios_pj",
            actividad_ica="servicios_generales")),
        ("Servicio de aseo pequeno (por debajo de la base)", dict(
            base_gravable=150_000, concepto="servicios_generales_declarante")),
        ("Compra a proveedor del Regimen Simple", dict(
            base_gravable=6_000_000, concepto="compras_generales_declarante",
            regimen_simple=True, actividad_ica="comercio_al_por_mayor_y_menor")),
    ]
    for titulo, kwargs in casos:
        print("=" * 68)
        print(titulo)
        print("-" * 68)
        print(c.calcular(**kwargs).resumen())
        print()
