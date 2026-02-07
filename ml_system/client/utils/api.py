import os
import requests
import streamlit as st
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APIClient:
    def __init__(self):
        self.base_url = os.getenv("ML_API_URL", "http://localhost:8000").rstrip("/")
        self.api_v1 = f"{self.base_url}/api/v1"
        self.timeout = 10  # seconds

    def _handle_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Generic request handler with error management.
        """
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            st.error(f"⏱️ API Request timed out connecting to {url}")
            return None
        except requests.exceptions.ConnectionError:
            st.error(f"🔌 Could not connect to API at {self.base_url}. Is the backend running?")
            return None
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ API Error: {e}")
            return None
        except Exception as e:
            st.error(f"⚠️ Unexpected Error: {e}")
            return None

    def health_check(self) -> bool:
        """
        Check system health.
        """
        url = f"{self.base_url}/health"
        data = self._handle_request("GET", url)
        return data is not None and data.get("status") == "ok"

    def predict(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send prediction request.
        """
        url = f"{self.api_v1}/predict"
        return self._handle_request("POST", url, json=payload)

    def explain(self, payload: Dict[str, Any], top_n: int = 10, plot: bool = False) -> Optional[Dict[str, Any]]:
        """
        Send explanation request.
        """
        # backend is /api/v1/explain?top_n=10&plot=false
        url = f"{self.api_v1}/explain"
        params = {"top_n": top_n, "plot": plot}
        return self._handle_request("POST", url, json=payload, params=params)

# Singleton instance
api_client = APIClient()
