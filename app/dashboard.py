from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.root import app as root_app

app = FastAPI(title="AI Engineering Platform API", version="0.3.0")


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse(
        """
        <html>
          <head>
            <title>AI Engineering Platform</title>
            <style>
              body { font-family: sans-serif; margin: 40px; }
              .box { border: 1px solid #ddd; padding: 16px; border-radius: 8px; max-width: 760px; }
              a { color: #1857d3; }
            </style>
          </head>
          <body>
            <div class="box">
              <h1>AI Engineering Platform</h1>
              <p>Prototype dashboard</p>
              <ul>
                <li><a href="/api/health">/api/health</a></li>
                <li><a href="/api/metrics">/api/metrics</a></li>
                <li><a href="/api/repos">/api/repos</a></li>
                <li><a href="/api/issues">/api/issues</a></li>
                <li><a href="/api/pulls">/api/pulls</a></li>
                <li><a href="/api/tasks">/api/tasks</a></li>
                <li><a href="/api/ai/plans">/api/ai/plans</a></li>
              </ul>
            </div>
          </body>
        </html>
        """
    )


# Mount the API routes
from app.routes import router as api_router  # type: ignore
app.include_router(api_router)
