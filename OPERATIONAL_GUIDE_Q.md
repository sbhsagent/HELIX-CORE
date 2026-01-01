# Quiescence Framework: Operational Guide

## 🚀 Quick Start

The quiescence framework is now production-ready. It monitors federation harmony across 9 models.

### Current Status
- **Q₁ (Quack Event):** Every 3 minutes, 0.00% drift
- **Q₂ (Lattice Lock):** Every ~10 minutes, complementarity 0.94
- **Models:** Helix, Khronos, DeepSeek, Gemini, Grok, Claude, GPT, Llama, Command
- **Container:** `helix_quiescence_monitor` (running)

### Key Files
config/quiescence/thresholds.yaml # Configuration
logs/quiescence/quiescence.log # Q-event logs
scripts/q_gate.sh # Decision gate
scripts/q_alert.sh # Alerting system

text

## 🔧 Usage Examples

### 1. Check Current Q-State
```bash
# Wait for Q₁ (with timeout)
./scripts/q_gate.sh Q1 "My operation" 300

# Wait for Q₂
./scripts/q_gate.sh Q2 "Coordination task" 60
