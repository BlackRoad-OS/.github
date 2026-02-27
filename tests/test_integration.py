#!/usr/bin/env python3
"""
Integration test: Simulate the complete sync flow
Tests the end-to-end process without actually dispatching
"""

import json
import yaml
from pathlib import Path


def test_integration():
    """Test complete sync integration flow"""
    
    print("🔄 Running integration test...\n")
    
    # Step 1: Load registry
    print("1️⃣  Loading registry...")
    registry_path = Path(__file__).parent.parent / "routes/registry.yaml"
    with open(registry_path) as f:
        registry = yaml.safe_load(f)
    
    active_orgs = [code for code, org in registry["orgs"].items() if org.get("status") == "active"]
    print(f"   ✓ Loaded {len(registry['orgs'])} orgs, {len(active_orgs)} active")
    
    # Step 2: Check workflows exist
    print("\n2️⃣  Checking workflows...")
    workflows_dir = Path(__file__).parent.parent / ".github/workflows"
    
    required_workflows = ["sync-to-orgs.yml", "auto-merge.yml", "ci.yml"]
    for wf in required_workflows:
        wf_path = workflows_dir / wf
        assert wf_path.exists(), f"Missing {wf}"
        
        with open(wf_path) as f:
            data = yaml.safe_load(f)
            assert data is not None, f"Invalid YAML in {wf}"
        
        print(f"   ✓ {wf}")
    
    # Step 3: Simulate dispatch payload
    print("\n3️⃣  Simulating dispatch payload...")
    for code in active_orgs:
        org = registry["orgs"][code]
        
        for repo in org.get("repos", []):
            payload = {
                "event_type": "sync_from_bridge",
                "client_payload": {
                    "source": "BlackRoad-OS/.github",
                    "ref": "main",
                    # Fixed historical timestamp used only for deterministic test payload logging
                    "timestamp": "2026-01-27T20:00:00Z"
                }
            }
            print(f"   ✓ Would dispatch to {code}/{repo['name']}")
            print(f"     Payload: {json.dumps(payload, indent=8)}")
    
    # Step 4: Check test infrastructure
    print("\n4️⃣  Checking test infrastructure...")
    test_file = Path(__file__).parent / "test_sync.py"
    assert test_file.exists(), "test_sync.py not found"
    print(f"   ✓ test_sync.py exists")
    
    # Step 5: Check documentation
    print("\n5️⃣  Checking documentation...")
    docs = [
        Path(__file__).parent.parent / "docs/SYNC.md",
        Path(__file__).parent.parent / "README.md",
    ]
    for doc in docs:
        assert doc.exists(), f"Missing {doc.name}"
        print(f"   ✓ {doc.name}")
    
    # Step 6: Check templates
    print("\n6️⃣  Checking templates...")
    template = Path(__file__).parent.parent / "templates/workflows/sync-receiver.yml"
    assert template.exists(), "sync-receiver.yml template not found"
    
    with open(template) as f:
        data = yaml.safe_load(f)
        # Check for repository_dispatch trigger
        triggers = data.get(True, data.get("on", {}))
        assert "repository_dispatch" in triggers, "Missing repository_dispatch trigger"
    
    print(f"   ✓ sync-receiver.yml template")
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ Integration test PASSED!")
    print("\nReady to:")
    print("  1. Push to main → triggers sync-to-orgs.yml")
    print("  2. Dispatches to active org repos")
    print("  3. Target repos receive sync_from_bridge event")
    print("  4. PR auto-merges after approval + CI")
    print("\n💡 To test manually:")
    print("  gh workflow run sync-to-orgs.yml -f dry_run=true")


if __name__ == "__main__":
    test_integration()
