import cloudscraper
from flask import Flask, render_template, request, jsonify
import socket

app = Flask(__name__)
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})

@app.route('/')
def index():
    return """
    <h1>Advanced Universal Scanner</h1>
    <form action="/scan" method="post">
        <input type="text" name="url" placeholder="Enter URL (e.g. daraz.pk)" required>
        <button type="submit">Scan Website</button>
    </form>
    """

@app.route('/scan', methods=['POST'])
def scan():
    target = request.form.get('url')
    if not target.startswith('http'):
        target = 'https://' + target

    try:
        # 1. Bypass Security & Get Content
        response = scraper.get(target, timeout=10)
        
        # 2. Get Server IP
        domain = target.replace('https://', '').replace('http://', '').split('/')[0]
        ip_addr = socket.gethostbyname(domain)

        # 3. Analyze Results
        result = {
            "status": "Live",
            "url": target,
            "ip": ip_addr,
            "http_code": response.status_code,
            "server": response.headers.get('Server', 'Unknown'),
            "security": "Cloudflare/Protected" if "CF-RAY" in response.headers else "Standard"
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "Offline/Error", "details": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)