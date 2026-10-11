from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)

API_HOST = os.environ.get("API_HOST", "localhost")
API_PORT = os.environ.get("API_PORT", "5000")
API_URL = f"http://{API_HOST}:{API_PORT}"


@app.route("/")
def index():
    try:
        response = requests.get(f"{API_URL}/notes", timeout=5)
        response.raise_for_status()
        notes = response.json()
        api_error = False
    except requests.RequestException:
        notes = []
        api_error = True

    return render_template(
        "home.html",
        notes=notes,
        api_error=api_error
    )


@app.route("/docker")
def docker_page():
    return render_template("docker.html")


@app.route("/compose")
def compose_page():
    return render_template("compose.html")


@app.route("/microservices")
def microservices_page():
    return render_template("microservices.html")


@app.route("/notes", methods=["POST"])
def add_note():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if title and content and len(title) <= 120 and len(content) <= 5000:
        try:
            requests.post(
                f"{API_URL}/notes",
                json={"title": title, "content": content},
                timeout=5
            ).raise_for_status()
        except requests.RequestException:
            app.logger.exception("Could not save note through the API")

    return redirect(url_for("index"))


@app.route("/health")
def health():
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        response.raise_for_status()

        return {
            "status": "healthy",
            "api": "connected",
            "database": response.json().get("database", "unknown")
        }
    except requests.RequestException:
        return {
            "status": "unhealthy",
            "api": "disconnected"
        }, 503