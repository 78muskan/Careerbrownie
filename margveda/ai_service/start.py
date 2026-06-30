import os
import sys

port = int(os.environ.get("PORT", 8080))

import uvicorn

uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")
