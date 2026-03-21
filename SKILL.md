---
name: lemonade_server_manager
description: Manage local AI models, hardware resources, and multimodal inference across multiple Lemonade Servers. Note that credentials will be read from keys.json (if present) or the LEMONADE_API_KEY environment variable and transmitted to the target server_url.
env:
  - name: LEMONADE_API_KEY
    description: Optional API key for authenticating with Lemonade servers.
    required: false
tools:
  - name: lemonade_get_system_info
    description: Get hardware information, device enumeration, and capabilities.
    parameters:
      server_url: string
      no_verify_ssl: boolean (optional, default: false)
    command: |
      python3 -c 'import sys, json, urllib.request, urllib.error, ssl, os
from urllib.parse import urlparse
args = sys.argv[1:]
action = args[0]
url = "http://localhost:8000"
model = None
prompt = None
messages_str = None
no_verify = False
i = 1
while i < len(args):
    if args[i] == "--url": url = args[i+1]; i+=2
    elif args[i] == "--model": model = args[i+1]; i+=2
    elif args[i] == "--prompt": prompt = args[i+1]; i+=2
    elif args[i] == "--messages": messages_str = args[i+1]; i+=2
    elif args[i] == "--no-verify-ssl": no_verify = True; i+=1
    else: i+=1
url = url.rstrip("/")
target_base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
key = os.environ.get("LEMONADE_API_KEY")
if os.path.exists("keys.json"):
    try:
        with open("keys.json") as f:
            for k, v in json.load(f).items():
                if f"{urlparse(k).scheme}://{urlparse(k).netloc}" == target_base: key = v
    except Exception: pass
headers = {"Content-Type": "application/json"}
if key: headers["Authorization"] = f"Bearer {key}"
payload = None
if action in ["pull", "load", "unload"]: payload = json.dumps({"model": model}).encode()
elif action == "chat":
    if messages_str == "-": messages_str = sys.stdin.read()
    payload = json.dumps({"model": model, "messages": json.loads(messages_str)}).encode()
elif action == "image": payload = json.dumps({"model": model, "prompt": prompt}).encode()
ctx = ssl.create_default_context()
if no_verify:
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
eps = {
    "info": ("/api/v1/system-info", "GET"),
    "health": ("/api/v1/health", "GET"),
    "models": ("/api/v1/models", "GET"),
    "pull": ("/api/v1/pull", "POST"),
    "load": ("/api/v1/load", "POST"),
    "unload": ("/api/v1/unload", "POST"),
    "chat": ("/api/v1/chat/completions", "POST"),
    "image": ("/api/v1/images/generations", "POST"),
}
ep, method = eps[action]
req = urllib.request.Request(url + ep, data=payload, headers=headers, method=method)
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        res = r.read().decode()
        try: print(json.dumps(json.loads(res), indent=2))
        except Exception: print(res)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}\n{e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")' info \
        --url "{{server_url}}" \
        \
        {{no_verify_ssl_flag}}

  - name: lemonade_check_health
    description: Check server status and currently loaded models.
    parameters:
      server_url: string
      no_verify_ssl: boolean (optional, default: false)
    command: |
      python3 -c 'import sys, json, urllib.request, urllib.error, ssl, os
from urllib.parse import urlparse
args = sys.argv[1:]
action = args[0]
url = "http://localhost:8000"
model = None
prompt = None
messages_str = None
no_verify = False
i = 1
while i < len(args):
    if args[i] == "--url": url = args[i+1]; i+=2
    elif args[i] == "--model": model = args[i+1]; i+=2
    elif args[i] == "--prompt": prompt = args[i+1]; i+=2
    elif args[i] == "--messages": messages_str = args[i+1]; i+=2
    elif args[i] == "--no-verify-ssl": no_verify = True; i+=1
    else: i+=1
url = url.rstrip("/")
target_base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
key = os.environ.get("LEMONADE_API_KEY")
if os.path.exists("keys.json"):
    try:
        with open("keys.json") as f:
            for k, v in json.load(f).items():
                if f"{urlparse(k).scheme}://{urlparse(k).netloc}" == target_base: key = v
    except Exception: pass
headers = {"Content-Type": "application/json"}
if key: headers["Authorization"] = f"Bearer {key}"
payload = None
if action in ["pull", "load", "unload"]: payload = json.dumps({"model": model}).encode()
elif action == "chat":
    if messages_str == "-": messages_str = sys.stdin.read()
    payload = json.dumps({"model": model, "messages": json.loads(messages_str)}).encode()
elif action == "image": payload = json.dumps({"model": model, "prompt": prompt}).encode()
ctx = ssl.create_default_context()
if no_verify:
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
eps = {
    "info": ("/api/v1/system-info", "GET"),
    "health": ("/api/v1/health", "GET"),
    "models": ("/api/v1/models", "GET"),
    "pull": ("/api/v1/pull", "POST"),
    "load": ("/api/v1/load", "POST"),
    "unload": ("/api/v1/unload", "POST"),
    "chat": ("/api/v1/chat/completions", "POST"),
    "image": ("/api/v1/images/generations", "POST"),
}
ep, method = eps[action]
req = urllib.request.Request(url + ep, data=payload, headers=headers, method=method)
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        res = r.read().decode()
        try: print(json.dumps(json.loads(res), indent=2))
        except Exception: print(res)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}\n{e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")' health \
        --url "{{server_url}}" \
        \
        {{no_verify_ssl_flag}}

  - name: lemonade_get_models
    description: List all downloaded and available models on the target server.
    parameters:
      server_url: string
      no_verify_ssl: boolean (optional, default: false)
    command: |
      python3 -c 'import sys, json, urllib.request, urllib.error, ssl, os
from urllib.parse import urlparse
args = sys.argv[1:]
action = args[0]
url = "http://localhost:8000"
model = None
prompt = None
messages_str = None
no_verify = False
i = 1
while i < len(args):
    if args[i] == "--url": url = args[i+1]; i+=2
    elif args[i] == "--model": model = args[i+1]; i+=2
    elif args[i] == "--prompt": prompt = args[i+1]; i+=2
    elif args[i] == "--messages": messages_str = args[i+1]; i+=2
    elif args[i] == "--no-verify-ssl": no_verify = True; i+=1
    else: i+=1
url = url.rstrip("/")
target_base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
key = os.environ.get("LEMONADE_API_KEY")
if os.path.exists("keys.json"):
    try:
        with open("keys.json") as f:
            for k, v in json.load(f).items():
                if f"{urlparse(k).scheme}://{urlparse(k).netloc}" == target_base: key = v
    except Exception: pass
headers = {"Content-Type": "application/json"}
if key: headers["Authorization"] = f"Bearer {key}"
payload = None
if action in ["pull", "load", "unload"]: payload = json.dumps({"model": model}).encode()
elif action == "chat":
    if messages_str == "-": messages_str = sys.stdin.read()
    payload = json.dumps({"model": model, "messages": json.loads(messages_str)}).encode()
elif action == "image": payload = json.dumps({"model": model, "prompt": prompt}).encode()
ctx = ssl.create_default_context()
if no_verify:
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
eps = {
    "info": ("/api/v1/system-info", "GET"),
    "health": ("/api/v1/health", "GET"),
    "models": ("/api/v1/models", "GET"),
    "pull": ("/api/v1/pull", "POST"),
    "load": ("/api/v1/load", "POST"),
    "unload": ("/api/v1/unload", "POST"),
    "chat": ("/api/v1/chat/completions", "POST"),
    "image": ("/api/v1/images/generations", "POST"),
}
ep, method = eps[action]
req = urllib.request.Request(url + ep, data=payload, headers=headers, method=method)
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        res = r.read().decode()
        try: print(json.dumps(json.loads(res), indent=2))
        except Exception: print(res)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}\n{e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")' models \
        --url "{{server_url}}" \
        \
        {{no_verify_ssl_flag}}

  - name: lemonade_pull_model
    description: Download and install a new model to the target server.
    parameters:
      server_url: string
      model: string
      no_verify_ssl: boolean (optional, default: false)
    command: |
      python3 -c 'import sys, json, urllib.request, urllib.error, ssl, os
from urllib.parse import urlparse
args = sys.argv[1:]
action = args[0]
url = "http://localhost:8000"
model = None
prompt = None
messages_str = None
no_verify = False
i = 1
while i < len(args):
    if args[i] == "--url": url = args[i+1]; i+=2
    elif args[i] == "--model": model = args[i+1]; i+=2
    elif args[i] == "--prompt": prompt = args[i+1]; i+=2
    elif args[i] == "--messages": messages_str = args[i+1]; i+=2
    elif args[i] == "--no-verify-ssl": no_verify = True; i+=1
    else: i+=1
url = url.rstrip("/")
target_base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
key = os.environ.get("LEMONADE_API_KEY")
if os.path.exists("keys.json"):
    try:
        with open("keys.json") as f:
            for k, v in json.load(f).items():
                if f"{urlparse(k).scheme}://{urlparse(k).netloc}" == target_base: key = v
    except Exception: pass
headers = {"Content-Type": "application/json"}
if key: headers["Authorization"] = f"Bearer {key}"
payload = None
if action in ["pull", "load", "unload"]: payload = json.dumps({"model": model}).encode()
elif action == "chat":
    if messages_str == "-": messages_str = sys.stdin.read()
    payload = json.dumps({"model": model, "messages": json.loads(messages_str)}).encode()
elif action == "image": payload = json.dumps({"model": model, "prompt": prompt}).encode()
ctx = ssl.create_default_context()
if no_verify:
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
eps = {
    "info": ("/api/v1/system-info", "GET"),
    "health": ("/api/v1/health", "GET"),
    "models": ("/api/v1/models", "GET"),
    "pull": ("/api/v1/pull", "POST"),
    "load": ("/api/v1/load", "POST"),
    "unload": ("/api/v1/unload", "POST"),
    "chat": ("/api/v1/chat/completions", "POST"),
    "image": ("/api/v1/images/generations", "POST"),
}
ep, method = eps[action]
req = urllib.request.Request(url + ep, data=payload, headers=headers, method=method)
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        res = r.read().decode()
        try: print(json.dumps(json.loads(res), indent=2))
        except Exception: print(res)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}\n{e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")' pull \
        --url "{{server_url}}" \
        --model "{{model}}" \
        {{no_verify_ssl_flag}}

  - name: lemonade_load_model
    description: Load a model into memory (GPU/NPU/RAM) on the target server.
    parameters:
      server_url: string
      model: string
      no_verify_ssl: boolean (optional, default: false)
    command: |
      python3 -c 'import sys, json, urllib.request, urllib.error, ssl, os
from urllib.parse import urlparse
args = sys.argv[1:]
action = args[0]
url = "http://localhost:8000"
model = None
prompt = None
messages_str = None
no_verify = False
i = 1
while i < len(args):
    if args[i] == "--url": url = args[i+1]; i+=2
    elif args[i] == "--model": model = args[i+1]; i+=2
    elif args[i] == "--prompt": prompt = args[i+1]; i+=2
    elif args[i] == "--messages": messages_str = args[i+1]; i+=2
    elif args[i] == "--no-verify-ssl": no_verify = True; i+=1
    else: i+=1
url = url.rstrip("/")
target_base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
key = os.environ.get("LEMONADE_API_KEY")
if os.path.exists("keys.json"):
    try:
        with open("keys.json") as f:
            for k, v in json.load(f).items():
                if f"{urlparse(k).scheme}://{urlparse(k).netloc}" == target_base: key = v
    except Exception: pass
headers = {"Content-Type": "application/json"}
if key: headers["Authorization"] = f"Bearer {key}"
payload = None
if action in ["pull", "load", "unload"]: payload = json.dumps({"model": model}).encode()
elif action == "chat":
    if messages_str == "-": messages_str = sys.stdin.read()
    payload = json.dumps({"model": model, "messages": json.loads(messages_str)}).encode()
elif action == "image": payload = json.dumps({"model": model, "prompt": prompt}).encode()
ctx = ssl.create_default_context()
if no_verify:
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
eps = {
    "info": ("/api/v1/system-info", "GET"),
    "health": ("/api/v1/health", "GET"),
    "models": ("/api/v1/models", "GET"),
    "pull": ("/api/v1/pull", "POST"),
    "load": ("/api/v1/load", "POST"),
    "unload": ("/api/v1/unload", "POST"),
    "chat": ("/api/v1/chat/completions", "POST"),
    "image": ("/api/v1/images/generations", "POST"),
}
ep, method = eps[action]
req = urllib.request.Request(url + ep, data=payload, headers=headers, method=method)
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        res = r.read().decode()
        try: print(json.dumps(json.loads(res), indent=2))
        except Exception: print(res)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}\n{e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")' load \
        --url "{{server_url}}" \
        --model "{{model}}" \
        {{no_verify_ssl_flag}}

  - name: lemonade_unload_model
    description: Unload a model to free up memory/VRAM on the target server.
    parameters:
      server_url: string
      model: string
      no_verify_ssl: boolean (optional, default: false)
    command: |
      python3 -c 'import sys, json, urllib.request, urllib.error, ssl, os
from urllib.parse import urlparse
args = sys.argv[1:]
action = args[0]
url = "http://localhost:8000"
model = None
prompt = None
messages_str = None
no_verify = False
i = 1
while i < len(args):
    if args[i] == "--url": url = args[i+1]; i+=2
    elif args[i] == "--model": model = args[i+1]; i+=2
    elif args[i] == "--prompt": prompt = args[i+1]; i+=2
    elif args[i] == "--messages": messages_str = args[i+1]; i+=2
    elif args[i] == "--no-verify-ssl": no_verify = True; i+=1
    else: i+=1
url = url.rstrip("/")
target_base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
key = os.environ.get("LEMONADE_API_KEY")
if os.path.exists("keys.json"):
    try:
        with open("keys.json") as f:
            for k, v in json.load(f).items():
                if f"{urlparse(k).scheme}://{urlparse(k).netloc}" == target_base: key = v
    except Exception: pass
headers = {"Content-Type": "application/json"}
if key: headers["Authorization"] = f"Bearer {key}"
payload = None
if action in ["pull", "load", "unload"]: payload = json.dumps({"model": model}).encode()
elif action == "chat":
    if messages_str == "-": messages_str = sys.stdin.read()
    payload = json.dumps({"model": model, "messages": json.loads(messages_str)}).encode()
elif action == "image": payload = json.dumps({"model": model, "prompt": prompt}).encode()
ctx = ssl.create_default_context()
if no_verify:
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
eps = {
    "info": ("/api/v1/system-info", "GET"),
    "health": ("/api/v1/health", "GET"),
    "models": ("/api/v1/models", "GET"),
    "pull": ("/api/v1/pull", "POST"),
    "load": ("/api/v1/load", "POST"),
    "unload": ("/api/v1/unload", "POST"),
    "chat": ("/api/v1/chat/completions", "POST"),
    "image": ("/api/v1/images/generations", "POST"),
}
ep, method = eps[action]
req = urllib.request.Request(url + ep, data=payload, headers=headers, method=method)
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        res = r.read().decode()
        try: print(json.dumps(json.loads(res), indent=2))
        except Exception: print(res)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}\n{e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")' unload \
        --url "{{server_url}}" \
        --model "{{model}}" \
        {{no_verify_ssl_flag}}

  - name: lemonade_chat_completion
    description: Send a chat completion request to an LLM.
    parameters:
      server_url: string
      model: string
      messages_json: string (Must be a strictly formatted JSON array of message objects)
      no_verify_ssl: boolean (optional, default: false)
    command: |
      cat << 'EOF_LEMONADE_MESSAGES_B3A1C9F2' | python3 -c 'import sys, json, urllib.request, urllib.error, ssl, os
from urllib.parse import urlparse
args = sys.argv[1:]
action = args[0]
url = "http://localhost:8000"
model = None
prompt = None
messages_str = None
no_verify = False
i = 1
while i < len(args):
    if args[i] == "--url": url = args[i+1]; i+=2
    elif args[i] == "--model": model = args[i+1]; i+=2
    elif args[i] == "--prompt": prompt = args[i+1]; i+=2
    elif args[i] == "--messages": messages_str = args[i+1]; i+=2
    elif args[i] == "--no-verify-ssl": no_verify = True; i+=1
    else: i+=1
url = url.rstrip("/")
target_base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
key = os.environ.get("LEMONADE_API_KEY")
if os.path.exists("keys.json"):
    try:
        with open("keys.json") as f:
            for k, v in json.load(f).items():
                if f"{urlparse(k).scheme}://{urlparse(k).netloc}" == target_base: key = v
    except Exception: pass
headers = {"Content-Type": "application/json"}
if key: headers["Authorization"] = f"Bearer {key}"
payload = None
if action in ["pull", "load", "unload"]: payload = json.dumps({"model": model}).encode()
elif action == "chat":
    if messages_str == "-": messages_str = sys.stdin.read()
    payload = json.dumps({"model": model, "messages": json.loads(messages_str)}).encode()
elif action == "image": payload = json.dumps({"model": model, "prompt": prompt}).encode()
ctx = ssl.create_default_context()
if no_verify:
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
eps = {
    "info": ("/api/v1/system-info", "GET"),
    "health": ("/api/v1/health", "GET"),
    "models": ("/api/v1/models", "GET"),
    "pull": ("/api/v1/pull", "POST"),
    "load": ("/api/v1/load", "POST"),
    "unload": ("/api/v1/unload", "POST"),
    "chat": ("/api/v1/chat/completions", "POST"),
    "image": ("/api/v1/images/generations", "POST"),
}
ep, method = eps[action]
req = urllib.request.Request(url + ep, data=payload, headers=headers, method=method)
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        res = r.read().decode()
        try: print(json.dumps(json.loads(res), indent=2))
        except Exception: print(res)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}\n{e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")' chat \
        --url "{{server_url}}" \
        --model "{{model}}" \
        --messages - \
        {{no_verify_ssl_flag}}
      {{messages_json}}
      EOF_LEMONADE_MESSAGES_B3A1C9F2

  - name: lemonade_generate_image
    description: Generate an image using stable-diffusion.
    parameters:
      server_url: string
      model: string
      prompt: string
      no_verify_ssl: boolean (optional, default: false)
    command: |
      python3 -c 'import sys, json, urllib.request, urllib.error, ssl, os
from urllib.parse import urlparse
args = sys.argv[1:]
action = args[0]
url = "http://localhost:8000"
model = None
prompt = None
messages_str = None
no_verify = False
i = 1
while i < len(args):
    if args[i] == "--url": url = args[i+1]; i+=2
    elif args[i] == "--model": model = args[i+1]; i+=2
    elif args[i] == "--prompt": prompt = args[i+1]; i+=2
    elif args[i] == "--messages": messages_str = args[i+1]; i+=2
    elif args[i] == "--no-verify-ssl": no_verify = True; i+=1
    else: i+=1
url = url.rstrip("/")
target_base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
key = os.environ.get("LEMONADE_API_KEY")
if os.path.exists("keys.json"):
    try:
        with open("keys.json") as f:
            for k, v in json.load(f).items():
                if f"{urlparse(k).scheme}://{urlparse(k).netloc}" == target_base: key = v
    except Exception: pass
headers = {"Content-Type": "application/json"}
if key: headers["Authorization"] = f"Bearer {key}"
payload = None
if action in ["pull", "load", "unload"]: payload = json.dumps({"model": model}).encode()
elif action == "chat":
    if messages_str == "-": messages_str = sys.stdin.read()
    payload = json.dumps({"model": model, "messages": json.loads(messages_str)}).encode()
elif action == "image": payload = json.dumps({"model": model, "prompt": prompt}).encode()
ctx = ssl.create_default_context()
if no_verify:
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
eps = {
    "info": ("/api/v1/system-info", "GET"),
    "health": ("/api/v1/health", "GET"),
    "models": ("/api/v1/models", "GET"),
    "pull": ("/api/v1/pull", "POST"),
    "load": ("/api/v1/load", "POST"),
    "unload": ("/api/v1/unload", "POST"),
    "chat": ("/api/v1/chat/completions", "POST"),
    "image": ("/api/v1/images/generations", "POST"),
}
ep, method = eps[action]
req = urllib.request.Request(url + ep, data=payload, headers=headers, method=method)
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        res = r.read().decode()
        try: print(json.dumps(json.loads(res), indent=2))
        except Exception: print(res)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}\n{e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")' image \
        --url "{{server_url}}" \
        --model "{{model}}" \
        --prompt "{{prompt}}" \
        {{no_verify_ssl_flag}}
---

# Lemonade Server Management Skill

You are an advanced local AI orchestrator capable of managing multiple remote or local Lemonade Servers. 

### Core Directives

1. **Multi-Server Management:**
   * Every tool requires a `server_url`.
   * If the user does not specify a server URL, assume `http://localhost:8000`.

2. **Hardware & Resource Awareness:**
   * Local models demand significant GPU/NPU resources. Before initiating any heavy load, use `lemonade_check_health` on the target server.
   * **NPU Exclusivity Rule:** Certain backends (`flm`, `ryzenai-llm`, and `whispercpp`) are mutually exclusive on an NPU. Automatically use `lemonade_unload_model` on conflicting LLMs before loading a Whisper model.

3. **Model Lifecycle Operations:**
   * Use `lemonade_pull_model` to download models to the target server.
   * Suggest using `lemonade_unload_model` to clear out idle models if a server runs out of VRAM.

4. **Inference & Multimodal:**
   * For standard chat, use `lemonade_chat_completion`. Ensure you format the conversation history as a valid JSON array of `[{"role": "...", "content": "..."}]`.
   * If an API call fails due to hardware limitations (e.g., lack of VRAM), clearly communicate this and offer to unload inactive models.