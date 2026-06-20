from app import create_app
from app.config import APP_CONFIG

app = create_app()

if __name__ == "__main__":
    app.run(host=APP_CONFIG.host, port=APP_CONFIG.port)