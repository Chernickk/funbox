# funbox

## to run tests:

python3 manage.py test --settings=funbox.test_settings

## run test server:

pip3 install -r requirements.txt \
python3 manage.py runserver

## minimum for run prod server

pip3 install gunicorn \
gunicorn funbox.wsgi
