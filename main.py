from enum import unique
from flask import Flask, json, render_template, jsonify, redirect, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "akumakanmierebus"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SchoolData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(250), unique=False)
    teacher_name = db.Column(db.String(250), unique=True)
    rating = db.Column(db.Float, unique=True)

db.create_all()


@app.route('/')
def home():
    data = db.session.query(SchoolData).all()
    return render_template("index.html", data=data)

@app.route('/add_site')
def add_site():
    data = db.session.query(SchoolData).all()
    return render_template("add.html", data=data)

@app.route('/random', methods=['GET'])
def random_material():
    data = db.session.query(SchoolData).all()
    material = random.choice(data)
    return jsonify(jawis2_random_material={
        "id": material.id,
        "material name": material.material,
        "teacher name": material.teacher_name,
        "rating": material.rating,
    })

@app.route('/byid/<id>', methods=['GET'])
def take_materialby_id(id):
    material = SchoolData.query.get(id)
    return jsonify(jawis2_random_material={
        "id": material.id,
        "material name": material.material,
        "teacher name": material.teacher_name,
        "rating": material.rating,
    })


@app.route('/all', methods=['GET'])
def all_material():
    data = db.session.query(SchoolData).all()
    material_data = []
    for i in data:
        jawis2={
        "id":i.id,
        "material name":i.material,
        "teacher name":i.teacher_name,
        "rating":i.rating,
    }
        material_data.append(jawis2)
    return jsonify(School materials=material_data)


@app.route('/add_material', methods=['POST', "GET"])
def add_material():
    key = request.form.get('secret_key')
    if key == "nasigorengtelorceplok":
        new_data = SchoolData(
            material = request.form.get('name'),
            teacher_name = request.form.get('teacher'),
            rating = float(request.form.get('rating')),
        )
        db.session.add(new_data)
        db.session.commit()
        return jsonify(result={
            "status":200,
            "reason":"The data is submited..."
        })
    else:
        return jsonify(result={
            "status":400,
            "reason":"Key Error, Please check your Key"
        })

@app.route('/update_rating', methods=['POST', "PATCH"])
def update_rating():
    key = request.form.get('secret_key')
    id = request.form.get('id')
    new_rating = request.form.get('rating')
    if key == "nasigorengtelordadar":
        material = SchoolData.query.get(id)
        material.rating = float(new_rating)
        db.session.commit()
        return jsonify(result={
            "status":200,
            "reason":"The data is updated..."
        })
    else:
        return jsonify(result={
            "status":400,
            "reason":"Key Error, Please check your Key"
        })

@app.route('/delete_material', methods=['POST', "DELETE"])
def delete_material():
    key = request.form.get('secret_key')
    print(key)
    id = request.form.get('id') 
    if key == "nasigorengpedes":
        material = SchoolData.query.get(int(id))
        db.session.delete(material)
        db.session.commit()
        return jsonify(response={
            "status": 200,
            "success":"Success to delete material from API..."
        })
    else:
        return jsonify(response={
            "status": 404,
            "reason":"Key Error, Please check your Key"
        })

if __name__ == "__main__":
    app.run(debug=True)