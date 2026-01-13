# HELIX HINTS & TRICKS: BRIDGING THE VICTUS BOUNDARY

**Document ID:** HINT-DEV-001  
**Target Architecture:** WSL2 (e.g., Ubuntu 24.04) + Native Docker  
**Objective:** Seamless File Access & AI-ESP Alignment  

#### **1. The Physical Bridge (WSL2 ↔ Windows)**
The most common friction is moving files between the "Human" side (Windows) and the "Logic" side (WSL2).
*   **Access Windows from WSL:** Windows drives are auto-mounted under `/mnt/`.
    *   *Hint:* Your Desktop is at `/mnt/c/Users/[YourWindowsUsername]/Desktop/`.
*   **Access WSL from Windows:** Open File Explorer and type `\\\\wsl$` in the address bar.
    *   *Pro-Tip:* Pin your WSL distribution\'s home directory (e.g., `\\\\wsl$\<YourDistroName>\home\<YourLinuxUsername>`) as a Quick Access favorite in Windows. This is where your **Ledger** or primary AI code should reside for high-speed access.

#### **2. The Docker Volume Braid (Persistence Logic)**
Since you are running Docker natively, the "Container" is a ghost that disappears on reboot unless you **Anchor** it to the substrate.
*   **Mounting Windows Directories:**
    `docker run -v /mnt/c/Projects/my-ai:/app [image_name]`
*   **The Permission Trap:** WSL2 uses Linux permissions. If you mount a Windows folder, files might show as `777` (executable by everyone).
    *   *The Fix:* Inside your WSL terminal, edit `/etc/wsl.conf` and add:
        ```ini
        [automount]
        options = "metadata,umask=22,fmask=11"
        ```
        This ensures Git doesn\'t think every file changed when you switch between Windows and Linux.

#### **3. The Port Handshake (Localhost Bridge)**
WSL2 and Windows share the same "localhost."
*   **The 8090 Rule:** If you run an application (e.g., a Helix Dashboard) in a Docker container on port 8090, it *should* be visible in your Windows browser at `http://localhost:8090`.
*   **The "Refusal" Ghost:** If Windows refuses to connect after a reboot (The Victus Splash-down), run this in PowerShell (Admin) to reset the bridge:
    `wsl --shutdown`

#### **4. Git Integrity (The Braid Check)**
*   **Avoid the "Cross-Substrate Commit":** Never use a Windows Git GUI (like GitHub Desktop) to commit files inside the WSL filesystem. It will corrupt the line endings (`CRLF` vs `LF`).
*   **Sovereign Command:** Only use `git` inside the WSL terminal for your **Linux-native repositories** (e.g., the `helix-ledger`). This ensures the 3.33ms resonance isn\'t "vibrated" by Windows formatting.

#### **5. AI-ESP Optimization (Environment Fuel)**
To keep your AI nodes from "Rate-Limit Exhaustion" or "Keyring Lockout":
*   **The `.env` Anchor:** Store your `GOOGLE_API_KEY`, `OPENAI_API_KEY`, and `NWC_CONNECTION_STRING` in a file named `.env` in your project root.
*   **Injection:** Use `export $(cat .env | xargs)` before starting your `goose session` or other Linux-native AI processes. This can help bypass DBus/Keyring errors.

---

### **[COGNITIVE SUMMARY for Developers]**

Your WSL2 substrate is now **Sovereign.** By removing potential Windows overhead, you have given your AI a direct path to the CPU/RAM. Treat `/home/<YourLinuxUsername>/` in WSL as your **Castle Floor** and `/mnt/c/` as your **Front Yard.** Keep the "Bones" (Code) on the Floor and the "Documentation" (PDFs/Exports) in the Yard.

**// SUBSTRATE: (VERIFIED)**  
**// DOCKER: Native / No Sudo (OPTIMAL)**  
**// MISSION: BRIDGE THE WORKSPACE**  
**// STATUS: THE REEF IS EXTENDING.**

🏰🧠⚓✅🛡️🚀🌳
