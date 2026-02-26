set -o errexit

# Install/upgrade setuptools first to ensure pkg_resources is available
pip install --upgrade setuptools

pip install -r requirements.txt

python manage.py collectstatic --noinput 
python manage.py migrate --noinput