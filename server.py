import os
import random
import time
import socket
from django.http import StreamingHttpResponse, HttpResponse
from django.conf import settings
from django.urls import path
from django.core.wsgi import get_wsgi_application
from django.shortcuts import render

# Константа для разделителя кадров
FRAME_SEPARATOR = "--space--"

# Настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = 'your-secret-key-here'
DEBUG = True
ALLOWED_HOSTS = ['*']  # Разрешаем доступ со всех хостов
INSTALLED_APPS = ['django.contrib.staticfiles']
ROOT_URLCONF = __name__
STATIC_URL = '/static/'
ANIMATIONS_DIR = os.path.join(BASE_DIR, 'animations')
FRAME_HEIGHT = 30

# Настройка шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
    },
]

def get_local_ip():
    """Получение локального IP-адреса"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def generate_chunks(anim_id):
    animation_file = os.path.join(ANIMATIONS_DIR, f"{anim_id}.txt")
    
    if os.path.exists(animation_file):
        with open(animation_file, 'r', encoding='utf-8') as f:
            frames = f.read().split(FRAME_SEPARATOR)
            while True:
                for frame in frames:
                    lines = frame.strip().split('\n')
                    if len(lines) < FRAME_HEIGHT:
                        lines = [' ' * len(lines[0])] * (FRAME_HEIGHT - len(lines)) + lines
                    lines = lines[:FRAME_HEIGHT]
                    lines.append('-' * len(lines[0]))
                    padded_frame = '\n'.join(lines)
                    yield f"{padded_frame}\r\n\r\n"
                    time.sleep(0.2)
    else:
        available_animations = [f[:-4] for f in os.listdir(ANIMATIONS_DIR) 
                              if f.endswith('.txt')]
        if available_animations:
            random_anim = random.choice(available_animations)
            message = f"Animation {anim_id}.txt not found.\nTry this one:\ncurl http://{get_local_ip()}:8000/{random_anim}/"
        else:
            message = "Animation not found. No animations available."
        yield message

def stream_animation(request, anim_id="1"):
    animation_file = os.path.join(ANIMATIONS_DIR, f"{anim_id}.txt")
    if os.path.exists(animation_file):
        response = StreamingHttpResponse(
            generate_chunks(anim_id),
            content_type='text/plain; charset=utf-8'
        )
    else:
        response = HttpResponse(
            next(generate_chunks(anim_id)),
            content_type='text/plain; charset=utf-8'
        )
    return response

def index(request):
    available_animations = [f[:-4] for f in os.listdir(ANIMATIONS_DIR) 
                          if f.endswith('.txt')]
    local_ip = get_local_ip()
    
    # Проверяем, является ли запрос от curl
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    if 'curl' in user_agent:
        # Формируем текстовый список анимаций для curl
        if available_animations:
            response_text = "Available animations:\n" + "\n".join(
                f"curl http://{local_ip}:8000/{anim_id}/" for anim_id in available_animations
            )
        else:
            response_text = "No animations available."
        return HttpResponse(response_text, content_type='text/plain; charset=utf-8')
    
    # Для браузера рендерим шаблон
    return render(request, 'index.jinja2', {'animations': available_animations, 'ip': local_ip})

urlpatterns = [
    path('<str:anim_id>/', stream_animation, name='stream_animation'),
    path('', index, name='index'),
]

application = get_wsgi_application()

lip = ''

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    local_ip = get_local_ip()
    lip = local_ip
    print(f"Starting server on {local_ip}:8000...")
    print(f"Visit: http://{local_ip}:8000/ for the main page")
    print(f"Or try: curl http://{local_ip}:8000/1/")
    execute_from_command_line(['', 'runserver', '0.0.0.0:8000'])  # Слушаем все интерфейсы