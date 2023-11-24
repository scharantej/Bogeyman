 
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///children_horror_stories.db'
db = SQLAlchemy(app)

class HorrorStory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<HorrorStory %r>' % self.title

db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/horror_stories')
def horror_stories():
    horror_stories = HorrorStory.query.all()
    return render_template('horror_stories.html', horror_stories=horror_stories)

@app.route('/horror_stories/<int:horror_story_id>')
def horror_story(horror_story_id):
    horror_story = HorrorStory.query.get(horror_story_id)
    return render_template('horror_story.html', horror_story=horror_story)

@app.route('/add_horror_story', methods=['GET', 'POST'])
def add_horror_story():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_horror_story = HorrorStory(title=title, content=content)
        db.session.add(new_horror_story)
        db.session.commit()
        return redirect(url_for('horror_stories'))
    return render_template('add_horror_story.html')

@app.route('/edit_horror_story/<int:horror_story_id>', methods=['GET', 'POST'])
def edit_horror_story(horror_story_id):
    horror_story = HorrorStory.query.get(horror_story_id)
    if request.method == 'POST':
        horror_story.title = request.form['title']
        horror_story.content = request.form['content']
        db.session.commit()
        return redirect(url_for('horror_stories'))
    return render_template('edit_horror_story.html', horror_story=horror_story)

@app.route('/delete_horror_story/<int:horror_story_id>')
def delete_horror_story(horror_story_id):
    horror_story = HorrorStory.query.get(horror_story_id)
    db.session.delete(horror_story)
    db.session.commit()
    return redirect(url_for('horror_stories'))

if __name__ == '__main__':
    app.run(debug=True)
