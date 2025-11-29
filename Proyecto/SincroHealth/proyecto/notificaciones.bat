@echo off
cd /d "C:\Users\lenovo ci5\Desktop\proyecto IS\abrancupos-main\Proyecto\SincroHealth\proyecto"
call ..\..\venv\Scripts\activate
python manage.py shell -c "from polls.tasks import enviar_notificaciones; enviar_notificaciones()"
