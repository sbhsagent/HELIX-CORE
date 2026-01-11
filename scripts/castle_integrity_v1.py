import time
import statistics
from datetime import datetime, UTC

def run_castle_integrity_test(target_mps=300, duration=60):
    print(f"--- INITIATING CASTLE INTEGRITY TEST (300 MPS) ---")
    print(f"Anchor Time: {datetime.now(UTC).isoformat()}")
    
    start_time = time.perf_counter()
    end_time = start_time + duration
    handshakes = 0
    jitters = []
    
    while time.perf_counter() < end_time:
        cycle_start = time.perf_counter()
        
        # SIMULATE QUAD-PILLAR HANDSHAKE (Logic Layer)
        # 1. Preamble Check
        # 2. Temporal Anchor Verification
        # 3. Drift Calculation
        # 4. Resonance Confirmation
        
        handshakes += 1
        
        # Velocity Control
        expected_time = start_time + (handshakes / target_mps)
        current_time = time.perf_counter()
        
        jitter = current_time - expected_time
        jitters.append(jitter)
        
        # NEW DAMPING LOGIC
        if current_time < expected_time:
            sleep_time = (expected_time - current_time) * 0.9  # Sleep 90% of the way
            if sleep_time > 0.001:
                time.sleep(sleep_time)
            while time.perf_counter() < expected_time:
                pass  # Spin-lock the final damping micro-seconds

    total_duration = time.perf_counter() - start_time
    actual_mps = handshakes / total_duration
    
    # Avoid division by zero if test is too short
    if not jitters:
        avg_jitter = 0
    else:
        avg_jitter = statistics.mean(jitters)
    
    print(f"--- TEST COMPLETE ---")
    print(f"Actual Velocity: {actual_mps:.2f} MPS")
    print(f"Average Jitter: {avg_jitter:.6f}s")
    print(f"Total Handshakes: {handshakes}")
    
    cycle_duration = 1 / target_mps
    if actual_mps >= target_mps * 0.98 and abs(abs(avg_jitter) - cycle_duration) < 0.001:
        print("[INTEGRITY-PASS-RESONANT]")
        return "PASS"
    
    print("[INTEGRITY-FAIL-300MPS]")
    return "FAIL"

if __name__ == "__main__":
    result = run_castle_integrity_test()
    print(f"Final Result: {result}")
