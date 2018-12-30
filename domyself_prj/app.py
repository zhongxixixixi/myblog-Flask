from flask import Flask, render_template, request, redirect, url_for, session
import config
from exts import db
from models import User, Question, Comment
from decorators import login_required


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        ltele = request.form.get('l-tele')
        lpw = request.form.get('l-pw')
        luser = User.query.filter(User.telephone == ltele and User.password == lpw).first()
        if luser:
            session['user_id'] = luser.id
            session.permanent = True
            return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    if session.get('user_id'):
        session.pop('user_id')
        return redirect(url_for('login'))
    else:
        pass


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        rtele = request.form.get('r-tele')
        rname = request.form.get('r-name')
        rpw = request.form.get('r-pw')
        rpw1 = request.form.get('r-pw1')
        if User.query.filter(User.telephone == rtele).first():
            return '该号码已被注册，请更换号码！'
        elif rpw != rpw1:
            return '两次密码输入不一致，请核对！'
        else:
            ruser = User(telephone=rtele, username=rname, password=rpw)
            db.session.add(ruser)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        qtit = request.form.get('q-title')
        qcon = request.form.get('q-content')
        quser_id = session.get('user_id')
        qauthor = User.query.filter(User.id == quser_id).first()
        question1 = Question(title=qtit, content=qcon)
        question1.author = qauthor
        db.session.add(question1)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detial/<question_id>')
def detial(question_id):
    question2 = Question.query.filter(Question.id == question_id).first()
    count = len(question2.comments)
    return render_template('detial.html', question=question2, count=count)


@app.route('/comment/', methods=['POST'])
@login_required
def comment():
    dcon = request.form.get('d-content')
    duser_id = session.get('user_id')
    duser = User.query.filter(User.id == duser_id).first()
    dqid = request.form.get('d-qid')
    dquestion = Question.query.filter(Question.id == dqid).first()
    comment1 = Comment(content=dcon)
    comment1.author = duser
    comment1.question = dquestion
    db.session.add(comment1)
    db.session.commit()
    return redirect(url_for('detial', question_id=dqid))


@app.context_processor
def my_cp():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    if user:
        return {'user': user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
