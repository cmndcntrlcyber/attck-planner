#!/usr/bin/env python3
"""
Test script for Tavily MCP integration
Demonstrates real-time threat intelligence gathering capabilities
"""

import os
import sys
from dotenv import load_dotenv

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from backend.tavily_mcp import get_tavily_client

def test_threat_intelligence():
    """Test threat intelligence search"""
    print("=" * 60)
    print("Testing Tavily MCP Integration")
    print("=" * 60)

    # Load environment variables
    load_dotenv()

    # Check if Tavily API key is configured
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        print("\n⚠️  Warning: TAVILY_API_KEY not found in environment")
        print("Please set TAVILY_API_KEY in your .env file")
        print("\nTo get an API key:")
        print("1. Visit https://tavily.com")
        print("2. Sign up for a free account")
        print("3. Copy your API key to .env file\n")
        return

    print("\n✓ Tavily API key found")

    # Initialize Tavily client
    print("\nInitializing Tavily MCP client...")
    tavily_client = get_tavily_client()

    if not tavily_client.client:
        print("✗ Failed to initialize Tavily client")
        return

    print("✓ Tavily MCP client initialized successfully")

    # Test threat intelligence search
    print("\n" + "-" * 60)
    print("Test Case: Searching for APT29 threat intelligence")
    print("-" * 60)

    actor_name = "APT29"
    desired_impact = "Data Exfiltration"

    print(f"\nActor: {actor_name}")
    print(f"Impact: {desired_impact}")
    print("\nSearching...")

    threat_intel = tavily_client.search_threat_intelligence(
        actor_name=actor_name,
        desired_impact=desired_impact,
        max_results=3
    )

    if threat_intel.get("enabled"):
        print(f"\n✓ Search completed successfully")
        print(f"  Found {len(threat_intel.get('results', []))} results")

        # Display context summary
        if threat_intel.get("context"):
            print("\n📊 Threat Intelligence Summary:")
            print("-" * 60)
            print(threat_intel["context"])

        # Display results
        if threat_intel.get("results"):
            print("\n📄 Recent Security Research:")
            print("-" * 60)
            for i, result in enumerate(threat_intel["results"], 1):
                print(f"\n{i}. {result['title']}")
                print(f"   URL: {result['url']}")
                print(f"   Score: {result['score']:.2f}")
                print(f"   Content: {result['content'][:150]}...")

        # Test context enrichment
        print("\n" + "-" * 60)
        print("Test Case: Context Enrichment")
        print("-" * 60)

        techniques = ["T1071 - Application Layer Protocol", "T1059 - Command and Scripting Interpreter"]
        enriched_context = tavily_client.enrich_context(
            actor_name=actor_name,
            desired_impact=desired_impact,
            techniques=techniques
        )

        if enriched_context:
            print("\n✓ Context enrichment successful")
            print(f"  Generated {len(enriched_context)} characters of enriched context")
            print("\n📝 Enriched Context Preview:")
            print("-" * 60)
            print(enriched_context[:500] + "...")
        else:
            print("\n⚠️  Context enrichment returned empty result")
    else:
        print("\n✗ Search failed")
        if "error" in threat_intel:
            print(f"  Error: {threat_intel['error']}")

    print("\n" + "=" * 60)
    print("Tavily MCP Integration Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_threat_intelligence()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
