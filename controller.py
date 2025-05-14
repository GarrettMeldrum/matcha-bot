import subprocess
import threading
import time
import signal
import sys
import os

# —— CONFIGURE THESE TO MATCH YOUR SCRIPT NAMES ——
SCRIPTS = [
    "astrid-tea-bot.py",
    "jj-market-bot.py"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _stream_output(pipe, label):
    """Read lines from pipe and print them prefixed."""
    for raw in iter(pipe.readline, ""):
        line = raw.rstrip()
        if line:
            print(f"[{label}] {line}")

def launch_watchers():
    procs = []
    for script in SCRIPTS:
        script_path = os.path.join(BASE_DIR, script)
        if not os.path.isfile(script_path):
            print(f"Cannot find script: {script_path}")
            continue

        # -u = unbuffered so we see prints immediately
        cmd = [sys.executable, "-u", script_path]
        p = subprocess.Popen(
            cmd,
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,      # get str not bytes
            bufsize=1       # line-buffered
        )
        print(f"Launched {script} (pid={p.pid})")

        # start a thread to forward its output
        t = threading.Thread(
            target=_stream_output,
            args=(p.stdout, script),
            daemon=True
        )
        t.start()

        procs.append(p)

    if not procs:
        print("No slave scripts were launched. Exiting.")
        sys.exit(1)

    return procs

def shutdown(proc):
    if proc.poll() is None:
        try:
            proc.send_signal(signal.SIGINT)
        except Exception:
            pass
        time.sleep(1)

    if proc.poll() is None:
        proc.kill()
        print(f"Killed pid={proc.pid}")

def main():
    procs = launch_watchers()
    try:
        # wait for first one to exit
        winner = None
        while not winner:
            for p in procs:
                if p.poll() is not None:
                    winner = p
                    break
            time.sleep(0.5)

        print(f"\npid={winner.pid} exited first (code={winner.returncode}).")
        print("Shutting down the others...")
        for p in procs:
            if p is not winner:
                shutdown(p)

    except KeyboardInterrupt:
        print("\nController interrupted; shutting down all watchers…")
        for p in procs:
            shutdown(p)

if __name__ == "__main__":
    main()
