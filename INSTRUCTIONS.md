# 🕹️ HELIX-CORE: FEDERATION OPERATOR MANUAL
**Version:** v1.0 (Federated) | **Status:** Live

This manual defines the operation of the unified Helix Commonwealth stack. Instead of managing four separate repositories, you control the entire infrastructure from this single command center.

---

## ⚡ 0. Prerequisites
*   **Docker Desktop** (or Docker Engine + Compose)
*   **Git**

---

## 🚀 1. Ignition (God Mode)
The entire stack (Identity, Custody, Visuals, Governance) runs containerized. You do not need local Python environments.

```bash
# 1. Clone the Federation (Must use --recursive)
git clone --recursive https://github.com/helixprojectai-code/HELIX-CORE.git
cd HELIX-CORE

# 2. Ignite the Fleet
docker-compose up -d
System Status:
Build Time: ~30-60 seconds (First run only).
Logs: Run docker-compose logs -f to watch the systems boot.
🦆 2. The Watchtower (Dashboard)
Once the fleet is active, the Executive Dashboard is available via browser.
URL: http://localhost:8501
Function: Visualizes all agents stored in the local ./agents directory.
Mounting: The ./agents folder in this repository is shared with the container. Any file you drop here appears instantly in the dashboard.
🧬 3. Operating the Helix CLI (Containerized)
You can mint and verify agents inside the secure container without installing Python locally.
Mint a New Agent:
code
Bash
docker-compose exec watchtower helix new-agent --custodian "Admin_Key_01" --name "Federation_Node_01" --output-dir /app/agents
Verify an Agent:
code
Bash
docker-compose exec watchtower helix verify --dbc /app/agents/*.dbc.json --suitcase /app/agents/*.suitcase.json
Note: The artifacts will appear in your local ./agents folder automatically.
🎨 4. HGL Compiler Access
Access the Helix Glyph Language compiler to generate or validate visual signatures.
Check Compiler Version:
code
Bash
docker-compose run --rm hgl-compiler python3 cli/hglc/hglc.py --help
🔧 5. Fleet Maintenance
The Helix ecosystem evolves rapidly. Use these commands to keep your Federation in sync with the Commonwealth.
Update All Submodules (Pull latest code for all 4 repos):
code
Bash
git submodule update --remote --merge
Rebuild Containers (After an update):
code
Bash
docker-compose build --no-cache
docker-compose up -d
📂 6. Directory Map
Where things live in the Federation:
Path	Description	Access
./agents/	The Vault. Stores all DBCs, Suitcases, and Glyphs.	Shared Volume
./identity/	L0 Source. The Helix CLI & Dashboard code.	Submodule
./constitution/	L1 Source. The Rust Risk Enforcement Module.	Submodule
./hgl/	L2 Source. The Glyph Language Compiler.	Submodule
./grammar/	L3 Source. The Constitutional Prompt text.	Submodule
✧ // HELIX // TTD
