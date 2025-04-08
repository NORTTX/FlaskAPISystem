from flask import Flask, jsonify, request, Response, g, render_template, send_from_directory
from website import create_app
import yaml
import traceback
import json
import time
import logging
import pymongo
import datetime
import os

LOGGING_FILE = "Nortt.log"
REQUST_FILE = "requests.log"
app = create_app()

##############################################
# Log tutma kodu
##############################################
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(REQUST_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

def logrequest(path, method, ip, statuscode, httpversion):
    currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logdata = f'{currenttime} - {ip} - - [{currenttime}] "{method} {path} {httpversion}" {statuscode} -'
    try:
        logging.info(logdata)
    except Exception as error:
        logging.error(f"Logging Error: {error}")

##############################################
# DB ve ayar işlemleri
##############################################
MONGO_PATH = "mongodb"
MONGO_PORT = 27017
MONGO_HOST = "localhost"
MONGO_DATA = "sistem"
LOGGING_FILE = "Nortt.log"
Norttclient = pymongo.MongoClient(f"{MONGO_PATH}://{MONGO_HOST}:{MONGO_PORT}/")

##############################################
# Sistem ayarları
##############################################
with open('nortt.yaml', 'r') as file:
    nortt = yaml.safe_load(file)

##############################################
# Routes
##############################################

@app.route('/')
def index():
    return "Ana Sayfa - Mevcut HTML dosyalarına doğrudan URL ile erişebilirsin."

@app.errorhandler(404)
def page_not_found(e):
    file_path = os.path.join('templates', '404.html')
    if os.path.exists(file_path):
        return Response(open(file_path, 'r', encoding='utf-8').read(), content_type='text/html'), 404
    return "404 Sayfası bulunamadı! Lütfen 404.html dosyasını templates klasörüne ekleyin.", 404

@app.route('/<page_name>')
def serve_page(page_name):
    file_path = os.path.join('templates', f"{page_name}.html")
    if os.path.exists(file_path):
        return Response(open(file_path, 'r', encoding='utf-8').read(), content_type='text/html')
    return page_not_found(None)  

@app.route('/<path:file_path>')
def serve_file(file_path):
    valid_extensions = ['.js', '.css']
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext not in valid_extensions:
        return serve_page(file_path)
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == os.path.basename(file_path) and file.endswith(tuple(valid_extensions)):
                full_path = os.path.join(root, file)
                content_type = 'application/javascript' if file_ext == '.js' else 'text/css'
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        return Response(f.read(), content_type=content_type)
                except Exception as e:
                    return f"Dosya okuma hatası: {str(e)}", 500
    
    return page_not_found(None) 

@app.route('/menu')
def show_menu():
    html_files = [f[:-5] for f in os.listdir('templates') if f.endswith('.html')]
    return "<br>".join([f"<a href='/{page}'>{page}</a>" for page in html_files])

if __name__ == '__main__':
    try:
        if nortt["mode"] == "dev":
            app.run(debug=nortt["debug"])
        else:
            from waitress import serve
            serve(
                app,
                host=nortt["host"],
                port=nortt["port"],
                threads=nortt["threads"],
                connection_limit=nortt["connectionlimit"],
                max_request_body_size=nortt["maxrequestbodysize"]
            )
    except Exception as error:
        print(str(error))
        traceback.print_exc()