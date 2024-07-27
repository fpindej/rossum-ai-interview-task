from app import create_app, Config

app = create_app()

if __name__ == '__main__':
    app.config.from_object(Config)
    app.run(debug=Config.DEBUG, port=Config.PORT)
