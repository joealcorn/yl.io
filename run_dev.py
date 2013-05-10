from ylio import app
app.run(debug=app.config.get('DEBUG', True))
