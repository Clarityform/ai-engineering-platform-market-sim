from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.auth_routes import router as auth_router
from app.routes import router as api_router

app = FastAPI(title="AI Engineering Platform", version="0.4.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
app.include_router(auth_router)


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse(
        """
        <html>
          <head>
            <title>AI Engineering Platform</title>
            <style>
              body { font-family: system-ui, sans-serif; background: #f7f9fc; color: #0f172a; margin: 40px; }
              .card { background: white; border: 1px solid #dfe7ef; border-radius: 12px; padding: 24px; max-width: 900px; }
              a { color: #1d4ed8; text-decoration: none; }
              ul { line-height: 1.8; }
              .badge { display: inline-block; background: #dbeafe; color: #1d4ed8; padding: 6px 10px; border-radius: 999px; font-size: 12px; }
            </style>
          </head>
          <body>
            <div class="card">
              <span class="badge">Prototype v0.4.0</span>
              <h1>AI Engineering Platform</h1>
              <p>Operational prototype for repo, issue, task, PR, AI planning, auth, and dashboard flows.</p>
              <ul>
                <li><a href="/api/health">Health</a></li>
                <li><a href="/api/metrics">Metrics</a></li>
                <li><a href="/api/repos">Repos</a></li>
                <li><a href="/api/issues">Issues</a></li>
                <li><a href="/api/pulls">Pull Requests</a></li>
                <li><a href="/api/tasks">Tasks</a></li>
                <li><a href="/api/ai/plans">AI Plans</a></li>
                <li><a href="/api/dashboard/summary">Dashboard Summary</a></li>
                <li><a href="/api/auth/login?username=demo&password=demo123">Demo Login</a></li>
              </ul>
            </div>
          </body>
        </html>
        """
    )
