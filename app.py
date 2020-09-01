from music.app_factory import create_app


if __name__ == "__main__":
    app = create_app()

    app.run(port=app.config['PORT'], host='0.0.0.0')