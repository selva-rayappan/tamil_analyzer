import os
import sys
from flask import Flask, render_template, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from tamil import utf8
from freqAnalysis import getLetterCount

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "worksheet.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class Literal(db.Model):
    title = db.Column(db.String(1000), unique=True, nullable=False, primary_key=True)
    length = db.Column(db.Integer)

    def __repr__(self):
        return f'(name={self.title}, age={self.length})'

@app.route('/', methods=["GET", "POST"])
def home():
    literals = None
    uyir_dict = {}
    mei_dict = {}
    uyirmei_dict = {}
    uyirkuril_dict = {}
    uyirnaedil_dict = {}
    uyirmeikuril_dict = {}
    uyirmeinaedil_dict = {}
    tamil_dict = {}
    string_inp = {}
    
    if request.form:
        try:
            literal = Literal(title=request.form.get("title"),length=len(request.form.get("title")))
            string_inp = request.form.get("title")
            #db.session.add(literal)
            #db.session.commit()
            uyir_dict,mei_dict,uyirmei_dict,uyirkuril_dict,uyirnaedil_dict,uyirmeikuril_dict,uyirmeinaedil_dict,tamil_dict = getLetterCount(string_inp)
            #uyir_dict=join("{}".format(v) for k, v in uyir_dict.items())
        except Exception as e:
            print("Failed to add book")
            print(e)
    #literals = Literal.query.all()
    return render_template("index.html", literals=literals,form_value=string_inp,uyir_value=uyir_dict,mei_value=mei_dict,uyirmei_value=uyirmei_dict,uyirkuril_value=uyirkuril_dict,uyirnaedil_value=uyirnaedil_dict,uyirmeikuril_value=uyirmeikuril_dict,uyirmeinaedil_value=uyirmeinaedil_dict,tamil_value=tamil_dict)
 
if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', debug=True)