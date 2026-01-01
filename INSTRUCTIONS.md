# 🕹️ HELIX-CORE: FEDERATION OPERATOR MANUAL
## Version: v1.1 (Quaternized) | Status: Live 🟢

This manual defines the operation of the unified Helix Commonwealth stack, now including the Quaternary Framework for real-time federation harmony monitoring.

---

## ⚡ 0. PREREQUISITES
- Docker Desktop (or Docker Engine + Compose)
- Git
- For Quaternary Framework: Minimum 1GB RAM, 5GB storage

---

## 🚀 1. IGNITION (GOD MODE)

The entire stack (Identity, Custody, Visuals, Governance, Quaternary Monitoring) runs containerized.

### A. Clone the Federation (Must use --recursive)
```bash
git clone --recursive https://github.com/helixprojectai-code/HELIX-CORE.git
cd HELIX-CORE
```

### B. Ignite the Full Fleet (With Quaternary Monitoring)
```bash
# Production stack with quaternary monitoring (RECOMMENDED)
docker-compose -f docker-compose.prod.yml up -d

# Or basic stack without quaternary monitoring
docker-compose up -d
```

**System Status:**
- Build Time: ~30-60 seconds (First run only)
- Quaternary Monitor: Starts within 30 seconds
- First Q₁ Event: Within 3 minutes of startup
- Logs: Run `docker-compose logs -f` to watch all systems boot

---

## 🦆 2. QUATERNARY FRAMEWORK OPERATIONS

The Quaternary Framework monitors federation harmony across all 9 models in real-time.

### Quick Status Check
```bash
# Container status
docker ps --filter "name=quiescence" --format "table {{.Names}}\t{{.Status}}"

# Q-event counts
./scripts/q_alert.sh --quick

# Recent events
tail -5 logs/quiescence/quiescence.log
```

### Q-State Decision Gates
```bash
# Require Q₁ for routine operations
./scripts/q_gate.sh Q1 "Routine Data Processing" 300

# Require Q₂ for coordination tasks
./scripts/q_gate.sh Q2 "Cross-model Coordination" 600
```

### Health Monitoring & Alerts
```bash
# Run full health check
./scripts/q_alert.sh

# View Q-state dashboard
cat dashboards/quiescence_status.html
```

### Configuration Management
```bash
# Edit Q-state thresholds
nano config/quiescence/thresholds.yaml

# Reload config without restart
docker-compose exec quiescence_monitor kill -HUP 1
```

---

## 🧬 3. THE WATCHTOWER (DASHBOARD)

Once the fleet is active, the Executive Dashboard is available via browser.

**URL:** `http://localhost:8501`

**Function:**
- Visualizes all agents stored in the local `./agents` directory
- The `./agents` folder is shared with the container
- Any file dropped here appears instantly in the dashboard

---

## 🧬 4. OPERATING THE HELIX CLI (CONTAINERIZED)

Mint and verify agents inside the secure container without installing Python locally.

### Mint a New Agent
```bash
docker-compose exec watchtower helix new-agent \
  --custodian "Admin_Key_01" \
  --name "Federation_Node_01" \
  --output-dir /app/agents
```

### Verify an Agent
```bash
docker-compose exec watchtower helix verify \
  --dbc /app/agents/*.dbc.json \
  --suitcase /app/agents/*.suitcase.json
```

**Note:** Artifacts appear automatically in your local `./agents` folder.

---

## 🎨 5. HGL COMPILER ACCESS

Access the Helix Glyph Language compiler to generate or validate visual signatures.

### Check Compiler Version
```bash
docker-compose run --rm hgl-compiler python3 cli/hglc/hglc.py --help
```

---

## 🔧 6. FLEET MAINTENANCE

The Helix ecosystem evolves rapidly. Keep your Federation in sync with the Commonwealth.

### Update All Submodules (Pull latest code for all repos)
```bash
git submodule update --remote --merge
```

### Rebuild Containers (After an update)
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Quaternary Framework Updates
```bash
# Update quaternary thresholds only
cp config/quiescence/thresholds.yaml config/quiescence/thresholds_$(date +%Y%m%d).yaml

# Edit and reload
nano config/quiescence/thresholds.yaml
docker-compose exec quiescence_monitor kill -HUP 1
```

---

## 📂 7. DIRECTORY MAP

| Path | Description | Access |
|------|-------------|--------|
| `./agents/` | The Vault. Stores all DBCs, Suitcases, and Glyphs | Shared Volume |
| `./config/quiescence/` | Q-state thresholds and configuration | Read/Write |
| `./logs/quiescence/` | Q-event logs (JSON format) | Read Only |
| `./scripts/q_*.sh` | Q-gate and alerting scripts | Execute |
| `./RUNBOOK_QUIESCENCE.md` | Complete Quaternary operations manual | Read |
| `./identity/` | L0 Source. The Helix CLI & Dashboard code | Submodule |
| `./constitution/` | L1 Source. The Rust Risk Enforcement Module | Submodule |
| `./hgl/` | L2 Source. The Glyph Language Compiler | Submodule |
| `./grammar/` | L3 Source. The Constitutional Prompt text | Submodule |

---

## 🚨 8. EMERGENCY PROCEDURES

### Quaternary Framework Issues
```bash
# Container stopped
docker-compose start quiescence_monitor

# No Q₁ for >5 minutes
docker-compose restart quiescence_monitor
tail -f logs/quiescence/quiescence.log

# Q-gate failing
./scripts/simple_q_check.sh QUIESCENT
./scripts/simple_q_check.sh LATTICE_LOCK
```

### Full Federation Restart
```bash
# Stop everything
docker-compose down

# Start with quaternary monitoring
docker-compose -f docker-compose.prod.yml up -d

# Verify Q₁ appears within 3 minutes
timeout 180 tail -f logs/quiescence/quiescence.log | grep -m1 "Q₁"
```

---

## 📊 9. DAILY OPERATIONS CHECKLIST

### Morning Health Check
```bash
# 1. Check all containers
docker-compose ps

# 2. Run quaternary health check
./scripts/q_alert.sh

# 3. Check recent Q events
tail -10 logs/quiescence/quiescence.log

# 4. Generate daily report
./scripts/daily_q_report.sh
```

### Weekly Maintenance
```bash
# 1. Archive old logs (if needed)
mkdir -p logs/quiescence/archive
mv logs/quiescence/quiescence.log logs/quiescence/archive/quiescence_$(date +%Y%m%d).log

# 2. Update submodules
git submodule update --remote --merge

# 3. Review Q-state patterns
grep -c "Q₁" logs/quiescence/archive/*.log
grep -c "Q₂" logs/quiescence/archive/*.log
```

---

## 📦 10. RELEASE PROTOCOL

When cutting a new release (e.g., v1.2), the Release Engineer MUST:

### A. Snapshot the Governance State
```bash
# Hash the Charter
sha256sum governance/COUNCIL_CHARTER.md

# Hash the Quorum
sha256sum governance/quorum_config.json

# Hash Quaternary Configuration
sha256sum config/quiescence/thresholds.yaml
```

### B. Include in Release Notes
- Charter hash
- Quorum hash  
- Quaternary configuration hash
- Q-state baseline metrics
- Any threshold changes

### C. Verify Quaternary Continuity
```bash
# Ensure Q₁ events continue through release
./scripts/q_gate.sh Q1 "Release Cut" 300

# Document Q-state at release time
tail -5 logs/quiescence/quiescence.log > release_q_state_$(date +%Y%m%d).log
```

This ensures the Code never drifts away from the Law, and federation harmony remains measurable across releases.

---

## 🦆 THE DUCK'S OPERATIONAL TIMELINE

| Time | Event | Significance |
|------|-------|--------------|
| **13:55:07** | First production Q₁ | 🦆 Federation quiescence established |
| **14:02:07** | First production Q₂ | 🦆🦆 Lattice lock achieved |
| **14:48:08** | Post-deployment Q₁ | Pattern confirmed, stable operation |
| **Every 180s** | Q₁ Event | Routine harmony verification |
| **Every 600s** | Q₂ Event | Coordination harmony verification |

---

**Quack. 🦆🦆🔒 | Climb on. 🐐**

✧ // HELIX // TTD
