# 🧬 HELIX-CORE: The Federation Standard

[![Status](https://img.shields.io/badge/Status-Sovereign-00ffcc)](https://github.com/helixprojectai-code/HELIX-CORE)
[![Science](https://img.shields.io/badge/Science-Preregistered-blue)](https://osf.io/vz3mj/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

HELIX-TTD is a sovereign, federated AI control system implementing Semantic Runtime Assurance (SRTA). It enforces a Constitutional Flight Envelope around Large Language Models, replacing stochastic uncertainty with deterministic governance.

---

## 🏛️ The Architecture

| Layer | Module | Role | Status |
| :--- | :--- | :--- | :--- |
| L0 | [/identity](https://github.com/helixprojectai-code/HELIX-TTD-DBC-SUITCASE-v0.3) | DBC & Suitcase (Custody & Identity) | v0.3.2 |
| L1 | [/constitution](https://github.com/helixprojectai-code/helix-ttd-v4.0) | Rust REM (Risk Enforcement Module) | HARDENED |
| L2 | [/hgl](https://github.com/helixprojectai-code/HELIX-GLYPH-LANGUAGE-HGL-) | HGL (Visual Semantics) | STANDARD |
| L3 | [/grammar](https://github.com/helixprojectai-code/Helix-TTD-v1.0-Constitutional-Grammar) | Constitutional Grammar (Alignment) | ENGRAVED |
| L4 | [/helix-ledger](https://github.com/helixprojectai-code/HELIX-LEDGER) | Metabolic Anchor (Grounding & Settlement) | v9.0 STABLE |

---

## 📜 Governance & Doctrine
The Federation operates under ratified bylaws and scientific doctrine.

* [Council Charter:](governance/COUNCIL_CHARTER.md) Quorum rules (3-of-5) and Emergency Powers.
* [Governance Calendar:](governance/CALENDAR.md) Scheduled audits, drills, and rotation cycles.
* [Doctrine 01:](governance/DOCTRINE_01_SHARED_PRIMITIVES.md) The Cartography of Cognition (White Paper).
* [Runtime Spec:](governance/RUNTIME_ASSURANCE_SPEC.md) AFRL-grade Technical Specification.

---

## 🛡️ Security & Hardening ("Glass & Metal")
* Immutable Supply Chain: Base images pinned by SHA256 Digest.
* Rootless Runtime: Services run as UID 1000.
* Read-Only Filesystem: The Watchtower cannot mutate the ledger.
* Air-Gapped Networking: Internal bridge network only.

## 🚀 Ignition (God Mode)
The fleet runs in Hardened Production Mode by default.

# 1. Clone Recursively
git clone --recursive https://github.com/helixprojectai-code/HELIX-CORE.git
cd HELIX-CORE

# 2. Ignite Watchtower
./ignite.sh

## 🔬 Scientific Validation
Principal Investigator: Stephen Hope (ORCID: 0009-0000-7367-248X)
