import application

if __name__ == '__main__':
    app = application.create_app()
    app.run('0.0.0.0')
