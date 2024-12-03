from flask import Flask, request, render_template, redirect, url_for, send_from_directory 
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'jpg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Structure
YEARS = {
    "Primo anno": {
        "Biennio itis": ["Lingua e letteratura italiana", "Storia e geografia", "Lingua inglese", "Diritto ed economia", "Matematica", "Tecnologie informatiche", "Scienza della terra e biologia", "Fisica", "Chimica", "Tecnologie e tecniche di rappresentazione grafica", "Scienze e tecnologie applicate", "Scienze motorie e sportive"],
        "Scienze Applicate": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia - Storia", "Filosofia", "Disegno e storia dell'arte", "Biologia", "Chimica", "Fisica", "Scienze Motorie", "Matematica", "Informatica"],
        "Internazionale": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia - Storia", "Filosofia", "Disegno e storia dell'arte", "Biologia", "Chimica", "Fisica", "Scienze Motorie", "Matematica", "Informatica"],
        "Sportivo": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia -Storia", "Filosofia", "Diritto ed economia nello sport", "Biologia", "Chimica", "Fisica", "Discipline sportive", "Scienze motorie e sportive", "Matematica", "Informatica"],
    },
    "Secondo anno": {
        "Biennio itis": ["Lingua e letteratura italiana", "Storia e geografia", "Lingua inglese", "Diritto ed economia", "Matematica", "Tecnologie informatiche", "Scienza della terra e biologia", "Fisica", "Chimica", "Tecnologie e tecniche di rappresentazione grafica", "Scienze e tecnologie applicate", "Scienze motorie e sportive"],
        "Scienze Applicate": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia - Storia", "Filosofia", "Disegno e storia dell'arte", "Biologia", "Chimica", "Fisica", "Scienze Motorie", "Matematica", "Informatica"],
        "Internazionale": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia - Storia", "Filosofia", "Disegno e storia dell'arte", "Biologia", "Chimica", "Fisica", "Scienze Motorie", "Matematica", "Informatica"],
        "Sportivo": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia -Storia", "Filosofia", "Diritto ed economia nello sport", "Biologia", "Chimica", "Fisica", "Discipline sportive", "Scienze motorie e sportive", "Matematica", "Informatica"],
    },
    "Terzo anno": {
        "Scienze Applicate": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia - Storia", "Filosofia", "Disegno e storia dell'arte", "Biologia", "Chimica", "Fisica", "Scienze Motorie", "Matematica", "Informatica"],
        "Internazionale": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia - Storia", "Filosofia", "Disegno e storia dell'arte", "Biologia", "Chimica", "Fisica", "Scienze Motorie", "Matematica", "Informatica"],
        "Sportivo": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia -Storia", "Filosofia", "Diritto ed economia nello sport", "Biologia", "Chimica", "Fisica", "Discipline sportive", "Scienze motorie e sportive", "Matematica", "Informatica"],
        "Chimica": ["Italiano", "Storia", "Inglese", "Matematica", "Chimica Analitica", "Chimica Organica", "Tecn. chimiche e industriali", "Scienze Motorie"],
        "Elettronica robotica e telecomunicazioni": ["Italiano", "Storia", "Inglese", "Matematica", "Elettronica ed elettrotecnica", "Sistemi Automatici", "Tecn. e Progettaz. sistemi Elettronici", "Robotica e telecomunicazioni", "Scienze Motorie"],
        "Informatica e telecomunicazioni": ["Italiano", "Storia", "Inglese", "Matematica", "Informatica", "Sistemi e reti", "TPSIT", "Telecomunicazioni", "Scienze Motorie"],
        "Trasporti e logistica": ["Italiano", "Storia", "Inglese", "Matematica", "Logistica", "Meccanica, macchine", "Diritto ed economia", "Elettronica, elettrotecnica e automazione", "Scienza della navigazione", "Scienze Motorie"],
        "Meccanica, meccatronica ed energia": ["Italiano", "Storia", "Inglese", "Matematica", "Meccanica macchine ed energia", "Sistemi e automazione", "TMPP", "Impianti energetici, disegno e progett.", "Tecnologia dell'autoveicolo", "Scienze Motorie"],
    },
    "Quarto anno": {
        "Scienze Applicate": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia - Storia", "Filosofia", "Disegno e storia dell'arte", "Biologia", "Chimica", "Fisica", "Scienze Motorie", "Matematica", "Informatica"],
        "Internazionale": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia - Storia", "Filosofia", "Disegno e storia dell'arte", "Biologia", "Chimica", "Fisica", "Scienze Motorie", "Matematica", "Informatica"],
        "Sportivo": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia -Storia", "Filosofia", "Diritto ed economia nello sport", "Biologia", "Chimica", "Fisica", "Discipline sportive", "Scienze motorie e sportive", "Matematica", "Informatica"],
        "Chimica": ["Italiano", "Storia", "Inglese", "Matematica", "Chimica Analitica", "Chimica Organica", "Tecn. chimiche e industriali", "Scienze Motorie"],
        "Elettronica robotica e telecomunicazioni": ["Italiano", "Storia", "Inglese", "Matematica", "Elettronica ed elettrotecnica", "Sistemi Automatici", "Tecn. e Progettaz. sistemi Elettronici", "Robotica e telecomunicazioni", "Scienze Motorie"],
        "Informatica e telecomunicazioni": ["Italiano", "Storia", "Inglese", "Matematica", "Informatica", "Sistemi e reti", "TPSIT", "Telecomunicazioni", "Scienze Motorie"],
        "Trasporti e logistica": ["Italiano", "Storia", "Inglese", "Matematica", "Logistica", "Meccanica, macchine", "Diritto ed economia", "Elettronica, elettrotecnica e automazione", "Scienza della navigazione", "Scienze Motorie"],
        "Meccanica, meccatronica ed energia": ["Italiano", "Storia", "Inglese", "Matematica", "Meccanica macchine ed energia", "Sistemi e automazione", "TMPP", "Impianti energetici, disegno e progett.", "Tecnologia dell'autoveicolo", "Scienze Motorie"],
    },
    "Quinto anno": {
        "Scienze Applicate": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia - Storia", "Filosofia", "Disegno e storia dell'arte", "Biologia", "Chimica", "Fisica", "Scienze Motorie", "Matematica", "Informatica"],
        "Internazionale": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia - Storia", "Filosofia", "Disegno e storia dell'arte", "Biologia", "Chimica", "Fisica", "Scienze Motorie", "Matematica", "Informatica"],
        "Sportivo": ["Lingua e letteratura italiana", "Inglese", "Storia e geografia -Storia", "Filosofia", "Diritto ed economia nello sport", "Biologia", "Chimica", "Fisica", "Discipline sportive", "Scienze motorie e sportive", "Matematica", "Informatica"],
        "Chimica": ["Italiano", "Storia", "Inglese", "Matematica", "Chimica Analitica", "Chimica Organica", "Tecn. chimiche e industriali", "Scienze Motorie"],
        "Elettronica robotica e telecomunicazioni": ["Italiano", "Storia", "Inglese", "Matematica", "Elettronica ed elettrotecnica", "Sistemi Automatici", "Tecn. e Progettaz. sistemi Elettronici", "Robotica e telecomunicazioni", "Scienze Motorie"],
        "Informatica e telecomunicazioni": ["Italiano", "Storia", "Inglese", "Matematica", "Informatica", "Sistemi e reti", "TPSIT", "Telecomunicazioni", "Scienze Motorie"],
        "Trasporti e logistica": ["Italiano", "Storia", "Inglese", "Matematica", "Logistica", "Meccanica, macchine", "Diritto ed economia", "Elettronica, elettrotecnica e automazione", "Scienza della navigazione", "Scienze Motorie"],
        "Meccanica, meccatronica ed energia": ["Italiano", "Storia", "Inglese", "Matematica", "Meccanica macchine ed energia", "Sistemi e automazione", "TMPP", "Impianti energetici, disegno e progett.", "Tecnologia dell'autoveicolo", "Scienze Motorie"],
    },
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', years=YEARS)

# serve uploaded files
@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/view/<year>/<subject>/<topic>')
def view_notes(year, subject, topic):
    path = os.path.join(app.config['UPLOAD_FOLDER'], year, subject, topic)
    if os.path.exists(path):
        files = os.listdir(path)
    else:
        files = []
    return render_template('view.html', year=year, subject=subject, topic=topic, files=files)

@app.route('/viewyear/<year>')
def view_year(year):
    return render_template('viewyear.html', macroyear=year, years=YEARS[year])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        year = request.form['year']
        subject = request.form['subject']
        topic = request.form['topic']
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], year, subject, topic)
            os.makedirs(save_path, exist_ok=True)
            file.save(os.path.join(save_path, filename))
            return redirect(url_for('view_notes', year=year, subject=subject, topic=topic))
    return render_template('upload.html', years=YEARS)



if __name__ == '__main__':
    app.run(debug=True)
