# customer_purchases
A tool for its support team to look up clients by their ID number, in order to speed up calls and build loyalty with the best customers.
# higiapp
Aplicación web creada desde el backend para gestionar ventas de productos de higiene personal.

# stack
Aplicación web creada a través del framework Django, a continuación se detallan las primeras acciones con el proyecto, después de clonarlo

## 1. Crear un entorno virtual (venv)
    python3 -m venv *<nombre del entorno>* 

## 2. Activar venv -> *Debe estar en el mismo nivel del directorio venv*
    source *<nombre del entorno>*/bin/activate

## 3. Instalar el listado de los requerimientos
    pip install -r requirements.txt

## 4. Crear un archivo para variables de entorno
    touch .env

## 5. Crear migraciones
    python3 manage.py makemigrations

## 6. Ejecutar migraciones
    python3 manage.py migrate



