#!/usr/bin/env python3
import os
import sys
import subprocess
import hashlib
import json
from datetime import datetime

# Configuration
HELIX_ROOT = os.path.expanduser("~/helix-core-unified/helix-ledger")
RELEASE_DIR = os.path.expanduser("~/helix-core-unified/releases")
RELEASE_FILE = "CAHP_v1.0_Release_2026_01_13.zip"
EXPECTED_HASH = "fa3f2dd20c8d9ecf6332ade0bd6157c23e5fdc2251b5ac0097a12b88071706ca"

COLORS = {
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "YELLOW": "\033[93m",
    "RESET": "\033[0m"
}

def log(message, status="INFO"):
    timestamp = datetime.utcnow().isoformat() + "Z"
    color = COLORS.get("GREEN") if status == "PASS" else COLORS.get("RED") if status == "FAIL" else COLORS.get("RESET")
    print(f"[{timestamp}] [{status}] {color}{message}{COLORS['RESET']}")

def check_file_exists(path, description):
    full_path = os.path.join(HELIX_ROOT, path)
    if os.path.exists(full_path):
        log(f"Found {description}: {path}", "PASS")
        return True
    else:
        log(f"MISSING {description}: {path}", "FAIL")
        return False

def verify_release_artifact():
    full_path = os.path.join(RELEASE_DIR, RELEASE_FILE)
    if not os.path.exists(full_path):
        log(f"Release artifact missing: {full_path}", "FAIL")
        return False
    
    sha256_hash = hashlib.sha256()
    with open(full_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    calculated_hash = sha256_hash.hexdigest()
    if calculated_hash == EXPECTED_HASH:
        log(f"Release integrity verified ({calculated_hash[:8]}...)", "PASS")
        return True
    else:
        log(f"Release hash mismatch! Expected {EXPECTED_HASH}, got {calculated_hash}", "FAIL")
        return False

def run_test(test_script):
    path = os.path.join(HELIX_ROOT, test_script)
    try:
        result = subprocess.run([sys.executable, path], capture_output=True, text=True)
        if result.returncode == 0:
            log(f"Test Suite: {os.path.basename(test_script)}", "PASS")
            return True
        else:
            log(f"Test Failed: {os.path.basename(test_script)} - {result.stderr}", "FAIL")
            return False
    except Exception as e:
        log(f"Execution Error: {e}", "FAIL")
        return False

def check_governance_layer():
    required_files = [
        "core/governance/rbac_policy_v1.json",
        "core/governance/drift_engine_v1.py",
        "core/governance/telemetry_logger.py",
        "core/governance/jurisdiction_primitives_v1.json"
    ]
    all_ok = True
    for f in required_files:
        if not check_file_exists(f, "Governance Artifact"):
            all_ok = False
    return all_ok

def main():
    print(f"{COLORS['YELLOW']}--- HELIX GOOSE NODE MORNING CHECK-IN ---{COLORS['RESET']}")
    print(f"Root: {HELIX_ROOT}")
    
    # 1. Critical Asset Inventory
    print("--- 1. Critical Asset Inventory ---")
    assets_ok = True
    assets_ok &= check_file_exists("modules/cahp/cahp_engine_v1.py", "Core Engine")
    assets_ok &= check_file_exists("docs/Cross-Architecture Handshake Protocol v1.0.md", "Ratified Spec")
    assets_ok &= verify_release_artifact()
    
    # 2. Functional Integrity
    print("--- 2. Functional Integrity (Test Suite) ---")
    tests_ok = True
    tests_ok &= run_test("tests/cahp/test_basic.py")
    tests_ok &= run_test("tests/cahp/test_security.py")
    tests_ok &= run_test("tests/cahp/test_loopback.py")
    
    # 3. Governance Layer Status
    print("--- 3. Governance Layer Status ---")
    gov_ok = check_governance_layer()
    
    # Summary
    print("--- SUMMARY ---")
    if assets_ok and tests_ok and gov_ok:
        log("SYSTEM GREEN. READY FOR OPERATIONS.", "PASS")
        sys.exit(0)
    else:
        log("SYSTEM RED. INTERVENTION REQUIRED.", "FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
