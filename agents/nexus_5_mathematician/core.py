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
                "break_even_qty": round(5000 / (base_price - (landed_cost + amazon_economics["total_amz_opex"]))), # Assuming 5k launch investment
                "payback_months": 8,
                "breakdown": {
                    "Amazon Fees (15% + FBA)": f"${amazon_economics['referral_fee'] + amz_fba_fee}",
                    "Ads/PPC Spend (25%)": f"${amazon_economics['ads_spend_cac']}",
                    "Net Margin": f"${round(base_price - (landed_cost + amazon_economics['total_amz_opex']), 2)}"
                },
                "notes": "Escenario de venta transaccional de alta fricción. El modelo confirma que el 40%+ del capital bruto es absorbido por el ecosistema de Amazon (Marketplace Fees + PPC), dejando un margen de seguridad estrecho ante fluctuaciones de CAC. Esta vía se recomienda exclusivamente como motor de visibilidad ('Loss Leader') para alimentar el algoritmo y capturar el ranking inicial en el nicho, actuando como puerta de entrada para el resto del ecosistema NEXUS. Se requiere un control de inventario agresivo para evitar roturas de stock que penalicen el ranking orgánico ganado."
            },
            "multipack_amz": {
                "name": f"Optimization Strategy: Multi-Pack (X2 Units)",
                "price": round(base_price * 1.85, 2),
                "landed": landed_cost * 2,
                "opex": round((base_price * 1.85 * 0.15) + amz_fba_fee + 2.00 + (base_price * 0.20), 2),
                "margin_pct": round(((round(base_price * 1.85, 2) - ((landed_cost * 2) + round((base_price * 1.85 * 0.15) + amz_fba_fee + 2.00 + (base_price * 0.20), 2))) / round(base_price * 1.85, 2)) * 100, 1),
                "viability": "Medium High",
                "break_even_qty": round(7500 / (round(base_price * 1.85, 2) - ((landed_cost * 2) + round((base_price * 1.85 * 0.15) + amz_fba_fee + 2.00 + (base_price * 0.20), 2)))),
                "payback_months": 5,
                "breakdown": {
                    "FBA Savings (Shared)": f"${round(amz_fba_fee, 2)}",
                    "PPC Efficiency (+15%)": f"${round(base_price * 0.20, 2)}",
                    "Net Margin": f"${round(round(base_price * 1.85, 2) - ((landed_cost * 2) + round((base_price * 1.85 * 0.15) + amz_fba_fee + 2.00 + (base_price * 0.20), 2)), 2)}"
                },
                "notes": "Optimización de Unit Economics mediante la dilución radical de costos logísticos fijos. Al compartir el 'Last-Mile Delivery' y el 'FBA Fulfillment' entre múltiples unidades, el margen neto se expande significativamente. Estrategia de guerrilla ideal para capturar al segmento 'Pro-sumer', maximizando el Lifetime Value (LTV) desde el primer contacto y reduciendo la dependencia de la compra única. El 'Average Order Value' (AOV) superior compensa la inversión inicial en PPC de manera más acelerada."
            },
            "kit_premium": {
                "name": f"NEXUS Masterpiece: Digital Kit / Ecosistema",
                "price": kit_price,
                "landed": kit_cost,
                "opex": amazon_economics["total_amz_opex"] + 5.00,
                "margin_pct": round(((kit_price - (kit_cost + amazon_economics["total_amz_opex"] + 5.00)) / kit_price) * 100, 1),
                "viability": "Recommended",
                "break_even_qty": round(15000 / (kit_price - (kit_cost + amazon_economics["total_amz_opex"] + 5.00))),
                "payback_months": 4,
                "breakdown": {
                    "Shared CAC (Efficiency)": f"${round(kit_price * 0.12, 2)}",
                    "High Ticket Buffer": f"${round(kit_price * 0.10, 2)}",
                    "Net Margin": f"${round(kit_price - (kit_cost + amazon_economics['total_amz_opex'] + 5.00), 2)}"
                },
                "notes": "La culminación de la propuesta de valor NEXUS. Al inyectar valor intangible (Capa de Software, Garantía VIP, Ecosistema Digital), desacoplamos el precio final del costo físico de los materiales (BOM). Este escenario crea un 'Foso Defensivo' inexpugnable contra la competencia de bajo costo, permitiendo un Premium del 40% sobre el MSRP promedio del mercado sin erosionar la tasa de conversión. El payback es el más rápido de todos los modelos debido a la alta contribución marginal por cada venta."
            },
            "dtc_exclusive": {
                "name": "DTC Strategy: Venta Directa (Web Propia)",
                "price": kit_price,
                "landed": kit_cost,
                "opex": round((kit_price * 0.03) + 12.00 + (kit_price * 0.25), 2), # Gateway + Shipping + Branding Ads
                "margin_pct": round(((kit_price - (kit_cost + round((kit_price * 0.03) + 12.00 + (kit_price * 0.25), 2))) / kit_price) * 100, 1),
                "viability": "Visionary",
                "break_even_qty": round(20000 / (kit_price - (kit_cost + round((kit_price * 0.03) + 12.00 + (kit_price * 0.25), 2)))),
                "payback_months": 12,
                "breakdown": {
                    "No Marketplace Fees": "0% Fees",
                    "Branding Investment": f"${round(kit_price * 0.25, 2)}",
                    "Net Margin": f"${round(kit_price - (kit_cost + round((kit_price * 0.03) + 12.00 + (kit_price * 0.25), 2)), 2)}"
                },
                "notes": "Escenario de soberanía de marca total e independencia de plataforma. Aunque la inversión inicial en adquisición de tráfico (Meta/TikTok Ads) es elevada, la eliminación de las comisiones de Amazon y la propiedad absoluta de los datos del cliente permiten una rentabilidad compuesta. Es la vía crítica para transformar un producto de impulso en una marca con 'Brand Equity' y valor de salida (Exit Value) real. Se recomienda el uso de un funnel de suscripción ('Sub & Save') para maximizar la recurrencia."
            },
            "b2b_bulk": {
                "name": "B2B Strategy: Canal Corporativo / Mayorista",
                "price": round(base_price * 1.4, 2), # Bundled in volume cases
                "landed": landed_cost,
                "opex": round(base_price * 0.10, 2), # Logistics only, no PPC
                "margin_pct": round(((round(base_price * 1.4, 2) - (landed_cost + round(base_price * 0.10, 2))) / round(base_price * 1.4, 2)) * 100, 1),
                "viability": "Stable",
                "break_even_qty": round(10000 / (round(base_price * 1.4, 2) - (landed_cost + round(base_price * 0.10, 2)))),
                "payback_months": 6,
                "breakdown": {
                    "Zero PPC Ads": "$0.00",
                    "Logística de Volumen": f"${round(base_price * 0.10, 2)}",
                    "Net Margin": f"${round(round(base_price * 1.4, 2) - (landed_cost + round(base_price * 0.10, 2)), 2)}"
                },
                "notes": "Canal de estabilización de flujo de caja y rentabilidad pura. Al eliminar el gasto variable en PPC y la volatilidad algorítmica, este modelo asegura márgenes netos de dos dígitos altos. Se recomienda para contratos de suministro corporativo o 'Hard-Bundling', actuando como el pulmón financiero que permite financiar las campañas de marca agresivas en los canales de retail. Ideal para rotación de stock estancado mediante acuerdos 'Close-out'."
            }
        }
        
        if peak_months:
            seasonality_note = f"VENTANA DE LIQUIDEZ MÁXIMA DETECTADA: El capital debe concentrarse 90 días antes de {', '.join(peak_months)}. Se recomienda un fondo de reserva para escalar el PPC durante estos meses donde el ROAS tiende a duplicarse."
        else:
            seasonality_note = "ESTACIONALIDAD ESTABLE: Los márgenes proyectados mantienen una linealidad constante. Se recomienda un escalado orgánico y sostenido del inventario."

        # 2. MARKET BENCHMARK COMPARISON (Forensic Insight & FBA Sensitivity)
        top_10 = strategy_data.get("scout_data", {}).get("top_10_products", [])
        
        # FBA Sensitivity Calibration (Simulated based on category weight/size logic)
        # Tiers: Small/Light (<$3.50), Standard ($4.50-$6.50), Large ($8.00+)
        category_fba_base = amz_fba_fee # 6.50 from baseline

        def calculate_efficiency_tier(price, fba_fee):
            impact = (fba_fee / price) * 100 if price > 0 else 0
            if impact < 12: return "Tier 1: High Efficiency (Dominance)", "#059669", impact
            if impact < 18: return "Tier 2: Mid-Range (Standard)", "#2563eb", impact
            return "Tier 3: Low Efficiency (Vulnerable)", "#dc2626", impact

        market_benchmark = {}
        processed_top_10 = []

        for p in top_10:
            p_price = p.get("price", 50.0)
            # Calibration: Competitors usually have slightly higher or lower FBA based on their rank/volume
            # Ranking 1-3 usually has size optimization (Tier 1)
            p_fba = category_fba_base - 1.0 if p.get("rank", 10) <= 3 else (category_fba_base + 1.5 if p.get("rank", 10) > 7 else category_fba_base)
            tier_label, tier_color, impact_pct = calculate_efficiency_tier(p_price, p_fba)
            
            p_landed = round(p_price * 0.22, 2)
            p_referral = round(p_price * 0.15, 2)
            p_profit = round(p_price - (p_landed + p_referral + p_fba + (p_price * 0.10)), 2) # Assumed 10% PPC for comps

            processed_top_10.append({
                "rank": p.get("rank"),
                "name": p.get("name"),
                "msrp": p_price,
                "fba_fee": p_fba,
                "fba_impact_pct": round(impact_pct, 1),
                "efficiency_tier": tier_label,
                "tier_color": tier_color,
                "est_net_profit": p_profit,
                "is_assumed": True
            })

        # Specific NEXUS Comparison
        n_tier, n_color, n_impact = calculate_efficiency_tier(kit_price, amz_fba_fee)
        
        roi_models = {
            "id": generate_id(),
            "parent_strategy_id": strategy_data.get("id"),
            "scenarios": scenarios,
            "amazon_baseline": amazon_economics,
            "fba_sensitivity_analysis": {
                "competitors": processed_top_10,
                "nexus_target": {
                    "name": f"NEXUS {label} Platinum",
                    "msrp": kit_price,
                    "fba_fee": amz_fba_fee,
                    "fba_impact_pct": round(n_impact, 1),
                    "efficiency_tier": n_tier,
                    "tier_color": n_color
                }
            },
            "market_benchmark": { # Legacy support
                "best_seller": processed_top_10[0] if processed_top_10 else {},
                "mid_range": processed_top_10[4] if len(processed_top_10) > 4 else {}
            },
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
