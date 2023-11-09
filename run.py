import logging
from app import app

if __name__ == '__main__':
    # Configurar el registro para la aplicación Flask
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    # Ahora, cuando inicies tu aplicación, Flask y Werkzeug deberían registrar mensajes de depuración.
    app.run(debug=True)
