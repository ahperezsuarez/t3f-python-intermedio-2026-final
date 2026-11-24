import requests
from typing import List, Dict, Optional, Tuple

API_SALES_URL = "http://127.0.0.1:8000/sales"

class SaleService:
    @staticmethod
    def get_all() -> Tuple[Optional[List[Dict]], Optional[str]]:
        try:
            res = requests.get(f"{API_SALES_URL}/", timeout=5)
            if res.status_code == 200:
                return res.json(), None
            return None, res.json().get("detail", "Error cargando ventas")
        except requests.exceptions.RequestException as e:
            return None, f"Error de red: {e}"

    @staticmethod
    def create_sale(customer_id: int, items: List[Dict]) -> Tuple[bool, Optional[str]]:
        try:
            payload = {"customer_id": customer_id, "items": items}
            res = requests.post(f"{API_SALES_URL}/", json=payload, timeout=5)
            if res.status_code == 201:
                return True, None
            return False, res.json().get("detail", "Error al procesar la venta")
        except requests.exceptions.RequestException as e:
            return False, f"Error de red: {e}"