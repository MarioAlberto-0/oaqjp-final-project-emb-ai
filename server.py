"""Convenience entry point for the final-project Flask server."""

from final_project.server import app


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
