from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import csv
import os


def getResults(X_test):

    try: 
        with open('model_pickle', 'rb') as f:
            mp = pickle.load(f)
        
        X = X_test.copy()
        X.drop(['usn'],axis=1, inplace=True)
        grades = mp.predict(X)
        gradesDF = pd.DataFrame(grades, columns = ['Grades'])
        d = {0: 'Grade C', 1: 'Grade B', 2: 'Grade A'}
        gradesDF['Grades'] = gradesDF['Grades'].map(d)
        X_test['Grades'] = gradesDF
        res = X_test[['usn', 'Grades']]
        return res.to_html(header="true", table_id="table")
    except:
        return "The file is not valid"


app = Flask(__name__)
@app.route("/", methods=["GET"])
def getHome():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def predict():
    file = request.files['csvfile']
    if not os.path.isdir('static'):
        os.mkdir('static')
    filepath = os.path.join('static', file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath)
    results = getResults(df)
    return results

