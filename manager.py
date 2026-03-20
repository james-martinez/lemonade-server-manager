import sys
import json
import argparse
import urllib.request
import urllib.error
import ssl
import os
from urllib.parse import urlparse

def get_api_key(target_url):
    """Retrieves the correct API key for the target URL from keys.json."""
    parsed_target = urlparse(target_url)
    target_base = f"{parsed_target.scheme}://{parsed_target.netloc}"
    
    key_file = os.path.join(os.path.dirname(__file__), "keys.json")
    
    if os.path.exists(key_file):
        try:
            with open(key_file, 'r') as f:
                keys = json.load(f)
                for server_url, api_key in keys.items():
                    parsed_server = urlparse(server_url)
                    server_base = f"{parsed_server.scheme}://{parsed_server.netloc}"
                    if target_base == server_base:
                        return api_key
        except Exception as e:
            print(f"Warning: Could not read keys.json cleanly - {e}", file=sys.stderr)

    return os.environ.get("LEMONADE_API_KEY")

def send_request(url, method="GET", payload=None, verify_ssl=True):
    """Helper to send HTTP requests with optional JSON payload and Auth headers."""
    headers = {"Content-Type": "application/json"}
    
    api_key = get_api_key(url)
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    data = None
    if payload:
        data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        # Create SSL context based on verify_ssl flag
        ctx = None
        if not verify_ssl:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(req, context=ctx) as response:
            result = response.read().decode("utf-8")
            try:
                return json.dumps(json.loads(result), indent=2)
            except json.JSONDecodeError:
                return result
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8")
        return f"HTTP Error {e.code}: {e.reason}\n{error_msg}"
    except urllib.error.URLError as e:
        return f"Connection Error: {e.reason}"

def main():
    parser = argparse.ArgumentParser(description="Lemonade Server Manager Tool")
    parser.add_argument("action", choices=[
        "info", "health", "models", "pull", "load", "unload", "chat", "image"
    ])
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of Lemonade Server")
    parser.add_argument("--model", help="Target model name or ID")
    parser.add_argument("--prompt", help="Text prompt for completions or images")
    parser.add_argument("--messages", help="JSON string of chat messages")
    parser.add_argument("--no-verify-ssl", action="store_true", help="Disable SSL certificate verification (for IP addresses with self-signed certs)")
    
    args = parser.parse_args()
    base_url = args.url.rstrip("/")

    if args.action == "info":
        print(send_request(f"{base_url}/api/v1/system-info", verify_ssl=not args.no_verify_ssl))
    elif args.action == "health":
        print(send_request(f"{base_url}/api/v1/health", verify_ssl=not args.no_verify_ssl))
    elif args.action == "models":
        print(send_request(f"{base_url}/api/v1/models", verify_ssl=not args.no_verify_ssl))
    elif args.action in ["pull", "load", "unload"]:
        if not args.model:
            print("Error: --model is required.")
            sys.exit(1)
        print(send_request(f"{base_url}/api/v1/{args.action}", method="POST", payload={"model": args.model}, verify_ssl=not args.no_verify_ssl))
    elif args.action == "chat":
        if not args.model or not args.messages:
            print("Error: --model and --messages are required.")
            sys.exit(1)

        messages_str = args.messages
        if messages_str == "-":
            messages_str = sys.stdin.read()

        try:
            messages_list = json.loads(messages_str)
        except json.JSONDecodeError:
            print("Error: --messages must be valid JSON.")
            sys.exit(1)
        print(send_request(f"{base_url}/api/v1/chat/completions", method="POST", payload={"model": args.model, "messages": messages_list}, verify_ssl=not args.no_verify_ssl))
    elif args.action == "image":
        if not args.model or not args.prompt:
            print("Error: --model and --prompt are required.")
            sys.exit(1)
        print(send_request(f"{base_url}/api/v1/images/generations", method="POST", payload={"model": args.model, "prompt": args.prompt}, verify_ssl=not args.no_verify_ssl))

if __name__ == "__main__":
    main()
