#!/usr/bin/env python
from app.settings import (
    HOST,
    PORT
)
from app.web import create_app

if __name__ == '__main__':
    # manager.run(threaded=True)
    app = create_app()
    app.run(host=HOST, port=PORT, threaded=True)
