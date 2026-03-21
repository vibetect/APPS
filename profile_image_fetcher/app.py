#!/usr/bin/env python3
"""
Flask web server for the Profile Image Fetcher.
Run:  python app.py
Then open http://localhost:5000 in your browser.
"""

import os
import urllib.request
from urllib.error import HTTPError, URLError

from flask import Flask, jsonify, render_template, request, send_file

from fetcher import FetcherError, get_avatar_url, parse_username

app = Flask(__name__)

SAVED_DIR = os.path.join(os.path.dirname(__file__), "saved_images")
os.makedirs(SAVED_DIR, exist_ok=True)

API_KEY = os.environ.get("LUNARCRUSH_API_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fetch", methods=["POST"])
def fetch():
    profile = (request.json or {}).get("profile", "").strip()
    size = int((request.json or {}).get("size", 200))

    if not profile:
        return jsonify({"error": "Profile name or URL is required"}), 400

    username = parse_username(profile)
    if not username:
        return jsonify({"error": "Could not parse a username from the input"}), 400

    try:
        avatar_url = get_avatar_url(username, size=size, api_key=API_KEY)
    except FetcherError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 500

    # Download into memory for preview
    try:
        headers = {"User-Agent": "profile-image-fetcher/1.0"}
        req = urllib.request.Request(avatar_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            image_data = resp.read()
            content_type = resp.headers.get("Content-Type", "image/png")
    except (HTTPError, URLError) as e:
        return jsonify({"error": f"Failed to download image: {e}"}), 502

    if not image_data:
        return jsonify({"error": "Downloaded image was empty"}), 502

    # Save to disk
    ext = "png" if avatar_url.lower().endswith(".png") else "jpg"
    filename = f"{username}_profile.{ext}"
    saved_path = os.path.join(SAVED_DIR, filename)
    with open(saved_path, "wb") as f:
        f.write(image_data)

    size_kb = round(len(image_data) / 1024, 1)

    return jsonify(
        {
            "username": username,
            "avatar_url": avatar_url,
            "filename": filename,
            "saved_path": saved_path,
            "size_kb": size_kb,
            "content_type": content_type,
        }
    )


@app.route("/image/<filename>")
def serve_image(filename):
    """Serve a previously saved image for preview."""
    path = os.path.join(SAVED_DIR, filename)
    if not os.path.isfile(path):
        return "Not found", 404
    return send_file(path)


@app.route("/download/<filename>")
def download(filename):
    """Trigger a browser download of a saved image."""
    path = os.path.join(SAVED_DIR, filename)
    if not os.path.isfile(path):
        return "Not found", 404
    return send_file(path, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    print("Profile Image Fetcher running at http://localhost:5000")
    app.run(debug=True, port=5000)
