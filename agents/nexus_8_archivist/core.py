"""
Nexus_8_Archivist: Archive Agent for Firebase
Archives all case data for traceability and longitudinal product studies.
"""
import hashlib
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

def generate_product_hash(query: str) -> str:
    """Generate consistent hash for product queries to enable grouping."""
    # Normalize: lowercase, strip, remove extra spaces
    normalized = " ".join(query.lower().strip().split())
    return hashlib.md5(normalized.encode()).hexdigest()[:12]

def timestamp_now():
    return datetime.utcnow()


class Nexus8Archivist:
    """
    Archivist Agent - Archives all NEXUS-360 case data to Firebase.
    
    Features:
    - Archive complete case data (SSOT + report)
    - Track product history for longitudinal studies
    - Retrieve past cases for reference
    """
    
    def __init__(self, db=None):
        self.db = db
        self.role = "Nexus-8 Archivist"
        logger.info(f"[{self.role}] Initialized. DB: {'Active' if db else 'MockDB'}")
    
    def archive_case(
        self,
        case_id: str,
        product_query: str,
        ssot: dict,
        report_html: str,
        verdict: dict = None,
        metadata: dict = None
    ) -> dict:
        """
        Archive a complete case to Firebase.
        
        Args:
            case_id: Unique identifier for this case
            product_query: Original user query/product description
            ssot: Complete SSOT data from pipeline
            report_html: Generated HTML report
            verdict: Dynamic verdict from Strategist
            metadata: Additional metadata
        
        Returns:
            Archive record with case_id and product_hash
        """
        logger.info(f"[{self.role}] Archiving case: {case_id}")
        
        product_hash = generate_product_hash(product_query)
        
        # Extract key metadata from SSOT
        scout_data = ssot.get("scout_data", {})
        top_10 = scout_data.get("top_10_products", [])
        sales_intel = scout_data.get("sales_intelligence", {})
        market_share = sales_intel.get("market_share_by_brand", [])
        
        # Build archive record
        archive_record = {
            "case_id": case_id,
            "created_at": timestamp_now(),
            "product_query": product_query,
            "product_hash": product_hash,
            "ssot_snapshot": ssot,
            "report_html": report_html,
            "verdict_summary": verdict.get("title", "") if verdict else "",
            "verdict_text": verdict.get("text", "") if verdict else "",
            "metadata": {
                "niche": ssot.get("strategist_data", {}).get("scout_anchor", product_query[:50]),
                "top_brands": [p.get("brand", "Unknown") for p in top_10[:5]],
                "avg_price": sum([p.get("price", 0) for p in top_10]) / len(top_10) if top_10 else 0,
                "gaps_count": len(ssot.get("strategist_data", {}).get("strategic_gaps", [])),
                "market_leaders": [m.get("brand", "") for m in market_share[:3]],
                **(metadata or {})
            }
        }
        
        # Save to Firebase
        if self.db:
            try:
                # Save case
                self.db.collection("nexus_archive").document(case_id).set(archive_record)
                logger.info(f"[{self.role}] ✅ Case archived: {case_id}")
                
                # Update product index for longitudinal tracking
                self._update_product_index(product_hash, product_query, case_id)
                
            except Exception as e:
                logger.error(f"[{self.role}] ❌ Archive failed: {e}")
        else:
            logger.warning(f"[{self.role}] ⚠️ No DB - case not persisted (MockDB mode)")
        
        return {
            "case_id": case_id,
            "product_hash": product_hash,
            "archived_at": timestamp_now().isoformat(),
            "status": "archived" if self.db else "mock_only"
        }
    
    def _update_product_index(self, product_hash: str, product_name: str, case_id: str):
        """Update product index to track all cases for this product."""
        if not self.db:
            return
        
        try:
            product_ref = self.db.collection("product_index").document(product_hash)
            product_doc = product_ref.get()
            
            if product_doc.exists:
                # Add to existing product history
                existing = product_doc.to_dict()
                case_ids = existing.get("case_ids", [])
                if case_id not in case_ids:
                    case_ids.append(case_id)
                product_ref.update({
                    "case_ids": case_ids,
                    "last_analyzed": timestamp_now(),
                    "analysis_count": len(case_ids)
                })
                logger.info(f"[{self.role}] Updated product index: {product_hash} ({len(case_ids)} cases)")
            else:
                # Create new product entry
                product_ref.set({
                    "product_hash": product_hash,
                    "product_name": product_name[:100],
                    "case_ids": [case_id],
                    "first_analyzed": timestamp_now(),
                    "last_analyzed": timestamp_now(),
                    "analysis_count": 1
                })
                logger.info(f"[{self.role}] Created product index: {product_hash}")
                
        except Exception as e:
            logger.warning(f"[{self.role}] Product index update failed: {e}")
    
    def retrieve_case(self, case_id: str) -> Optional[dict]:
        """Retrieve a specific case by ID."""
        if not self.db:
            logger.warning(f"[{self.role}] No DB connection")
            return None
        
        try:
            doc = self.db.collection("nexus_archive").document(case_id).get()
            if doc.exists:
                logger.info(f"[{self.role}] Retrieved case: {case_id}")
                return doc.to_dict()
            else:
                logger.warning(f"[{self.role}] Case not found: {case_id}")
                return None
        except Exception as e:
            logger.error(f"[{self.role}] Retrieve failed: {e}")
            return None
    
    def find_product_history(self, product_query: str) -> List[dict]:
        """
        Find all previous analyses for a product.
        Enables longitudinal studies by comparing cases over time.
        """
        product_hash = generate_product_hash(product_query)
        
        if not self.db:
            logger.warning(f"[{self.role}] No DB - cannot search history")
            return []
        
        try:
            # Get product index
            product_doc = self.db.collection("product_index").document(product_hash).get()
            
            if not product_doc.exists:
                logger.info(f"[{self.role}] No history for product: {product_hash}")
                return []
            
            product_data = product_doc.to_dict()
            case_ids = product_data.get("case_ids", [])
            
            # Retrieve all cases (summary only, not full SSOT)
            cases = []
            for cid in case_ids:
                case_doc = self.db.collection("nexus_archive").document(cid).get()
                if case_doc.exists:
                    case_data = case_doc.to_dict()
                    cases.append({
                        "case_id": cid,
                        "created_at": case_data.get("created_at"),
                        "verdict": case_data.get("verdict_summary"),
                        "avg_price": case_data.get("metadata", {}).get("avg_price"),
                        "top_brands": case_data.get("metadata", {}).get("top_brands"),
                        "gaps_count": case_data.get("metadata", {}).get("gaps_count")
                    })
            
            # Sort by date (newest first)
            cases.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
            logger.info(f"[{self.role}] Found {len(cases)} cases for product: {product_hash}")
            return cases
            
        except Exception as e:
            logger.error(f"[{self.role}] History search failed: {e}")
            return []
    
    def compare_cases(self, case_id_1: str, case_id_2: str) -> dict:
        """
        Compare two cases of the same product to identify changes.
        Useful for longitudinal market studies.
        """
        case1 = self.retrieve_case(case_id_1)
        case2 = self.retrieve_case(case_id_2)
        
        if not case1 or not case2:
            return {"error": "One or both cases not found"}
        
        m1 = case1.get("metadata", {})
        m2 = case2.get("metadata", {})
        
        comparison = {
            "case_1": {"id": case_id_1, "date": str(case1.get("created_at", ""))},
            "case_2": {"id": case_id_2, "date": str(case2.get("created_at", ""))},
            "changes": {
                "price_change": {
                    "before": m1.get("avg_price", 0),
                    "after": m2.get("avg_price", 0),
                    "delta": round(m2.get("avg_price", 0) - m1.get("avg_price", 0), 2),
                    "pct_change": round(((m2.get("avg_price", 1) - m1.get("avg_price", 1)) / m1.get("avg_price", 1)) * 100, 1) if m1.get("avg_price") else 0
                },
                "gaps_change": {
                    "before": m1.get("gaps_count", 0),
                    "after": m2.get("gaps_count", 0)
                },
                "brand_shifts": {
                    "before": m1.get("top_brands", []),
                    "after": m2.get("top_brands", []),
                    "new_entrants": [b for b in m2.get("top_brands", []) if b not in m1.get("top_brands", [])],
                    "exited": [b for b in m1.get("top_brands", []) if b not in m2.get("top_brands", [])]
                },
                "verdict_evolution": {
                    "before": case1.get("verdict_summary", ""),
                    "after": case2.get("verdict_summary", "")
                }
            }
        }
        
        logger.info(f"[{self.role}] Compared cases: {case_id_1} vs {case_id_2}")
        return comparison
    
    def list_all_cases(self, limit: int = 20) -> List[dict]:
        """List all archived cases (for dashboard/admin view)."""
        if not self.db:
            return []
        
        try:
            docs = self.db.collection("nexus_archive").order_by(
                "created_at", direction="DESCENDING"
            ).limit(limit).stream()
            
            cases = []
            for doc in docs:
                data = doc.to_dict()
                cases.append({
                    "case_id": data.get("case_id"),
                    "created_at": data.get("created_at"),
                    "product": data.get("product_query", "")[:50],
                    "verdict": data.get("verdict_summary", ""),
                    "niche": data.get("metadata", {}).get("niche", "")
                })
            
            return cases
        except Exception as e:
            logger.error(f"[{self.role}] List cases failed: {e}")
            return []
