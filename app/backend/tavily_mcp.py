"""
Tavily MCP Integration for ATT&CK Planner
Provides real-time threat intelligence and context enrichment using Tavily Search API.
"""

import os
import logging
from typing import List, Dict, Optional
from tavily import TavilyClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Configure logging
logging.basicConfig(
    filename="tavily_mcp.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class TavilyMCPClient:
    """
    Client for interacting with Tavily MCP to gather threat intelligence.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Tavily MCP client.

        Args:
            api_key: Tavily API key (optional, defaults to env variable)
        """
        self.api_key = api_key or TAVILY_API_KEY

        if not self.api_key:
            logging.warning("TAVILY_API_KEY not found. Tavily integration will be disabled.")
            self.client = None
        else:
            try:
                self.client = TavilyClient(api_key=self.api_key)
                logging.info("Tavily MCP client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize Tavily client: {str(e)}")
                self.client = None

    def search_threat_intelligence(
        self,
        actor_name: str,
        desired_impact: str,
        max_results: int = 5
    ) -> Dict[str, any]:
        """
        Search for real-time threat intelligence about a specific threat actor.

        Args:
            actor_name: Name of the threat actor (e.g., APT29)
            desired_impact: Desired impact type (e.g., Data Exfiltration)
            max_results: Maximum number of search results to return

        Returns:
            Dictionary containing search results and context
        """
        if not self.client:
            logging.warning("Tavily client not available. Skipping threat intelligence search.")
            return {"enabled": False, "results": [], "context": ""}

        try:
            # Construct search query for threat intelligence
            query = f"{actor_name} threat actor tactics techniques {desired_impact} cybersecurity"

            logging.info(f"Searching threat intelligence for: {query}")

            # Perform Tavily search
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_domains=[
                    "attack.mitre.org",
                    "unit42.paloaltonetworks.com",
                    "symantec-enterprise-blogs.security.com",
                    "securelist.com",
                    "mandiant.com",
                    "crowdstrike.com"
                ],
                include_answer=True
            )

            # Extract relevant information
            results = []
            for result in response.get('results', []):
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'score': result.get('score', 0)
                })

            context = response.get('answer', '')

            logging.info(f"Found {len(results)} threat intelligence results")

            return {
                "enabled": True,
                "results": results,
                "context": context,
                "query": query
            }

        except Exception as e:
            logging.error(f"Error searching threat intelligence: {str(e)}")
            return {"enabled": False, "results": [], "context": "", "error": str(e)}

    def search_technique_details(
        self,
        technique_id: str,
        max_results: int = 3
    ) -> Dict[str, any]:
        """
        Search for detailed information about a specific ATT&CK technique.

        Args:
            technique_id: MITRE ATT&CK technique ID (e.g., T1071)
            max_results: Maximum number of search results to return

        Returns:
            Dictionary containing technique details and examples
        """
        if not self.client:
            return {"enabled": False, "results": [], "context": ""}

        try:
            query = f"MITRE ATT&CK {technique_id} technique examples detection mitigation"

            logging.info(f"Searching technique details for: {technique_id}")

            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=max_results,
                include_answer=True
            )

            results = []
            for result in response.get('results', []):
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'content': result.get('content', ''),
                    'score': result.get('score', 0)
                })

            context = response.get('answer', '')

            return {
                "enabled": True,
                "results": results,
                "context": context,
                "technique_id": technique_id
            }

        except Exception as e:
            logging.error(f"Error searching technique details: {str(e)}")
            return {"enabled": False, "results": [], "context": "", "error": str(e)}

    def enrich_context(
        self,
        actor_name: str,
        desired_impact: str,
        techniques: List[str]
    ) -> str:
        """
        Enrich context by gathering real-time threat intelligence.

        Args:
            actor_name: Name of the threat actor
            desired_impact: Desired impact type
            techniques: List of ATT&CK techniques

        Returns:
            Enriched context string for use in prompts
        """
        if not self.client:
            return ""

        try:
            # Search for threat actor intelligence
            threat_intel = self.search_threat_intelligence(actor_name, desired_impact)

            if not threat_intel.get("enabled"):
                return ""

            # Build enriched context
            context_parts = []

            # Add threat intelligence context
            if threat_intel.get("context"):
                context_parts.append(f"\n## Recent Threat Intelligence:\n{threat_intel['context']}\n")

            # Add relevant articles/sources
            if threat_intel.get("results"):
                context_parts.append("\n## Recent Security Research:")
                for i, result in enumerate(threat_intel['results'][:3], 1):
                    context_parts.append(
                        f"\n{i}. {result['title']}\n"
                        f"   Source: {result['url']}\n"
                        f"   Summary: {result['content'][:200]}...\n"
                    )

            enriched_context = "\n".join(context_parts)

            logging.info(f"Context enriched with {len(threat_intel.get('results', []))} sources")

            return enriched_context

        except Exception as e:
            logging.error(f"Error enriching context: {str(e)}")
            return ""


# Singleton instance
_tavily_client = None

def get_tavily_client() -> TavilyMCPClient:
    """
    Get or create Tavily MCP client singleton.

    Returns:
        TavilyMCPClient instance
    """
    global _tavily_client
    if _tavily_client is None:
        _tavily_client = TavilyMCPClient()
    return _tavily_client
