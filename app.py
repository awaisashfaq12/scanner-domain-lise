import whois
import socket
import threading
import logging
from flask import Flask, render_template_string
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = Flask(__name__)
console = Console()
last_scan_result = {}

# --- PRO UI DESIGN (Glassmorphism Dark Theme) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>awais77 | Pro Intel Dashboard</title>
    <style>
        :root { --primary: #58a6ff; --bg: #0d1117; --card: #161b22; --text: #c9d1d9; --success: #3fb950; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .header { margin-bottom: 30px; text-align: center; }
        .header h1 { color: var(--primary); font-size: 2.5rem; margin-bottom: 5px; text-shadow: 0 0 15px rgba(88, 166, 255, 0.3); }
        .container { width: 100%; max-width: 800px; background: var(--card); border: 1px solid #30363d; border-radius: 16px; padding: 25px; box-shadow: 0 10px 40px rgba(0,0,0,0.6); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
        .data-card { background: #010409; border: 1px solid #21262d; padding: 15px; border-radius: 10px; transition: 0.3s; }
        .data-card:hover { border-color: var(--primary); transform: translateY(-5px); }
        .label { color: #8b949e; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
        .value { color: var(--success); font-size: 16px; font-weight: bold; margin-top: 5px; word-break: break-all; }
        .footer { margin-top: 40px; font-size: 12px; color: #484f58; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 awais77 Pro Intel</h1>
        <p>Advanced Domain & Owner Intelligence Scanner</p>
    </div>
    <div class="container">
        <h3 style="border-bottom: 1px solid #30363d; padding-bottom: 10px;">Latest Scan Results</h3>
        {% if data %}
        <div class="grid">
            {% for key, val in data.items() %}
            <div class="data-card">
                <div class="label">{{ key }}</div>
                <div class="value">{{ val }}</div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <p style="text-align: center; color: #8b949e;">Waiting for scan input from Termux...</p>
        {% endif %}
    </div>
    <div class="footer">Project: awais77 | v3.0 Pro Version</div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, data=last_scan_result)

# --- ADVANCED LOGIC ---
def get_pro_intel(domain):
    global last_scan_result
    try:
        # IP Intelligence
        ip_addr = socket.gethostbyname(domain)
        
        # WHOIS Intelligence (Owner/Country)
        w = whois.whois(domain)
        
        last_scan_result = {
            "Domain": domain.upper(),
            "IP Address": ip_addr,
            "Owner": w.name if w.name else "Private / Protected",
            "Organization": w.org if w.org else "N/A",
            "Country": w.country if w.country else "Unknown / Hidden",
            "Registrar": w.registrar if w.registrar else "N/A",
            "Created": str(w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date)[:10],
            "Expires": str(w.expiration_date[0] if isinstance(w.expiration_date, list) else w.expiration_date)[:10],
            "Server Status": "ONLINE"
        }
        return last_scan_result
    except Exception as e:
        last_scan_result = {"Error": str(e)}
        return last_scan_result

# --- TERMINAL UI ---
def run_cli():
    console.print(Panel("[bold cyan]AWAI577 PRO SCANNER v3.0[/bold cyan]\n[green]Hybrid UI & Logic Mode Active[/green]", expand=False))
    console.print("[dim]Dashboard: http://127.0.0.1:5000[/dim]\n")
    
    while True:
        target = input("┌──[Enter Target Domain]\n└─> ").strip()
        if not target: continue
        
        console.print(f"[yellow]Fetching Deep Intel for {target}...[/yellow]")
        data = get_pro_intel(target)
        
        if "Error" in data:
            console.print(f"[red]![/red] {data['Error']}")
        else:
            table = Table(title=f"Report: {target}", border_style="blue", show_header=True, header_style="bold magenta")
            table.add_column("Property", style="dim")
            table.add_column("Detected Value", style="bold green")
            for k, v in data.items():
                table.add_row(k, str(v))
            console.print(table)
            console.print(f"\n[bold green]✔[/bold green] Dashboard Updated Successfully!\n")

if __name__ == "__main__":
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000), daemon=True).start()
    run_cli()
