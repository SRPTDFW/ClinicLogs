import os
import io
import csv
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me-in-production')

db_url = os.environ.get('DATABASE_URL', 'sqlite:///clinic.db')
if db_url.startswith('postgres://'):  # some providers hand out the old-style URL
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
if db_url.startswith('postgresql://') and '+psycopg' not in db_url:
    db_url = db_url.replace('postgresql://', 'postgresql+psycopg://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

DEFAULT_CLINICS = ["Weatherford", "Ponder", "Bridgeport", "Decatur", "Springtown",
                    "Willow Park", "Conroe", "North Richland Hills", "Rhome"]
DEFAULT_CLINIC_PASSCODE = os.environ.get('DEFAULT_CLINIC_PASSCODE', 'clinic123')
ADMIN_PASSCODE = os.environ.get('ADMIN_PASSCODE', 'admin123')


# ---------------- models ----------------
class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    passcode_hash = db.Column(db.String(255), nullable=False)


class TempReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    value = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(255))


class ChemicalUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(80))
    qty = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(40))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    done = db.Column(db.Boolean, default=False)


class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(200))


def get_setting(key, default=None):
    s = Setting.query.filter_by(key=key).first()
    return s.value if s else default


def set_setting(key, value):
    s = Setting.query.filter_by(key=key).first()
    if not s:
        s = Setting(key=key, value=str(value))
        db.session.add(s)
    else:
        s.value = str(value)
    db.session.commit()


def seed():
    db.create_all()
    for name in DEFAULT_CLINICS:
        if not Clinic.query.filter_by(name=name).first():
            db.session.add(Clinic(name=name, passcode_hash=generate_password_hash(DEFAULT_CLINIC_PASSCODE)))
    db.session.commit()
    if get_setting('range_min') is None:
        set_setting('range_min', 158)
    if get_setting('range_max') is None:
        set_setting('range_max', 167)


with app.app_context():
    seed()


# ---------------- auth ----------------
def login_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if not session.get('clinic_id') and not session.get('is_admin'):
            return redirect(url_for('login'))
        return f(*a, **kw)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if not session.get('is_admin'):
            return redirect(url_for('login'))
        return f(*a, **kw)
    return wrapper


def current_clinic_id():
    return session.get('clinic_id')


# ---------------- pages ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        mode = request.form.get('mode')
        if mode == 'admin':
            if request.form.get('passcode', '') == ADMIN_PASSCODE:
                session.clear()
                session['is_admin'] = True
                return redirect(url_for('admin'))
            error = 'Incorrect admin passcode.'
        else:
            clinic_name = request.form.get('clinic')
            passcode = request.form.get('passcode', '')
            clinic = Clinic.query.filter_by(name=clinic_name).first()
            if clinic and check_password_hash(clinic.passcode_hash, passcode):
                session.clear()
                session['clinic_id'] = clinic.id
                session['clinic_name'] = clinic.name
                return redirect(url_for('index'))
            error = 'Incorrect clinic or passcode.'
    clinics = Clinic.query.order_by(Clinic.name).all()
    return render_template('login.html', clinics=clinics, error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    if session.get('is_admin'):
        return redirect(url_for('admin'))
    return render_template('index.html', clinic_name=session.get('clinic_name'))


@app.route('/admin')
@admin_required
def admin():
    clinics = Clinic.query.order_by(Clinic.name).all()
    return render_template('admin.html', clinics=clinics,
                            range_min=get_setting('range_min', 158),
                            range_max=get_setting('range_max', 167))


@app.route('/admin/reset-passcode', methods=['POST'])
@admin_required
def admin_reset_passcode():
    clinic = Clinic.query.get(request.form.get('clinic_id'))
    new_pass = request.form.get('new_passcode')
    if clinic and new_pass:
        clinic.passcode_hash = generate_password_hash(new_pass)
        db.session.commit()
    return redirect(url_for('admin'))


@app.route('/admin/range', methods=['POST'])
@admin_required
def admin_range():
    set_setting('range_min', request.form.get('range_min'))
    set_setting('range_max', request.form.get('range_max'))
    return redirect(url_for('admin'))


# ---------------- API ----------------
@app.route('/api/range')
@login_required
def api_range():
    return jsonify({'min': float(get_setting('range_min', 158)), 'max': float(get_setting('range_max', 167))})


@app.route('/api/entries')
@login_required
def api_entries():
    clinic_id = request.args.get('clinic_id') if session.get('is_admin') else current_clinic_id()
    d = request.args.get('date')
    temps = TempReading.query.filter_by(clinic_id=clinic_id, date=d).order_by(TempReading.id).all()
    chems = ChemicalUsage.query.filter_by(clinic_id=clinic_id, date=d).order_by(ChemicalUsage.id).all()
    tasks = Task.query.filter_by(clinic_id=clinic_id, date=d).order_by(Task.id).all()
    return jsonify({
        'temps': [{'id': t.id, 'time': t.time, 'value': t.value, 'note': t.note} for t in temps],
        'chemicals': [{'id': c.id, 'name': c.name, 'category': c.category, 'qty': c.qty, 'unit': c.unit} for c in chems],
        'tasks': [{'id': t.id, 'text': t.text, 'done': t.done} for t in tasks],
    })


@app.route('/api/temps', methods=['POST'])
@login_required
def add_temp():
    data = request.json
    t = TempReading(clinic_id=current_clinic_id(), date=data['date'], time=data['time'],
                     value=float(data['value']), note=data.get('note', ''))
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id})


@app.route('/api/temps/<int:id>', methods=['DELETE'])
@login_required
def del_temp(id):
    t = TempReading.query.filter_by(id=id, clinic_id=current_clinic_id()).first()
    if t:
        db.session.delete(t)
        db.session.commit()
    return jsonify({'ok': True})


@app.route('/api/chemicals', methods=['POST'])
@login_required
def add_chem():
    data = request.json
    c = ChemicalUsage(clinic_id=current_clinic_id(), date=data['date'], name=data['name'],
                       category=data.get('category'), qty=float(data['qty']), unit=data.get('unit'))
    db.session.add(c)
    db.session.commit()
    return jsonify({'id': c.id})


@app.route('/api/chemicals/<int:id>', methods=['DELETE'])
@login_required
def del_chem(id):
    c = ChemicalUsage.query.filter_by(id=id, clinic_id=current_clinic_id()).first()
    if c:
        db.session.delete(c)
        db.session.commit()
    return jsonify({'ok': True})


@app.route('/api/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.json
    t = Task(clinic_id=current_clinic_id(), date=data['date'], text=data['text'], done=False)
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id})


@app.route('/api/tasks/<int:id>', methods=['PATCH'])
@login_required
def patch_task(id):
    data = request.json
    t = Task.query.filter_by(id=id, clinic_id=current_clinic_id()).first()
    if t:
        t.done = data.get('done', t.done)
        db.session.commit()
    return jsonify({'ok': True})


@app.route('/api/tasks/<int:id>', methods=['DELETE'])
@login_required
def del_task(id):
    t = Task.query.filter_by(id=id, clinic_id=current_clinic_id()).first()
    if t:
        db.session.delete(t)
        db.session.commit()
    return jsonify({'ok': True})


@app.route('/api/clinics')
@admin_required
def api_clinics():
    return jsonify([{'id': c.id, 'name': c.name} for c in Clinic.query.order_by(Clinic.name).all()])


def _history_rows(clinic_filter=None):
    q_temps, q_chems, q_tasks = TempReading.query, ChemicalUsage.query, Task.query
    if not session.get('is_admin'):
        cid = current_clinic_id()
        q_temps = q_temps.filter_by(clinic_id=cid)
        q_chems = q_chems.filter_by(clinic_id=cid)
        q_tasks = q_tasks.filter_by(clinic_id=cid)
    elif clinic_filter and clinic_filter != 'all':
        q_temps = q_temps.filter_by(clinic_id=clinic_filter)
        q_chems = q_chems.filter_by(clinic_id=clinic_filter)
        q_tasks = q_tasks.filter_by(clinic_id=clinic_filter)

    clinics = {c.id: c.name for c in Clinic.query.all()}
    days = {}
    for t in q_temps.all():
        days.setdefault((t.clinic_id, t.date), {'temps': [], 'chemicals': [], 'tasks': []})['temps'].append(
            {'value': t.value, 'time': t.time})
    for c in q_chems.all():
        days.setdefault((c.clinic_id, c.date), {'temps': [], 'chemicals': [], 'tasks': []})['chemicals'].append(
            {'name': c.name, 'qty': c.qty, 'unit': c.unit})
    for tk in q_tasks.all():
        days.setdefault((tk.clinic_id, tk.date), {'temps': [], 'chemicals': [], 'tasks': []})['tasks'].append(
            {'done': tk.done})

    rows = []
    for (cid, d), val in sorted(days.items(), key=lambda kv: kv[0][1], reverse=True):
        rows.append({
            'clinic': clinics.get(cid, 'Unknown'),
            'date': d,
            'temps': val['temps'],
            'chemicals': val['chemicals'],
            'tasks_done': sum(1 for t in val['tasks'] if t['done']),
            'tasks_total': len(val['tasks']),
        })
    return rows


@app.route('/api/history')
@login_required
def api_history():
    return jsonify(_history_rows(request.args.get('clinic_id')))


@app.route('/api/export.csv')
@login_required
def export_csv():
    rows = _history_rows(request.args.get('clinic_id'))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Clinic', 'Temp Readings', 'Chemicals Used', 'Tasks Done'])
    for row in rows:
        temps_str = '; '.join(f"{t['value']}F@{t['time']}" for t in row['temps'])
        chem_str = '; '.join(f"{c['name']} ({c['qty']}{c['unit']})" for c in row['chemicals'])
        writer.writerow([row['date'], row['clinic'], temps_str, chem_str,
                          f"{row['tasks_done']}/{row['tasks_total']}"])
    mem = io.BytesIO(output.getvalue().encode('utf-8'))
    return send_file(mem, mimetype='text/csv', as_attachment=True, download_name='srpt-clinic-log-export.csv')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
