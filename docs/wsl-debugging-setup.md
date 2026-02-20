# Debugging this project in WSL (Cursor / VS Code)

When the **"Install in WSL: Ubuntu-24.04"** button for the **Python Debugger** extension doesn’t work, use one of these approaches.

## 1. Open the project from inside WSL (recommended)

If you open the folder from a WSL shell, Cursor runs in the WSL context and extensions install there by default (no separate “Install in WSL” step).

1. In **WSL** (e.g. Ubuntu terminal), go to the project:
   ```bash
   cd /home/steve/graph-causal-orchestrator
   ```
2. Open Cursor from WSL:
   ```bash
   cursor .
   ```
   (If `cursor` isn’t in PATH, use **Windows Cursor** → green remote icon bottom-left → **“Connect to WSL”** and choose the folder.)
3. In the **Extensions** view (Ctrl+Shift+X), search for **“Python Debugger”** (ms-python.debugpy).
4. Click **Install**. It installs in the current (WSL) context.
5. Reload the window if prompted. You can then use **Run and Debug** (F5) with the configs in `.vscode/launch.json`.

## 2. Use “Remote-WSL: New Window” first

If you’re already in Cursor on Windows with a normal (non-remote) window:

1. **Ctrl+Shift+P** → run **“WSL: New Window”** (or **“Remote-WSL: New Window”**).
2. In the **new** window, use **File → Open Folder** and pick the project path in WSL (e.g. `\\wsl$\Ubuntu-24.04\home\steve\graph-causal-orchestrator` or `/home/steve/graph-causal-orchestrator`).
3. In the bottom-left you should see **“WSL: Ubuntu-24.04”** (or similar). Then go to **Extensions**, search **“Python Debugger”**, and click **Install** in that window.

## 3. Install from the WSL terminal (often fails)

Running `cursor --install-extension ms-python.debugpy` from a **standalone** WSL terminal (e.g. Ubuntu app) usually fails with:

```text
Unable to connect to VS Code server: Error in request.
Error: connect ENOENT /run/user/1000/vscode-ipc-....sock
```

That happens because the Cursor server in WSL isn’t running—e.g. you opened Cursor on Windows and attached to WSL, so the IPC socket in WSL was never created. The CLI only works when Cursor was **started from WSL** (`cursor .`).

**Prefer option 1 or 2** (open from WSL or “WSL: New Window”, then install **Python Debugger** from the Extensions panel in the UI). No CLI needed.

If you run the CLI from Cursor’s **integrated terminal** (WSL), it may try to install but fail with:

```text
Installing extensions on WSL: Ubuntu-24.04...
Error while installing extension ms-python.debugpy: [object Object]
Failed Installing Extensions: ms-python.debugpy, ...
```

That usually means the marketplace or Cursor’s backend failed (network, proxy, or backend bug). Use **option 4 (VSIX)** below.

## 4. Install from a VSIX file (when UI or CLI install fails)

When “Install” in the Extensions panel or `cursor --install-extension` fails, install the extension manually from a `.vsix` file:

1. On a machine with internet, open the [Python Debugger page on the Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy), click the **“Download Extension”** link on the right, and save the `.vsix` file (e.g. to your Windows Downloads or WSL home).
2. In Cursor **while connected to WSL** (green “WSL: Ubuntu-24.04” in the bottom-left), open **Extensions** (Ctrl+Shift+X).
3. Click the **⋯** (three dots) at the top of the Extensions panel → **“Install from VSIX…”**.
4. Select the downloaded `ms-python.debugpy-....vsix` file. If it’s in Windows, use a path like `\\wsl$\Ubuntu-24.04\home\steve\Downloads\...` or copy it into WSL first.
5. Reload the window if prompted. The debugger will then be available in WSL.

## After the extension is installed

- Use **Run and Debug** (Ctrl+Shift+D) and pick a configuration:
  - **Explore telecom graph** – run `scripts/explore_telecom_graph.py` with breakpoints.
  - **Add causal overlay** – run `scripts/add_causal_overlay.py`.
  - **Pytest: current file** – debug the active test file.
  - **Pytest: all tests** – debug the full test run.
- Set breakpoints in the editor margin (left of the line numbers).
- Ensure Neo4j is running and `.env` is set when debugging scripts that use the database.

## If the debugger still doesn’t start

- **First run can fail in WSL**: Some setups need to start the debugger **twice** (first run is cancelled by the environment; second run works). Try **F5** again.
- **Interpreter**: In the status bar, click the Python version and select the interpreter from your WSL environment (e.g. the project’s venv or `python3`).
- **Cursor version**: WSL and extensions work best on Cursor **0.50+**. Check **Help → About** and update if needed.
