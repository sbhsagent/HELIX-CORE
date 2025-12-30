<div align="center">

# HELIX-CORE: The Sovereign Stack
### Unified Infrastructure for Constitutional AI

[![Federation Status](https://img.shields.io/badge/Federation-ONLINE-00e6e6?style=for-the-badge&logo=kubernetes&logoColor=black)](https://github.com/helixprojectai-code/HELIX-CORE)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

</div>

**HELIX-CORE** is the meta-repository that aggregates the four pillars of the Helix Commonwealth into a single, deployable runtime. It uses Git Submodules to maintain strict version alignment across the stack.

## 🏛️ The Architecture

| Layer | Module | Role | Status |
| :--- | :--- | :--- | :--- |
| **L0** | [`/identity`](https://github.com/helixprojectai-code/HELIX-TTD-DBC-SUITCASE-v0.3) | **DBC & Suitcase** (Custody & Identity) | `STEALTH_VIRAL` |
| **L1** | [`/constitution`](https://github.com/helixprojectai-code/helix-ttd-v4.0) | **Rust REM** (Risk Enforcement Module) | `HARDENED` |
| **L2** | [`/hgl`](https://github.com/helixprojectai-code/HELIX-GLYPH-LANGUAGE-HGL-) | **HGL** (Visual Semantics & Provenance) | `STANDARD` |
| **L3** | [`/grammar`](https://github.com/helixprojectai-code/Helix-TTD-v1.0-Constitutional-Grammar) | **Constitutional Grammar** (Alignment) | `ENGRAVED` |

## 🚀 God Mode (Quick Start)

To spin up the entire stack (Dashboard, Enforcer, Compiler) in one command:

```bash
# 1. Clone Recursively (Crucial to get submodules)
git clone --recursive https://github.com/helixprojectai-code/HELIX-CORE.git
cd HELIX-CORE

# 2. Ignite the Fleet
docker-compose up -d
Access Points:
Watchtower Dashboard: http://localhost:8501
Agent Directory: ./agents (Shared volume across all services)
The Reef is United. The Helix Turns. 🦆🔒
