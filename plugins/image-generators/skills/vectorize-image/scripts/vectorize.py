#!/usr/bin/env python3
"""Vectorize a bitmap image via the vectorizer.ai API.

Turns a raster image (PNG, JPEG, etc.) into a clean vector file (SVG by
default). Auth is HTTP Basic with the API Id + Secret, read from the
environment — run `source ~/.secrets.sh` first.

Required env:
    VECTORIZER_API_ID       API Id   (Basic-auth username)
    VECTORIZER_API_SECRET   API Secret (Basic-auth password)

Cost: production = 1.0 credit (clean output), preview = 0.2 (watermarked),
test / test_preview = free (heavily watermarked, for pipeline checks only).
Default mode is production — it spends a credit and gives a usable file.

Examples:
    # Local PNG -> SVG (production, 1 credit)
    vectorize.py logo.png -o logo.svg

    # Free pipeline check (watermarked output, no charge)
    vectorize.py logo.png -o /tmp/check.svg --mode test

    # Limit to 16 colours, output PDF
    vectorize.py photo.jpg -o photo.pdf --format pdf -P processing.max_colors=16

    # Vectorize a remote image by URL
    vectorize.py https://example.com/logo.png -o logo.svg

    # Re-download another format cheaply using a stored image token
    vectorize.py token:abc123 -o logo.eps --format eps

Any API parameter can be passed through with -P name=value (repeatable),
e.g. -P output.draw_style=stroke_edges -P processing.shapes.min_area_px=2.
See references/api.md for the full parameter list.
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
import uuid

API_URL = "https://api.vectorizer.ai/api/v1/vectorize"
EXT_BY_FORMAT = {"svg": "svg", "eps": "eps", "pdf": "pdf", "dxf": "dxf", "png": "png"}


def encode_multipart(fields, file_field=None, file_path=None):
    """Build a multipart/form-data body from a dict of fields and one file."""
    boundary = "----vectorize" + uuid.uuid4().hex
    crlf = b"\r\n"
    body = bytearray()
    for name, value in fields.items():
        body += b"--" + boundary.encode() + crlf
        body += f'Content-Disposition: form-data; name="{name}"'.encode() + crlf + crlf
        body += str(value).encode() + crlf
    if file_field and file_path:
        filename = os.path.basename(file_path)
        ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        with open(file_path, "rb") as fh:
            data = fh.read()
        body += b"--" + boundary.encode() + crlf
        body += (
            f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"'
        ).encode() + crlf
        body += f"Content-Type: {ctype}".encode() + crlf + crlf
        body += data + crlf
    body += b"--" + boundary.encode() + b"--" + crlf
    return bytes(body), f"multipart/form-data; boundary={boundary}"


def main():
    ap = argparse.ArgumentParser(
        description="Vectorize a bitmap image via vectorizer.ai.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument(
        "input",
        help="Local image path, an http(s):// URL, or token:<id> to reuse a stored image.",
    )
    ap.add_argument("-o", "--output", help="Output file path. Defaults to <input>.<format>.")
    ap.add_argument(
        "-m", "--mode", default="production",
        choices=["production", "preview", "test", "test_preview"],
        help="production=1 credit (clean), preview=0.2 (watermark), test=free (heavy watermark).",
    )
    ap.add_argument(
        "-f", "--format", default="svg", choices=list(EXT_BY_FORMAT),
        help="Output file format (default svg).",
    )
    ap.add_argument(
        "-P", "--param", action="append", default=[], metavar="name=value",
        help="Pass-through API parameter, repeatable. E.g. -P processing.max_colors=16",
    )
    args = ap.parse_args()

    api_id = os.environ.get("VECTORIZER_API_ID")
    api_secret = os.environ.get("VECTORIZER_API_SECRET")
    if not api_id or not api_secret:
        sys.exit(
            "error: VECTORIZER_API_ID / VECTORIZER_API_SECRET not set — "
            "run `source ~/.secrets.sh` first"
        )

    # Assemble form fields.
    fields = {"mode": args.mode, "output.file_format": args.format}
    for kv in args.param:
        if "=" not in kv:
            sys.exit(f"error: --param must be name=value, got: {kv!r}")
        name, value = kv.split("=", 1)
        fields[name.strip()] = value.strip()

    # Resolve the input source into the right field / file.
    file_field = file_path = None
    src = args.input
    if src.startswith(("http://", "https://")):
        fields["image.url"] = src
    elif src.startswith("token:"):
        fields["image.token"] = src[len("token:"):]
    else:
        if not os.path.isfile(src):
            sys.exit(f"error: input file not found: {src}")
        file_field, file_path = "image", src

    body, content_type = encode_multipart(fields, file_field, file_path)

    out_path = args.output
    if not out_path:
        stem = "vectorized"
        if file_path:
            stem = os.path.splitext(os.path.basename(file_path))[0]
        out_path = f"{stem}.{EXT_BY_FORMAT[args.format]}"

    auth = base64.b64encode(f"{api_id}:{api_secret}".encode()).decode()
    req = urllib.request.Request(API_URL, data=body, method="POST")
    req.add_header("Authorization", "Basic " + auth)
    req.add_header("Content-Type", content_type)

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = resp.read()
            headers = resp.headers
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            err = json.loads(raw)["error"]
            sys.exit(
                f"error: vectorizer.ai returned HTTP {e.code} "
                f"(code {err.get('code')}): {err.get('message')}"
            )
        except (ValueError, KeyError):
            sys.exit(f"error: vectorizer.ai returned HTTP {e.code}: {raw.decode(errors='replace')}")
    except urllib.error.URLError as e:
        sys.exit(f"error: could not reach vectorizer.ai: {e.reason}")

    with open(out_path, "wb") as fh:
        fh.write(payload)

    # Surface cost + reusable token so the caller knows what just happened.
    charged = headers.get("X-Credits-Charged")
    calculated = headers.get("X-Credits-Calculated")
    token = headers.get("X-Image-Token")
    receipt = headers.get("X-Receipt")
    print(f"wrote {out_path} ({len(payload)} bytes, format={args.format}, mode={args.mode})")
    if charged is not None:
        print(f"credits charged: {charged}")
    if calculated is not None:
        print(f"credits that production would cost: {calculated}")
    if token:
        print(f"image token (reuse for cheap re-downloads): {token}")
    if receipt:
        print(f"receipt: {receipt}")


if __name__ == "__main__":
    main()
