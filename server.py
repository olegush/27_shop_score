import os

from app import app

host = os.environ.get('HOST')
port = int(os.environ.get('PORT', 5000))
app.run(host=host, port=port, use_reloader=True)
