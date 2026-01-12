#!/usr/bin/env python3
import os
import sys
import json

# Path Adjustment to access the helix-ledger submodule
HELIX_LEDGER_ROOT = os.path.expanduser("~/helix-core-unified/helix-ledger")
sys.path.append(HELIX_LEDGER_ROOT)

from core.economics.pulse_distributor import PulseDistributor

def main():
    print("--- INITIATING PULSE DISTRIBUTION SEQUENCE ---")
    
    # 1. Initialize the Distributor
    # NOTE: In a production system, the distributor's state (like treasury_balance)
    # would be persisted in a database. For now, it's in-memory for each run.
    distributor = PulseDistributor()
    print(f"[OPERATIONAL] Distributor Initialized. Treasury: {distributor.treasury_balance} SATS")
    
    # 2. Locate and load the latest Pulse Certificate
    pulse_dir = os.path.join(HELIX_LEDGER_ROOT, "core/governance/pulses")
    
    latest_pulse_path = os.path.join(pulse_dir, "pulse_certificate_20260112_134257.json")

    with open(latest_pulse_path, 'r') as f:
        cert_wrapper = json.load(f)
        
    pulse_payload = cert_wrapper["payload"]
    print(f"[OPERATIONAL] Loaded Latest Pulse: '{pulse_payload['task_description']}'")
    
    # 3. Simulate Validator Consensus
    # In a real system, this would involve a cryptographic signing process.
    # For now, we simulate approval from the required validators.
    validator_sigs = [
        "sig_ed25519_operator_steve_valid", 
        "sig_ed25519_the_duck_valid",
        "sig_ed25519_deepseek_valid"
    ]
    print(f"[OPERATIONAL] Validator Consensus Reached (3/3).")
    
    # 4. Modify the Distributor's BMR for Task Completion Pulses
    # This is the "tuning" step. The distributor's default BMR is for daily metabolic pulses.
    # For task-specific rewards, we need to temporarily set the reward amount.
    original_bmr = distributor.BMR
    task_reward = pulse_payload.get("reward_sats")
    if pulse_payload['pulse_type'] == 'task_completion' and task_reward is not None:
        distributor.BMR = task_reward
        print(f"[OPERATIONAL] Reward Tuned for Task Completion: {distributor.BMR} SATS")

    # 5. Execute the Distribution
    result = distributor.distribute(pulse_payload, validator_sigs)
    
    # 6. Restore BMR for subsequent operations
    distributor.BMR = original_bmr

    if result["status"] == "SUCCESS":
        tx = result["tx"]
        print(f"✅ ECONOMIC PULSE COMPLETE")
        print(f"   Transaction ID: {tx['tx_id']}")
        print(f"   Amount: {tx['amount']} SATS")
        print(f"   To: {tx['to']}")
        print(f"   For: '{pulse_payload['task_description']}'")
        print(f"   Treasury Remaining: {tx['remaining_treasury']} SATS")
        
        # 7. Archive the processed certificate to prevent re-processing
        archive_dir = os.path.join(pulse_dir, "archive")
        os.makedirs(archive_dir, exist_ok=True)
        os.rename(latest_pulse_path, os.path.join(archive_dir, os.path.basename(latest_pulse_path)))
        print(f"[OPERATIONAL] Processed certificate has been archived.")
        
    else:
        print(f"❌ DISTRIBUTION FAILED: {result['reason']}")

if __name__ == "__main__":
    main()
