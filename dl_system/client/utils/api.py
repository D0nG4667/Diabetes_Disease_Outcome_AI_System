import os
import requests
import logging
import streamlit as st
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DLClient:
    def __init__(self):
        # Load config from env or streamlit secrets
        self.api_url = os.getenv("DL_API_URL", "http://localhost:8000/api/v1").rstrip("/")
        self.api_key = os.getenv("DL_API_KEY", "pneumonoultramicroscopicsilicovolcanoconiosis")
        self.timeout = 10  # seconds

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def is_healthy(self) -> bool:
        """Check if API is reachable AND configured key/url are valid."""
        try:
            from urllib.parse import urlparse
            
            # 1. Host Reachability & System Health
            parsed = urlparse(self.api_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            health_url = f"{base_url}/health"
            
            resp_health = requests.get(health_url, timeout=2)
            if resp_health.status_code != 200:
                return False
                
            data = resp_health.json()
            if data.get("status") != "healthy" or data.get("artifacts_loaded") is not True:
                return False

            # 2. Configuration Validity (Path & Key)
            # Probe the actual API endpoint to ensure URL path (e.g. /api/v1) is correct.
            # We use GET on a POST endpoint. 
            # - 405 Method Not Allowed -> Path exists, Method wrong (Good)
            # - 401/403 -> Path exists, Auth failed (Bad Key, but System is 'up')
            # - 404 -> Path does not exist (Bad URL)
            probe_url = f"{self.api_url}/predict"
            resp_probe = requests.get(probe_url, timeout=2, headers=self._get_headers())
            
            if resp_probe.status_code == 404:
                # Faulty API URL
                return False
                
            return True

        except (requests.RequestException, ValueError, KeyError):
            return False

    def _is_valid_api_key(self) -> bool:
        """Check if the configured API key is accepted by the backend."""
        try:
            # We probe /predict (protected) with the key.
            # Use POST because GET 405 might bypass Auth dependency.
            url = f"{self.api_url}/predict"
            # Send empty json to trigger validation error (422) if auth works
            response = requests.post(url, json={}, headers=self._get_headers(), timeout=2)
            # 401/403 -> Invalid Key.
            # 200/422 -> Key accepted.
            return response.status_code not in [401, 403]
        except:
            return False

    def get_detailed_status(self) -> Dict[str, Any]:
        """
        Return a detailed status dict for UI components.
        Keys: 'healthy', 'connection', 'auth', 'model', 'message'
        """
        status = {
            "healthy": False,
            "connection": False,
            "auth": False,
            "model": False,
            "message": "Unknown Error"
        }
        
        try:
            from urllib.parse import urlparse
            
            # 1. Connection Check via /health
            parsed = urlparse(self.api_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            health_url = f"{base_url}/health"
            
            # Timeout fast if connection issues
            resp_health = requests.get(health_url, timeout=2)
            
            if resp_health.status_code == 200:
                status["connection"] = True
                data = resp_health.json()
                if data.get("status") == "healthy" and data.get("artifacts_loaded") is True:
                    status["model"] = True
                else:
                     status["message"] = "Model Not Loaded"
            else:
                status["message"] = f"Backend Error ({resp_health.status_code})"
                return status

            # 2. Auth & Path Check
            # We probe the actual API entry point (e.g. /api/v1/predict)
            # Use POST because GET 405 might bypass Auth dependency.
            # - 401/403 -> Path exists, Auth failed (Bad Key)
            # - 404 -> Path does not exist (Bad URL)
            # - 422 (Unprocessable Entity) -> Auth succeeded, Body invalid (Good!)
            # - 200 -> Auth succeeded (Good!)
            predict_url = f"{self.api_url}/predict"
            # Send empty json to trigger validation error (422) if auth works
            resp_auth = requests.post(predict_url, json={}, headers=self._get_headers(), timeout=2)
            
            if resp_auth.status_code == 404:
                status["message"] = "Invalid API URL Path"
                status["auth"] = False
                return status
            elif resp_auth.status_code in [401, 403]:
                status["message"] = "Authentication Failed (Invalid Key)"
                status["auth"] = False
                return status
            elif resp_auth.status_code in [200, 422]:
                # 422 means we reached the endpoint (Path OK) and passed Auth (Key OK)
                status["auth"] = True
            else:
                # Unexpected status code (e.g. 500)
                status["message"] = f"API Error ({resp_auth.status_code})"
                status["auth"] = False
                return status
            
            # 3. Final Aggregation
            if status["connection"] and status["model"] and status["auth"]:
                status["healthy"] = True
                status["message"] = "System Operational"

        except requests.exceptions.ConnectionError:
            status["message"] = "Connection Refused (Check API URL)"
        except Exception as e:
            status["message"] = f"Error: {str(e)}"
        
        return status

    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send prediction request to DL API.
        Payload should match Patient schema.
        """
        url = f"{self.api_url}/predict"
        try:
            response = requests.post(
                url, 
                json=payload, 
                headers=self._get_headers(), 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            self._handle_error(e)
            return {}
        except requests.ConnectionError:
            st.error("🔌 Connection Error: Could not connect to the DL Inference Server. Please check if the backend is running.")
            return {}
        except requests.Timeout:
            st.error("⏱️ Timeout: The model took too long to respond.")
            return {}
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
            return {}

    def explain(self, payload: Dict[str, Any], top_n: int = 10, plot: bool = False) -> Dict[str, Any]:
        """
        Send explanation request to DL API.
        """
        url = f"{self.api_url}/explain"
        params = {"top_n": top_n, "plot": plot}
        try:
            response = requests.post(
                url, 
                json=payload, 
                params=params, 
                headers=self._get_headers(), 
                timeout=20 # Explain can be slower
            )
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
             self._handle_error(e)
             return {}
        except Exception as e:
            st.error(f"❌ Error fetching explanation: {str(e)}")
            return {}

    def _handle_error(self, e: requests.HTTPError):
        """Parse API error response and display friendly message."""
        try:
            error_data = e.response.json()
            detail = error_data.get("detail", str(e))
            st.error(f"⚠️ API Error ({e.response.status_code}): {detail}")
        except Exception:
            st.error(f"⚠️ API Error ({e.response.status_code}): {str(e)}")

# Singleton instance
api_client = DLClient()
