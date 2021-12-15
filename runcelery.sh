cd /home/user/Documents/GitHub/dycon/
source venv/bin/activate
cd dycon_web
celery -A dycon_web worker --loglevel=info
