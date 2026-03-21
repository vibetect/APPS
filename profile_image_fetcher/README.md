# Profile Image Fetcher

A mini-app that fetches and saves X.com (Twitter) profile images using the [LunarCrush API](https://lunarcrush.com).

## Usage

```bash
python fetcher.py <username_or_url> [--size SIZE] [--output DIR] [--api-key KEY]
```

### Examples

```bash
# By username
python fetcher.py lunarcrush

# By X.com URL
python fetcher.py https://x.com/lunarcrush

# With @ prefix
python fetcher.py @elonmusk

# Custom size (pixels) and output directory
python fetcher.py lunarcrush --size 400 --output ./images

# With API key
python fetcher.py lunarcrush --api-key YOUR_KEY
# or via environment variable
LUNARCRUSH_API_KEY=YOUR_KEY python fetcher.py lunarcrush
```

## Output

Saves the profile image as `<username>_profile.png` in the specified output directory (defaults to the current directory).

## Requirements

- Python 3.6+
- No third-party dependencies (uses stdlib only)
- LunarCrush API key (optional for public profiles, set via `LUNARCRUSH_API_KEY`)
