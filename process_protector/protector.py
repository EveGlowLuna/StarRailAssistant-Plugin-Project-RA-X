# -*- coding: utf-8 -*-
"""
Process Protector for SRA.exe

Requirements:
0. If not running as Administrator, relaunch itself with elevation and exit the current instance.
1. If elevated, detect ..\\..\\..\\SRA.exe. If exists, launch it as a child process and monitor exit code.
2. If exit code is non-zero (abnormal), restart SRA.exe; if zero, exit protector.

Note: SRA.exe must run as Administrator; otherwise it will spawn an elevated instance and quit itself.
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import os
import sys
import time
import subprocess
from pathlib import Path

# -----------------------------
# Admin detection and elevation
# -----------------------------

def is_user_an_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin() -> None:
    """Relaunch this script/executable with admin rights and exit current process."""
    SHELLEXECUTEINFOW = wt.SHELLEXECUTEINFOW
    SEE_MASK_NOCLOSEPROCESS = 0x00000040

    # Build parameters
    if getattr(sys, "frozen", False):
        # Frozen executable (PyInstaller/py2exe)
        exe = sys.executable
        parameters = ""
        directory = None
    else:
        exe = sys.executable
        script = Path(__file__).resolve()
        # Pass the script path quoted
        parameters = f'"{script}"'
        directory = str(script.parent)

    sei = SHELLEXECUTEINFOW()
    sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFOW)
    sei.fMask = SEE_MASK_NOCLOSEPROCESS
    sei.hwnd = None
    sei.lpVerb = "runas"
    sei.lpFile = exe
    sei.lpParameters = parameters
    sei.lpDirectory = directory
    sei.nShow = 1  # SW_SHOWNORMAL

    if not ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei)):
        raise RuntimeError("Failed to elevate process.")

    # Optionally wait for the elevated process to finish starting up a bit
    if sei.hProcess:
        # Give the new elevated instance a moment; not strictly required
        time.sleep(0.5)
    # Exit current non-elevated instance
    os._exit(0)


# -----------------------------
# SRA launching and monitoring
# -----------------------------

def find_sra_exe() -> Path:
    """Return the path of ..\\..\\..\\SRA.exe relative to this file."""
    here = Path(__file__).resolve()
    # process_protector -> ProjectRAX (1) -> plugins (2) -> repo root (3)
    target = here.parents[3] / "SRA.exe"
    return target


def launch_sra(sra_path: Path) -> subprocess.Popen:
    """Launch SRA.exe as a child process (in elevated context if protector is elevated)."""
    # Inherit elevated token from protector, so SRA runs as admin.
    # Use cwd at SRA.exe directory to ensure relative paths inside SRA work.
    return subprocess.Popen(
        [str(sra_path)],
        cwd=str(sra_path.parent),
        shell=False,
        creationflags=0,
    )


def monitor_and_restart_loop() -> None:
    sra_path = find_sra_exe()
    if not sra_path.exists():
        print(f"[protector] SRA.exe not found: {sra_path}")
    
    while True:
        # Wait until SRA.exe exists
        while not sra_path.exists():
            print("[protector] Waiting for SRA.exe to appear...")
            time.sleep(3)

        try:
            print(f"[protector] Launching: {sra_path}")
            proc = launch_sra(sra_path)
        except Exception as e:
            print(f"[protector] Failed to launch SRA.exe: {e}")
            time.sleep(3)
            continue

        try:
            rc = proc.wait()
            print(f"[protector] SRA.exe exited with code: {rc}")
        except KeyboardInterrupt:
            print("[protector] Interrupted by user, exiting protector.")
            break
        except Exception as e:
            print(f"[protector] Error while waiting SRA.exe: {e}")
            rc = -1

        # Normal exit (0) -> do not restart; Abnormal -> restart
        if rc == 0:
            print("[protector] Normal exit detected. Protector will exit.")
            break
        else:
            print("[protector] Abnormal exit detected. Restarting SRA.exe...")
            time.sleep(2)
            # loop continues and relaunches


# -----------------------------
# Entry point
# -----------------------------

def main() -> None:
    if os.name != "nt":
        print("[protector] This protector is intended for Windows.")
    if not is_user_an_admin():
        print("[protector] Not elevated. Relaunching as admin...")
        relaunch_as_admin()
        return  # Unreachable; relaunch_as_admin exits current process

    print("[protector] Running with Administrator privileges.")
    monitor_and_restart_loop()


if __name__ == "__main__":
    main()