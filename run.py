"""Development entry point.

Starts the Flask REST API server. In production the frontend is built and hosted
by PyWebView; this entry point is for backend development and testing.
"""

from __future__ import annotations

from backend.app import create_app


def main() -> None:
    app = create_app()
    config = app.config["APP_CONFIG"]
    app.run(host=config.api.host, port=config.api.port, debug=config.env == "development")


if __name__ == "__main__":
    main()
