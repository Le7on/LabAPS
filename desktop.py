"""PyWebView desktop entry point (ADR-011).

Runs the Flask app (serving the built SPA) in a background thread and opens a
native desktop window pointing at it. Build the frontend first:

    cd frontend && npm run build

Then run:

    python desktop.py

Requires pywebview (``pip install pywebview``). If pywebview is unavailable this
prints instructions instead of failing hard, so the packaging path is optional.
"""

from __future__ import annotations

import threading

from backend.app import create_app

HOST = "127.0.0.1"
PORT = 5000


def _run_server(app) -> None:
    # Threaded Flask dev server is sufficient for a single-user desktop app.
    app.run(host=HOST, port=PORT, threaded=True, use_reloader=False)


def main() -> int:
    app = create_app()

    try:
        import webview
    except ImportError:
        print("pywebview is not installed. Install it with: pip install pywebview")
        print(f"Alternatively, run the server and open http://{HOST}:{PORT} in a browser.")
        _run_server(app)
        return 0

    server = threading.Thread(target=_run_server, args=(app,), daemon=True)
    server.start()

    webview.create_window("Lab APS", f"http://{HOST}:{PORT}", width=1280, height=800)
    webview.start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
