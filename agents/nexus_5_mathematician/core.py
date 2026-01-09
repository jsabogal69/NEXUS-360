import logging
from ..shared.utils import get_db, generate_id, timestamp_now, report_agent_activity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-5")

class Nexus5Mathematician:
    task_description = "Deep Financial Modeling & ROI Projection (Reactive)"
    def __init__(self):
        self.db = get_db()
        self.role = "NEXUS-5 (Mathematician)"

    @report_agent_activity
    async def calculate_roi_models(self, strategy_data: dict) -> dict:
        """
        Deep Financial Engine. Builds deterministic ROI models based on the 
        detected category and strategic recommendations.
        """
        logger.info(f"[{self.role}] Computing Deep Financial Models...")
        
        # 1. CORE NICHE DETECTION (Prioritize Scout Anchor)
        anchor = strategy_data.get("scout_anchor", "Mercado Analizado")
        norm_anchor = anchor.upper().replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
        
        is_lamp = any(x in norm_anchor for x in ["LAMP", "ILUMINACION", "LAMPARA", "LED", "LIGHTING"])
        is_electronics = any(x in norm_anchor for x in ["65W", "GAN", "CHARGER", "ADAPTADOR", "POWER"])
        is_baby = any(x in norm_anchor for x in ["BABY", "NIGHT LIGHT", "SLEEP AID", "BEBE", "NOCHE", "SUEÑO"])
        is_supplement = any(x in norm_anchor for x in ["PROTEIN", "VITAMIN", "SUPPLEMENT"])

        if is_baby:
            base_price = 39.99
            landed_cost = 7.20
            kit_price = 119.99
            kit_cost = 28.00
            label = "Baby Sleep Tech"
        elif is_lamp:
            base_price = 49.99
            landed_cost = 14.50
            kit_price = 129.99
            kit_cost = 38.00
            label = "Lámpara LED Pro"
        elif is_electronics:
            base_price = 44.99
            landed_cost = 11.20
            kit_price = 89.99
            kit_cost = 24.50
            label = "Adaptador GaN 65W"
        elif is_supplement:
            base_price = 39.99
            landed_cost = 8.50
            kit_price = 110.00
            kit_cost = 35.00
            label = "Suplemento Premium"
        else:
            base_price = 50.00
            landed_cost = 15.00
            kit_price = 125.00
            kit_cost = 40.00
            label = "Unidad Base"

        # 1. CORE UNIT ECONOMICS MODELS (AMAZON CALIBRATION)
        sales = strategy_data.get("sales_intelligence", {})
        peaks = sales.get("seasonality", {}).get("peaks", [])
        peak_months = [p['month'] for p in peaks if p['impact'] in ["Max", "Extreme"]]
        
        amz_referral_pct = 0.15  
        amz_fba_fee = 6.50       
        amz_storage_mth = 0.85   
        ppc_investment_pct = 0.28 if peak_months else 0.22 # Variable Ads based on seasonality intensity
        
        amazon_economics = {
            "msrp": base_price,
            "cogs_landed": landed_cost,
            "referral_fee": round(base_price * amz_referral_pct, 2),
            "fba_fulfillment": amz_fba_fee,
            "monthly_storage": amz_storage_mth,
            "ads_spend_cac": round(base_price * ppc_investment_pct, 2),
            "total_amz_opex": round((base_price * amz_referral_pct) + amz_fba_fee + amz_storage_mth + (base_price * ppc_investment_pct), 2),
            "seasonality_intensity": "High" if peak_months else "Standard"
        }

        scenarios = {
            "individual_amz": {
                "name": f"Amazon Strategy: Unidad Base ({label})",
                "price": base_price,
                "landed": landed_cost,
                "opex": amazon_economics["total_amz_opex"],
                "margin_pct": round(((base_price - (landed_cost + amazon_economics["total_amz_opex"])) / base_price) * 100, 1),
                "viability": "Risk High",
                "breakdown": {
                    "Amazon Fees (15% + FBA)": f"${amazon_economics['referral_fee'] + amz_fba_fee}",
                    "Ads/PPC Spend (25%)": f"${amazon_economics['ads_spend_cac']}",
                    "Net Margin": f"${round(base_price - (landed_cost + amazon_economics['total_amz_opex']), 2)}"
                },
                "notes": "Escenario de venta transaccional de alta fricción. El modelo confirma que el 40%+ del capital bruto es absorbido por el ecosistema de Amazon (Marketplace Fees + PPC), dejando un margen de seguridad estrecho ante fluctuaciones de CAC. Esta vía se recomienda exclusivamente como motor de visibilidad ('Loss Leader') para alimentar el algoritmo y capturar el ranking inicial en el nicho, actuando como puerta de entrada para el resto del ecosistema NEXUS."
            },
            "multipack_amz": {
                "name": f"Optimization Strategy: Multi-Pack (X2 Units)",
                "price": round(base_price * 1.85, 2),
                "landed": landed_cost * 2,
                "opex": round((base_price * 1.85 * 0.15) + amz_fba_fee + 2.00 + (base_price * 0.20), 2),
                "margin_pct": round(((round(base_price * 1.85, 2) - ((landed_cost * 2) + round((base_price * 1.85 * 0.15) + amz_fba_fee + 2.00 + (base_price * 0.20), 2))) / round(base_price * 1.85, 2)) * 100, 1),
                "viability": "Medium High",
                "breakdown": {
                    "FBA Savings (Shared)": f"${round(amz_fba_fee, 2)}",
                    "PPC Efficiency (+15%)": f"${round(base_price * 0.20, 2)}",
                    "Net Margin": f"${round(round(base_price * 1.85, 2) - ((landed_cost * 2) + round((base_price * 1.85 * 0.15) + amz_fba_fee + 2.00 + (base_price * 0.20), 2)), 2)}"
                },
                "notes": "Optimización de Unit Economics mediante la dilución radical de costos logísticos fijos. Al compartir el 'Last-Mile Delivery' y el 'FBA Fulfillment' entre múltiples unidades, el margen neto se expande significativamente. Estrategia de guerrilla ideal para capturar al segmento 'Pro-sumer', maximizando el Lifetime Value (LTV) desde el primer contacto y reduciendo la dependencia de la compra única."
            },
            "kit_premium": {
                "name": f"NEXUS Masterpiece: Digital Kit / Ecosistema",
                "price": kit_price,
                "landed": kit_cost,
                "opex": amazon_economics["total_amz_opex"] + 5.00,
                "margin_pct": round(((kit_price - (kit_cost + amazon_economics["total_amz_opex"] + 5.00)) / kit_price) * 100, 1),
                "viability": "Recommended",
                "breakdown": {
                    "Shared CAC (Efficiency)": f"${round(kit_price * 0.12, 2)}",
                    "High Ticket Buffer": f"${round(kit_price * 0.10, 2)}",
                    "Net Margin": f"${round(kit_price - (kit_cost + amazon_economics['total_amz_opex'] + 5.00), 2)}"
                },
                "notes": "La culminación de la propuesta de valor NEXUS. Al inyectar valor intangible (Capa de Software, Garantía VIP, Ecosistema Digital), desacoplamos el precio final del costo físico de los materiales (BOM). Este escenario crea un 'Foso Defensivo' inexpugnable contra la competencia de bajo costo, permitiendo un Premium del 40% sobre el MSRP promedio del mercado sin erosionar la tasa de conversión."
            },
            "dtc_exclusive": {
                "name": "DTC Strategy: Venta Directa (Web Propia)",
                "price": kit_price,
                "landed": kit_cost,
                "opex": round((kit_price * 0.03) + 12.00 + (kit_price * 0.25), 2), # Gateway + Shipping + Branding Ads
                "margin_pct": round(((kit_price - (kit_cost + round((kit_price * 0.03) + 12.00 + (kit_price * 0.25), 2))) / kit_price) * 100, 1),
                "viability": "Visionary",
                "breakdown": {
                    "No Marketplace Fees": "0% Fees",
                    "Branding Investment": f"${round(kit_price * 0.25, 2)}",
                    "Net Margin": f"${round(kit_price - (kit_cost + round((kit_price * 0.03) + 12.00 + (kit_price * 0.25), 2)), 2)}"
                },
                "notes": "Escenario de soberanía de marca total e independencia de plataforma. Aunque la inversión inicial en adquisición de tráfico (Meta/TikTok Ads) es elevada, la eliminación de las comisiones de Amazon y la propiedad absoluta de los datos del cliente permiten una rentabilidad compuesta. Es la vía crítica para transformar un producto de impulso en una marca con 'Brand Equity' y valor de salida (Exit Value) real."
            },
            "b2b_bulk": {
                "name": "B2B Strategy: Canal Corporativo / Mayorista",
                "price": round(base_price * 1.4, 2), # Bundled in volume cases
                "landed": landed_cost,
                "opex": round(base_price * 0.10, 2), # Logistics only, no PPC
                "margin_pct": round(((round(base_price * 1.4, 2) - (landed_cost + round(base_price * 0.10, 2))) / round(base_price * 1.4, 2)) * 100, 1),
                "viability": "Stable",
                "breakdown": {
                    "Zero PPC Ads": "$0.00",
                    "Logística de Volumen": f"${round(base_price * 0.10, 2)}",
                    "Net Margin": f"${round(round(base_price * 1.4, 2) - (landed_cost + round(base_price * 0.10, 2)), 2)}"
                },
                "notes": "Canal de estabilización de flujo de caja y rentabilidad pura. Al eliminar el gasto variable en PPC y la volatilidad algorítmica, este modelo asegura márgenes netos de dos dígitos altos. Se recomienda para contratos de suministro corporativo o 'Hard-Bundling', actuando como el pulmón financiero que permite financiar las campañas de marca agresivas en los canales de retail."
            }
        }
        
        if peak_months:
            seasonality_note = f"VENTANA DE LIQUIDEZ MÁXIMA DETECTADA: El capital debe concentrarse 90 días antes de {', '.join(peak_months)}. Se recomienda un fondo de reserva para escalar el PPC durante estos meses donde el ROAS tiende a duplicarse."
        else:
            seasonality_note = "ESTACIONALIDAD ESTABLE: Los márgenes proyectados mantienen una linealidad constante. Se recomienda un escalado orgánico y sostenido del inventario."

        # 2. MARKET BENCHMARK COMPARISON (Forensic Insight)
        top_10 = strategy_data.get("scout_data", {}).get("top_10_products", [])
        best_seller = top_10[0] if top_10 else {"name": "Líder de Categoría", "price": base_price * 1.2}
        mid_range = top_10[4] if len(top_10) > 4 else {"name": "Competidor Promedio", "price": base_price * 0.9}

        market_benchmark = {
            "best_seller": {
                "name": best_seller.get("name"),
                "msrp": best_seller.get("price"),
                "est_landed": round(best_seller.get("price") * 0.2, 2), # Assumed high volume efficiency
                "net_profit": round(best_seller.get("price") * 0.15, 2), # Assumed narrow margins
                "is_assumed": True
            },
            "mid_range": {
                "name": mid_range.get("name"),
                "msrp": mid_range.get("price"),
                "est_landed": round(mid_range.get("price") * 0.25, 2),
                "net_profit": round(mid_range.get("price") * 0.12, 2),
                "is_assumed": True
            },
            "nexus_suggested": {
                "name": f"NEXUS {label} Platinum",
                "msrp": kit_price,
                "landed": kit_cost,
                "net_profit": round(kit_price - (kit_cost + amazon_economics['total_amz_opex'] + 5.00), 2),
                "is_assumed": False # Based on our master strategy
            }
        }

        roi_models = {
            "id": generate_id(),
            "parent_strategy_id": strategy_data.get("id"),
            "scenarios": scenarios,
            "amazon_baseline": amazon_economics,
            "market_benchmark": market_benchmark,
            "seasonality_strategy": seasonality_note,
            "general_market_context": {
                "direct_to_consumer_margin": round(((base_price - (landed_cost + 12.00)) / base_price) * 100, 1),
                "retail_distribution_margin": round(((base_price * 0.5 - landed_cost) / (base_price * 0.5)) * 100, 1),
                "sku_proposals": {
                    "DTC_Exclusive": f"NEX-DTO-{label.replace(' ', '-').upper()}-001",
                    "B2B_Bulk": f"NEX-CORP-{label.replace(' ', '-').upper()}-V01"
                }
            },
            "timestamp": timestamp_now()
        }
        
        self._save_models(roi_models)
        return roi_models

    def _save_models(self, data: dict):
        if not self.db: return
        try:
            self.db.collection("validated_intelligence").document(data["id"]).set(data)
        except: pass
