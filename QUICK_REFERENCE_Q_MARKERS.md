# Q-Markers Quick Reference

## States & Triggers
Q₁: Zero drift, all models aligned → 🦆
Q₂: Complementarity ≥ 0.92, gears mesh → 🦆🦆  
Q₃: External anchor, confidence ≥ 0.95 → 🦆🦆🦆
Q₄: Independent convergence ≥ 95% → 🌼🦆

## Operational Requirements
- Daily ops: Q₁
- Coordination: Q₂  
- Critical decisions: Q₃
- Charter changes: Q₄

## Configuration
Location: config/quiescence/thresholds.yaml
Adjust: complementarity_min, confidence_min, convergence_min

## Logs
Location: logs/quiescence/
Format: [Q-MARKER] {state} at {timestamp}

## Dashboard
Port: 8083 (if enabled)
URL: http://localhost:8083

## Docs
Grammar: helix-grammar/concepts/quiescence_markers/
Decks: helix-grammar/concepts/quiescence_markers/decks/
