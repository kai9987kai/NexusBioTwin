from __future__ import annotations
import traceback
import sys
from pathlib import Path

# Add src to sys.path
sys.path.append(str(Path("src").absolute()))

try:
    from nexusbiotwin.server import app
    import uvicorn
    print("Dependencies loaded. Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
except Exception:
    traceback.print_exc()
    sys.exit(1)
