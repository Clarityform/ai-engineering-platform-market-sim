from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.routes import router

app = FastAPI(title="AI Engineering Platform", version="0.6.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse(
        """
        <html>
          <head>
            <title>AI Engineering Platform</title>
            <style>
              body { font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; margin: 0; padding: 32px; }
              .container { max-width: 1100px; margin: 0 auto; }
              .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-top: 28px; }
              .card { background: #111827; border: 1px solid #334155; border-radius: 14px; padding: 18px; }
              .card h3 { margin-top: 0; }
              .metric { font-size: 2rem; font-weight: 700; }
              .nav { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 20px; }
              .nav a { color: #93c5fd; text-decoration: none; }
              code { font-size: 12px; }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>AI Engineering Platform</h1>
              <p>Operational prototype dashboard for repo intelligence, task workflows, release management, and AI planning.</p>
              <div class="nav">
                <a href="/api/health">Health</a>
                <a href="/api/metrics">Metrics</a>
                <a href="/api/dashboard/overview">Overview</a>
                <a href="/api/analytics/release-readiness">Readiness</a>
                <a href="/api/repos">Repos</a>
                <a href="/api/tasks">Tasks</a>
                <a href="/api/projects">Projects</a>
                <a href="/api/releases">Releases</a>
                <a href="/api/environments">Environments</a>
              </div>
              <div id="dashboard" class="grid"></div>
            </div>
            <script>
              async function loadOverview() {
                const res = await fetch('/api/dashboard/overview');
                const data = await res.json();
                const metrics = data.metrics || {};
                const cards = [
                  { label: 'Repos', value: metrics.repos || 0 },
                  { label: 'Issues', value: metrics.issues || 0 },
                  { label: 'Pull Requests', value: metrics.prs || 0 },
                  { label: 'Tasks', value: metrics.tasks || 0 },
                  { label: 'AI Plans', value: metrics.plans || 0 },
                  { label: 'Projects', value: metrics.projects || 0 },
                  { label: 'Releases', value: metrics.releases || 0 },
                  { label: 'Environments', value: metrics.environments || 0 },
                ];
                document.getElementById('dashboard').innerHTML = cards.map(item => `
                  <div class="card">
                    <h3>${item.label}</h3>
                    <div class="metric">${item.value}</div>
                  </div>
                `).join('');
              }
              loadOverview();
            </script>
          </body>
        </html>
        """
    )
