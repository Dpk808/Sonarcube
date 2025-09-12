from flask import Flask, request, render_template_string, send_from_directory
import os
from prometheus_flask_exporter import PrometheusMetrics
from datetime import datetime

app = Flask(__name__)
metrics = PrometheusMetrics(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>File Upload on Kubernetes</title>
    <style>
        :root {
            --bg: #f6f8fb;
            --card: #ffffff;
            --text: #1f2937;
            --muted: #6b7280;
            --primary: #2563eb;
            --primary-600: #1d4ed8;
            --danger: #ef4444;
            --danger-600: #dc2626;
            --ring: rgba(37, 99, 235, 0.25);
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg: #0b1220;
                --card: #0f172a;
                --text: #e5e7eb;
                --muted: #94a3b8;
                --primary: #60a5fa;
                --primary-600: #3b82f6;
                --danger: #f87171;
                --danger-600: #ef4444;
                --ring: rgba(96, 165, 250, 0.35);
            }
        }

        * { box-sizing: border-box; }
        html, body { height: 100%; }
        body {
            margin: 0;
            font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica Neue, Arial, "Apple Color Emoji", "Segoe UI Emoji";
            background: radial-gradient(1200px 600px at 10% -10%, rgba(37, 99, 235, 0.08), transparent 60%),
                        radial-gradient(800px 400px at 110% 10%, rgba(99, 102, 241, 0.08), transparent 60%),
                        var(--bg);
            color: var(--text);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        .container {
            max-width: 960px;
            margin: 0 auto;
            padding: 24px;
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 20px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo {
            width: 36px;
            height: 36px;
            border-radius: 8px;
            background: linear-gradient(135deg, var(--primary), #8b5cf6);
            box-shadow: 0 6px 24px rgba(2, 6, 23, 0.15);
        }

        h1 {
            font-size: 1.35rem;
            margin: 0;
        }

        .actions a {
            color: var(--muted);
            text-decoration: none;
            font-size: 0.95rem;
        }
        .actions a:hover { color: var(--text); }

        .card {
            background: var(--card);
            border: 1px solid rgba(2, 6, 23, 0.06);
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 1px 2px rgba(2, 6, 23, 0.04), 0 8px 30px rgba(2, 6, 23, 0.06);
        }

        .upload {
            display: grid;
            gap: 12px;
            justify-items: start;
            margin-bottom: 20px;
        }

        .file-input {
            position: relative;
            display: inline-block;
        }
        .file-input input[type="file"] {
            position: absolute;
            inset: 0;
            opacity: 0;
            width: 100%;
            height: 100%;
            cursor: pointer;
        }
        .file-label {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 14px;
            background: linear-gradient(180deg, rgba(2, 6, 23, 0.03), transparent);
            border: 1px dashed rgba(2, 6, 23, 0.15);
            border-radius: 10px;
            color: var(--muted);
            transition: border-color .2s, color .2s, box-shadow .2s;
        }
        .file-input:hover .file-label {
            color: var(--text);
            border-color: var(--primary);
            box-shadow: 0 0 0 4px var(--ring);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 16px;
            border-radius: 10px;
            border: 1px solid rgba(2, 6, 23, 0.12);
            background: linear-gradient(180deg, rgba(255,255,255,0.06), transparent);
            color: var(--text);
            cursor: pointer;
            transition: transform .05s ease, box-shadow .2s, background .2s;
        }
        .btn:active { transform: translateY(1px); }
        .btn-primary {
            background: linear-gradient(180deg, var(--primary), var(--primary-600));
            border: none;
            color: white;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35);
        }
        .btn-primary:hover { filter: brightness(1.05); }
        .btn-danger {
            background: linear-gradient(180deg, var(--danger), var(--danger-600));
            border: none;
            color: white;
            box-shadow: 0 6px 18px rgba(239, 68, 68, 0.3);
        }
        .btn-danger:hover { filter: brightness(1.05); }

        .message {
            margin: 0 0 8px 0;
            color: var(--muted);
            font-size: 0.95rem;
        }

        .list {
            display: grid;
            gap: 10px;
            margin-top: 12px;
        }
        .item {
            display: grid;
            grid-template-columns: 1fr auto auto;
            align-items: center;
            gap: 10px;
            padding: 12px;
            border: 1px solid rgba(2, 6, 23, 0.08);
            border-radius: 12px;
            background: linear-gradient(180deg, rgba(2,6,23,0.03), transparent);
        }
        .file-meta {
            display: grid;
            grid-template-columns: auto 1fr;
            align-items: center;
            gap: 10px;
            text-align: left;
        }
        .file-meta small { color: var(--muted); display: block; }
        .item a { color: inherit; text-decoration: none; }
        .item a:hover { text-decoration: underline; }

        .footer {
            margin-top: 26px;
            color: var(--muted);
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .footer a { color: var(--muted); }
        .footer a:hover { color: var(--text); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="brand">
                <div class="logo" aria-hidden="true"></div>
                <h1>Kubernetes File Uploader</h1>
            </div>
            <div class="actions">
                <a href="/metrics" target="_blank" rel="noopener">Prometheus metrics</a>
            </div>
        </div>

        <div class="card">
            <form class="upload" action="/" method="post" enctype="multipart/form-data">
                <div class="file-input">
                    <span class="file-label">📁 Choose a file…</span>
                    <input type="file" name="file" required>
                </div>
                <button type="submit" class="btn btn-primary">⬆️ Upload</button>
                <div class="message">{{ msg }}</div>
            </form>

            <div class="list">
                {% for file in files %}
                    <div class="item">
                        <div class="file-meta">
                            <div>📄</div>
                            <div>
                                <a href="/uploads/{{ file.name }}" target="_blank">{{ file.name }}</a>
                                <small>{{ file.size_human }} • {{ file.mtime_human }}</small>
                            </div>
                        </div>
                        <a class="btn" href="/uploads/{{ file.name }}" target="_blank">View</a>
                        <form action="/delete/{{ file.name }}" method="post" onsubmit="return confirm('Delete {{ file.name }}?');">
                            <button type="submit" class="btn btn-danger">Delete</button>
                        </form>
                    </div>
                {% else %}
                    <div class="item" style="justify-content:center;">
                        <div class="file-meta"><div>🗂️</div><div>No files uploaded yet.</div></div>
                    </div>
                {% endfor %}
            </div>
        </div>

        <div class="footer">
            <span>Lightweight Flask • Observability-ready</span>
            <span><a href="https://prometheus.io" target="_blank" rel="noopener">Prometheus</a> + <a href="https://flask.palletsprojects.com" target="_blank" rel="noopener">Flask</a></span>
        </div>
    </div>
</body>
</html>
'''

def _human_bytes(num_bytes: int) -> str:
    step = 1024.0
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    unit_index = 0
    while size >= step and unit_index < len(units) - 1:
        size /= step
        unit_index += 1
    return f"{size:.1f} {units[unit_index]}" if unit_index > 0 else f"{int(size)} {units[unit_index]}"


def _list_files():
    try:
        entries = []
        for name in os.listdir(UPLOAD_FOLDER):
            path = os.path.join(UPLOAD_FOLDER, name)
            if not os.path.isfile(path):
                continue
            stat = os.stat(path)
            entries.append({
                "name": name,
                "size": stat.st_size,
                "size_human": _human_bytes(stat.st_size),
                "mtime": stat.st_mtime,
                "mtime_human": datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
            })
        # Newest first
        entries.sort(key=lambda e: e["mtime"], reverse=True)
        return entries
    except FileNotFoundError:
        return []


@app.route("/", methods=["GET", "POST"])
def upload():
    msg = ""
    if request.method == "POST":
        f = request.files['file']
        if f:
            f.save(os.path.join(UPLOAD_FOLDER, f.filename))
            msg = "Uploaded successfully!"
    files = _list_files()
    return render_template_string(HTML, msg=msg, files=files)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        msg = f"File {filename} deleted successfully!"
    except FileNotFoundError:
        msg = f"File {filename} not found."
    files = _list_files()
    return render_template_string(HTML, msg=msg, files=files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)