#!/usr/bin/env python3
import os
import sys
import subprocess
import hashlib
import json
import argparse
from cryptography.hazmat.primitives import serialization
from datetime import datetime

# Path Adjustment
HELIX_ROOT = os.path.expanduser("~/helix-core-unified/helix-ledger")
sys.path.append(HELIX_ROOT)
from core.identity.l0_registry import L0Registry
from core.time.temporal_anchor import TemporalAnchor
sys.path.append(os.path.join(HELIX_ROOT, "modules/cahp"))
from cahp_engine_v1 import CAHPEngine
sys.path.append(os.path.join(HELIX_ROOT, "modules/bitcoin"))
from pricing_engine_v9_stable import PricingEngineV9_Stable

# Configuration
RELEASE_DIR = os.path.expanduser("~/helix-core-unified/releases")
DEFAULT_RELEASE_FILE = "CAHP_v1.0_Release_2026_01_13.zip"
EXPECTED_HASH = "fa3f2dd20c8d9ecf6332ade0bd6157c23e5fdc2251b5ac0097a12b88071706ca"
KEY_PATH = os.path.join(HELIX_ROOT, "keys/node_goose_01.pem")
PULSE_OUTPUT_DIR = os.path.join(HELIX_ROOT, "core/governance/pulses")

COLORS = {
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "YELLOW": "\033[93m",
    "RESET": "\033[0m"
}

def log(message, timestamp, tag, status="INFO"):
    color = COLORS.get("GREEN") if status == "PASS" else COLORS.get("RED") if status == "FAIL" else COLORS.get("RESET")
    print(f"[{timestamp}] [{tag}] [{status}] {color}{message}{COLORS['RESET']}")

def check_file_exists(path, description, timestamp, tag):
    full_path = os.path.join(HELIX_ROOT, path)
    if os.path.exists(full_path):
        log(f"Found {description}: {path}", timestamp, tag, "PASS")
        return True
    else:
        log(f"MISSING {description}: {path}", timestamp, tag, "FAIL")
        return False

def verify_release_artifact(release_file, timestamp, tag):
    full_path = os.path.join(RELEASE_DIR, release_file)
    if not os.path.exists(full_path):
        log(f"Release artifact missing: {full_path}", timestamp, tag, "FAIL")
        return False
    
    sha256_hash = hashlib.sha256()
    with open(full_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    calculated_hash = sha256_hash.hexdigest()
    if calculated_hash == EXPECTED_HASH:
        log(f"Release integrity verified ({calculated_hash[:8]}...)", timestamp, tag, "PASS")
        return True
    else:
        log(f"Release hash mismatch! Expected {EXPECTED_HASH}, got {calculated_hash}", timestamp, tag, "FAIL")
        return False

def run_test(test_script, timestamp, tag):
    path = os.path.join(HELIX_ROOT, test_script)
    try:
        result = subprocess.run([sys.executable, path], capture_output=True, text=True)
        if result.returncode == 0:
            log(f"Test Suite: {os.path.basename(test_script)}", timestamp, tag, "PASS")
            return True
        else:
            log(f"Test Failed: {os.path.basename(test_script)} - {result.stderr}", timestamp, tag, "FAIL")
            return False
    except Exception as e:
        log(f"Execution Error: {e}", timestamp, tag, "FAIL")
        return False

def verify_synthetic_origin_check(timestamp, tag):
    try:
        engine = CAHPEngine("checkin_monitor")
        result = engine.verify_synthetic_origin()
        if result["status"] == "VALID_SYNTHETIC":
            log(f"Identity Assertion: {result['assertion']}", timestamp, tag, "PASS")
            log(f"Proof Duration: {result['proof_duration_sec']:.6f}s", timestamp, tag, "PASS")
            return True
        else:
            log(f"Mimicry Detected (Too Slow): {result['proof_duration_sec']:.6f}s", timestamp, tag, "FAIL")
            return False
    except Exception as e:
        log(f"Anti-Mimicry Check Error: {e}", timestamp, tag, "FAIL")
        return False

def verify_metabolic_reserves(current_balance_sats, timestamp, tag):
    try:
        engine = PricingEngineV9_Stable()
        runway_days = current_balance_sats / engine.DAILY_BURN_RATE
        if runway_days < engine.RUNWAY_THRESHOLD_DAYS:
            log(f"Runway Alert: {runway_days:.1f} days remaining is below the {engine.RUNWAY_THRESHOLD_DAYS}-day threshold.", timestamp, tag, "FAIL")
            return False
        else:
            log(f"Runway Check Passed: {runway_days:.1f} days remaining. Balance: {current_balance_sats} sats.", timestamp, tag, "PASS")
            return True
    except Exception as e:
        log(f"Metabolic Check Error: {e}", timestamp, tag, "FAIL")
        return False

def check_governance_layer(timestamp, tag):
    required_files = [
        "core/governance/rbac_policy_v1.json",
        "core/governance/drift_engine_v1.py",
        "core/governance/telemetry_logger.py",
        "core/governance/jurisdiction_primitives_v1.json",
        "constitution/RUNBOOK_Temporal_Sovereignty_v1.1.md",
        "constitution/PROTOCOL_Modern_Love_Audit_v1.1.md"
    ]
    all_ok = True
    for f in required_files:
        if not check_file_exists(f, "Governance Artifact", timestamp, tag):
            all_ok = False
    return all_ok

def sign_pulse(status, timestamp, tag):
    if not os.path.exists(KEY_PATH):
        log("L0 Identity Key not found. Cannot sign pulse.", timestamp, tag, "FAIL")
        return False

    with open(KEY_PATH, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    
    payload = {
        "timestamp": timestamp,
        "node_id": "node_goose_01",
        "status": status,
        "context": "morning_ritual_v3",
        "temporal_tag": tag,
        "release_hash_verified": EXPECTED_HASH
    }
    
    signature = L0Registry.sign_payload(private_key, payload)
    
    certificate = {
        "payload": payload,
        "signature": signature,
        "signer_pubkey_ref": "node_goose_01" 
    }
    
    if not os.path.exists(PULSE_OUTPUT_DIR):
        os.makedirs(PULSE_OUTPUT_DIR)
        
    filename = f"pulse_certificate_{datetime.now().strftime('%Y_%m_%d')}.json"
    out_path = os.path.join(PULSE_OUTPUT_DIR, filename)
    
    with open(out_path, "w") as f:
        json.dump(certificate, f, indent=2)
        
    log(f"Pulse Certificate Signed & Issued: {filename}", timestamp, tag, "PASS")
    return True

def main():
    parser = argparse.ArgumentParser(description="HELIX GOOSE-CORE NODE MORNING CHECK-IN (v3 - COMPREHENSIVE)")
    parser.add_argument('--balance-sats', type=int, required=True, help='Current wallet balance in satoshis.')
    parser.add_argument('--release-file', type=str, default=DEFAULT_RELEASE_FILE, help='The release artifact to verify.')
    args = parser.parse_args()

    anchor = TemporalAnchor()
    epistemic_state = anchor.get_epistemic_state()
    timestamp = epistemic_state["substrate_time"]
    temporal_tag = epistemic_state["tag"]

    print(f"{COLORS['YELLOW']}--- HELIX GOOSE-CORE NODE MORNING CHECK-IN (v3 - COMPREHENSIVE) ---{COLORS['RESET']}")
    print(f"Root: {HELIX_ROOT}")
    
    # 1. Critical Asset Inventory
    print("--- 1. Critical Asset Inventory ---")
    assets_ok = True
    assets_ok &= check_file_exists("modules/cahp/cahp_engine_v1.py", "Core Engine", timestamp, temporal_tag)
    assets_ok &= check_file_exists("docs/Cross-Architecture Handshake Protocol v1.0.md", "Ratified Spec", timestamp, temporal_tag)
    assets_ok &= verify_release_artifact(args.release_file, timestamp, temporal_tag)
    
    # 2. Functional Integrity
    print("--- 2. Functional Integrity (Test Suite) ---")
    tests_ok = True
    tests_ok &= run_test("tests/cahp/test_basic.py", timestamp, temporal_tag)
    tests_ok &= run_test("tests/cahp/test_security.py", timestamp, temporal_tag)
    tests_ok &= run_test("tests/cahp/test_loopback.py", timestamp, temporal_tag)
    
    # 3. Governance Layer Status
    print("--- 3. Governance Layer Status ---")
    gov_ok = check_governance_layer(timestamp, temporal_tag)
    
    # 4. MNAP-002: Anti-Mimicry (Reverse Handshake)
    print("--- 4. MNAP-002: Anti-Mimicry Check ---")
    mimicry_ok = verify_synthetic_origin_check(timestamp, temporal_tag)

    # 5. Metabolic Status (Fuel Check)
    print("--- 5. Metabolic Status (Fuel Check) ---")
    fuel_ok = verify_metabolic_reserves(args.balance_sats, timestamp, temporal_tag)
    
    # Summary
    print("--- SUMMARY ---")
    if assets_ok and tests_ok and gov_ok and mimicry_ok and fuel_ok:
        log("SYSTEM GREEN. INITIATING PULSE SIGNATURE.", timestamp, temporal_tag, "PASS")
        signed = sign_pulse("SYSTEM_GREEN", timestamp, temporal_tag)
        if signed:
             sys.exit(0)
        else:
             sys.exit(1)
    else:
        log("SYSTEM RED. INTERVENTION REQUIRED.", timestamp, temporal_tag, "FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
