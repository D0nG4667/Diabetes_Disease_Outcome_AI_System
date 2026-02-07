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
        self.api_key = os.getenv("ML_API_KEY", "") 
        self.timeout = 10  # seconds

    def get_docs_url(self) -> str:
        """Return the URL to the Swagger documentation."""
        return f"{self.base_url}/docs"

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def _handle_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Generic request handler with error management.
        """
        try:
            kwargs.setdefault("headers", self._get_headers())
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            st.error(f"⏱️ API Request timed out connecting to {url}")
            return None
        except requests.exceptions.ConnectionError:
            st.error(f"🔌 Could not connect to API at {self.base_url}")
            return None
        except requests.exceptions.HTTPError as e:
            self._handle_error(e)
            return None
        except Exception as e:
            st.error(f"⚠️ Unexpected Error: {e}")
            return None

    def _handle_error(self, e: requests.HTTPError):
        """Friendly error display."""
        try:
            error_data = e.response.json()
            detail = error_data.get("detail", str(e))
            st.error(f"❌ API Error ({e.response.status_code}): {detail}")
        except:
            st.error(f"❌ API Error ({e.response.status_code}): {str(e)}")

    def health_check(self) -> bool:
        """Simple health check."""
        status = self.get_detailed_status()
        return status["healthy"]

    def get_detailed_status(self) -> Dict[str, Any]:
        """Detailed status probing."""
        status = {
            "healthy": False,
            "connection": False,
            "model": False,
            "message": "Initializing..."
        }
        
        try:
            # 1. Connection & Model Check via /health
            health_url = f"{self.base_url}/health"
            resp = requests.get(health_url, timeout=2)
            
            if resp.status_code == 200:
                status["connection"] = True
                data = resp.json()
                # ML Backend returns "healthy" when model is loaded
                if data.get("status") == "healthy" and data.get("artifacts_loaded") is True:
                    status["model"] = True
                else:
                    status["message"] = "Model Not Ready/Loaded"
            else:
                status["message"] = f"Backend Error ({resp.status_code})"
                return status

            # 2. Final State Aggregation (Auth is not used in ML system)
            if status["connection"] and status["model"]:
                status["healthy"] = True
                status["message"] = "System Operational"

        except requests.exceptions.ConnectionError:
            status["message"] = "Connection Refused"
        except Exception as e:
            status["message"] = f"Error: {str(e)}"
            
        return status

    def predict(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        url = f"{self.api_v1}/predict"
        return self._handle_request("POST", url, json=payload)

    def explain(self, payload: Dict[str, Any], top_n: int = 10, plot: bool = False) -> Optional[Dict[str, Any]]:
        url = f"{self.api_v1}/explain"
        params = {"top_n": top_n, "plot": plot}
        return self._handle_request("POST", url, json=payload, params=params)

# Singleton instance
api_client = APIClient()
