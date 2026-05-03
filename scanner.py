import whois
import time
import threading
from flask import Flask, render_template_string, request
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# --- INITIALIZATION ---
app = Flask(__name__)
console = Console()
last_scan_result = {}

# --- FLASK UI DESIGN ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Elite Dashboard</title>
    <style>
        body { font-family: sans-serif; background: #0d1117; color: #c9d1d9; text-align: center; padding: 20px; }
        .card { background: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; display: inline-block; text-align: left; }
        .success { color: #3fb950; font-family: monospace; }
        h1 { color: #58a6ff; }
    </style>
</head>
<body>
    <h1>ðŸ” awais77 Project Dashboard</h1>
    <div class="card">
        <h3>Last Scan Result:</h3>
        <pre class="success">{{ result }}</pre>
    </div>
    <p style="font-size: 12px; color: #8b949e;">Localhost Active on Port 5000</p>
</body>
</html>
'''

@app.route('/')
def index():
    result_str = str(last_scan_result) if last_scan_result else "No scan performed yet."
    return render_template_string(HTML_TEMPLATE, result=result_str)

# --- SCANNER LOGIC ---
def get_domain_details(domain):
    global last_scan_result
    try:
        w = whois.whois(domain)
        last_scan_result = {
            "Domain": w.domain_name,
            "Registrar": w.registrar,
            "Org": w.org,
            "Country": w.country,
            "Expires": str(w.expiration_date)
        }
        return last_scan_result
    except Exception as e:
        return {"Error": str(e)}

# --- TERMINAL UI ---
def run_terminal_ui():
    console.print(Panel("[bold cyan]ELITE HYBRID SCANNER[/bold cyan]\n[green]CLI + LOCALHOST ACTIVE[/green]", expand=False))
    while True:
        target = input("\n[?] Enter Domain to Scan: ").strip()
        if target:
            console.print(f"[yellow]Scanning {target}... Check Dashboard at http://127.0.0.1:5000[/yellow]")
            data = get_domain_details(target)
            
            table = Table(title=f"Result: {target}")
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="white")
            for k, v in data.items():
                table.add_row(k, str(v))
            console.print(table)

# --- SERVER THREAD ---
def run_flask():
    # Flask ko silent mode mein chalane ke liye
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Flask ko alag thread mein chalana taake terminal block na ho
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Terminal UI start karein
    try:
        run_terminal_ui()
    except KeyboardInterrupt:
        print("\nStopping services...")
