#!/usr/bin/env python3
"""
Profile Image Fetcher - Fetches and saves X.com (Twitter) profile images
using the LunarCrush API.

Usage:
    python fetcher.py <username_or_url> [--size SIZE] [--output DIR]

Examples:
    python fetcher.py lunarcrush
    python fetcher.py https://x.com/lunarcrush
    python fetcher.py elonmusk --size 400 --output ./images
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from urllib.error import URLError, HTTPError


LUNARCRUSH_API_BASE = "https://lunarcrush.com/api4/public"
LUNARCRUSH_IMAGE_BASE = "https://lunarcrush.com/gi"


def parse_username(input_str: str) -> str:
    """Extract username from a URL or return as-is if already a username."""
    match = re.search(r"(?:x\.com|twitter\.com)/([A-Za-z0-9_]+)", input_str)
    if match:
        return match.group(1)
    return input_str.lstrip("@")


def fetch_json(url: str, api_key: str = None) -> dict:
    """Perform a GET request and return parsed JSON."""
    headers = {"User-Agent": "profile-image-fetcher/1.0", "Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


class FetcherError(Exception):
    """Raised when the fetcher cannot resolve or download a profile image."""


def get_avatar_url(username: str, size: int, api_key: str = None) -> str:
    """
    Resolve the avatar URL for an X.com username.

    Strategy:
    1. Call /creator/x/{username}/v1 and look for known avatar fields.
    2. Extract the Twitter user ID from the creator_id field and build the
       LunarCrush CDN URL directly.
    """
    url = f"{LUNARCRUSH_API_BASE}/creator/x/{username}/v1"
    try:
        data = fetch_json(url, api_key=api_key)
    except HTTPError as e:
        hint = ""
        if e.code == 401:
            hint = " (set LUNARCRUSH_API_KEY env variable or pass --api-key)"
        elif e.code == 404:
            hint = f" (profile '@{username}' not found on LunarCrush)"
        raise FetcherError(f"HTTP {e.code} fetching profile for '{username}'{hint}") from e
    except URLError as e:
        raise FetcherError(f"Network failure: {e.reason}") from e

    # The API may return a single object or wrap results in a "data" key
    creator = data.get("data") or data
    if isinstance(creator, list):
        creator = creator[0] if creator else {}

    # 1) Direct avatar URL fields
    for field in ("profile_image_url", "profile_image", "avatar", "avatar_url", "image"):
        val = creator.get(field)
        if val and val.startswith("http"):
            return val

    # 2) Build from creator_id  e.g. "twitter::988992203568562176"
    creator_id = creator.get("creator_id") or creator.get("id", "")
    match = re.search(r"twitter::(\d+)", str(creator_id))
    if match:
        twitter_uid = match.group(1)
        return f"{LUNARCRUSH_IMAGE_BASE}/w:{size}/cr:twitter::{twitter_uid}.png"

    # 3) Fall back to plain numeric id
    uid = creator.get("uid") or creator.get("user_id")
    if uid:
        return f"{LUNARCRUSH_IMAGE_BASE}/w:{size}/cr:twitter::{uid}.png"

    raise ValueError(
        f"Could not determine avatar URL from API response.\n"
        f"Response keys: {list(creator.keys())}"
    )


def download_image(url: str, output_path: str) -> None:
    """Download an image from URL and save to output_path."""
    headers = {"User-Agent": "profile-image-fetcher/1.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()

        if not data:
            raise FetcherError("Downloaded image was empty")

        with open(output_path, "wb") as f:
            f.write(data)
    except HTTPError as e:
        raise FetcherError(f"HTTP {e.code} downloading image") from e
    except URLError as e:
        raise FetcherError(f"Network failure downloading image: {e.reason}") from e


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and save X.com profile images via LunarCrush",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "profile",
        help="X.com username, @handle, or profile URL",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=200,
        metavar="PX",
        help="Image width in pixels (default: 200)",
    )
    parser.add_argument(
        "--output",
        default=".",
        metavar="DIR",
        help="Directory to save the image (default: current directory)",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("LUNARCRUSH_API_KEY"),
        metavar="KEY",
        help="LunarCrush API key (or set LUNARCRUSH_API_KEY env variable)",
    )
    args = parser.parse_args()

    username = parse_username(args.profile)
    print(f"Fetching profile image for: @{username}")

    try:
        avatar_url = get_avatar_url(username, size=args.size, api_key=args.api_key)
    except FetcherError as e:
        print(f"Error: {e}")
        sys.exit(1)
    print(f"Avatar URL: {avatar_url}")

    ext = "png" if avatar_url.lower().endswith(".png") else "jpg"
    filename = f"{username}_profile.{ext}"
    os.makedirs(args.output, exist_ok=True)
    output_path = os.path.join(args.output, filename)

    download_image(avatar_url, output_path)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"Saved: {output_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
