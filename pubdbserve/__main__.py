from pubdbserve import app
import uvicorn
import sys

uvicorn.run(app, host="0.0.0.0", port=int(sys.argv[1]))
