Instalación
===========

Es requisito tener instalado `Python 3+ <http://www.python.org/>`_.

* **Usuarios de la librería**

    ``pip install git+http://ETSGIT1/Snakes/raccoon.git@{version}#egg=raccoon``

    Nota: se debe sustituir ``{version}`` por la versión que se desea utilizar.

* **Desarrolladores**

    1. Clonar el repositorio:
        ``git clone http://etsgit1/Snakes/raccoon.git``

    2. [Opcional] Crear entorno virtual
        ``mkvirtualenv -a "/path/to/raccoon/" --python=python3.5 raccoon``

    3. Instalar dependencias de raccoon:
        ``cd raccoon``

        ``pip install -r requirements.txt``
