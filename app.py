from flask import Flask, request, jsonify, render_template, redirect
from classeviva import User, RequestURLs
import json

app = Flask(__name__)
class_data = None
classeviva_user = None

## ====== PAGINE ====== ##

@app.route('/classe/<string:nome_classe>')
def classe(nome_classe: str):
    nome_classe = nome_classe.upper().replace("_", " ")

    if not nome_classe in class_data["classi"]:
        return render_template('errore.html', error="Classe non trovata", codice=404)
    
    return render_template('classe.html', classe=nome_classe, orario=load_data()["classi"][nome_classe])

@app.route('/utente/login')
def login():
    return render_template('login.html', user=classeviva_user)

## ====== FUNCTIONS ====== ##
def load_data():
    with open('orario.json', 'rb') as file:
        data = json.load(file)

        for nome_classe in data["classi"]:
            classe = {}
            for giorno in data["classi"][nome_classe]:
                materie = []
                for ora in range(1, 7, 1):
                    ora_attuale = 1
                    for idx, mat in enumerate(data["classi"][nome_classe][giorno]):
                        if mat["durata"] == 1:
                            if ora_attuale == ora: 
                                materie.append({
                                    "materia": mat["materia"],
                                    "insegnanti": mat["insegnanti"],
                                    "aula": mat["aula"],
                                    "durata": mat["durata"],
                                    "ora": ora,
                                    "seconda_ora": False
                                })
                                break 
                        else:
                            if ora_attuale == ora:
                                materie.append({
                                    "materia": mat["materia"],
                                    "insegnanti": mat["insegnanti"],
                                    "aula": mat["aula"],
                                    "durata": mat["durata"],
                                    "ora": ora,
                                    "seconda_ora": False
                                })
                                break
                            elif ora_attuale + 1 == ora:
                                materie.append({
                                    "materia": mat["materia"],
                                    "insegnanti": mat["insegnanti"],
                                    "aula": mat["aula"],
                                    "durata": mat["durata"],
                                    "ora": ora,
                                    "seconda_ora": True
                                })
                                break

                        ora_attuale += mat["durata"]
                classe[giorno] = materie
            data["classi"][nome_classe] = classe

    return data

## ====== API ====== ##

@app.route('/api/classe/<string:nome_classe>')
def classe_args(nome_classe: str):
    data = load_data()
    args = request.args.to_dict()

    nome_classe = nome_classe.upper().replace("_", " ")

    if not nome_classe in data["classi"]:
        return jsonify({"messaggio": "classe non trovata", "codice": 404}), 404

    output = data.copy()["classi"][nome_classe]

    if 'giorno' in args:
        if not args["giorno"] in output:
            return jsonify({"messaggio": "giorno non trovato", "codice": 404}), 404
        else:
            output = output[args["giorno"]]

    if 'materia' in args:
        if type(output) == list:
                materie = []
                for materia in output:
                    if materia["materia"].lower() == (args["materia"]).lower().replace("_", " "):
                        materie.append(materia)

                if len(materie) == 0:
                    return jsonify({"messaggio": "materia non trovata", "codice": 404}), 404
                
                output = materie
        else:
            giorni = {}
            for giorno in output:
                for materia in output[giorno]:
                    if materia["materia"].lower() == (args["materia"]).lower().replace("_", " "):
                        if giorno in giorni:
                            giorni[giorno].append(materia)
                        else:
                            giorni[giorno] = [materia]

            if giorni == {}:
                return jsonify({"messaggio": "materia non trovata", "codice": 404}), 404
            
            output = giorni

    if 'ora' in args:
        if type(output) == list:
                materie = []
                for materia in output:
                    if int(materia["ora"]) == int(args["ora"]):
                        materie.append(materia)

                if len(materie) == 0:
                    return jsonify({"messaggio": "ora non trovata", "codice": 404}), 404
                
                output = materie
        else:
            giorni = {}
            for giorno in output:
                for materia in output[giorno]:
                    if int(materia["ora"]) == int(args["ora"]):
                        if giorno in giorni:
                            giorni[giorno].append(materia)
                        else:
                            giorni[giorno] = [materia]

            if giorni == {}:
                return jsonify({"messaggio": "ora non trovata", "codice": 404}), 404

            output = giorni

    if 'insegnante' in args:
        if type(output) == list:
                materie = []
                for materia in output:
                    for insegnante in materia["insegnanti"]:
                        if insegnante.lower().split(".")[0] == args["insegnante"].lower().replace("_", " "):
                            materie.append(materia)
                            break

                if len(materie) == 0:
                    return jsonify({"messaggio": "insegnante non trovato", "codice": 404}), 404
                
                output = materie
        else:
            giorni = {}
            for giorno in output:
                for materia in output[giorno]:
                    for insegnante in materia["insegnanti"]:
                        if insegnante.lower().split(".")[0] == args["insegnante"].lower().replace("_", " "):
                            if giorno in giorni:
                                giorni[giorno].append(materia)
                            else:
                                giorni[giorno] = [materia]

            if giorni == {}:
                return jsonify({"messaggio": "insegnante non trovato", "codice": 404}), 404

            output = giorni

    
        
    
    return jsonify({"risultato": output, "codice": 200}), 200

@app.post('/api/auth/login')
def login_api():
    global classeviva_user

    data = request.get_json()

    user = User(data['uid'], data['pwd'])
    if 'ident' not in json.dumps(user.login()):
        return jsonify({"messaggio": "username o password errati", "codice": 404}), 404
    
    classeviva_user = user
    return ({"risultato": user.to_json(), "codice": 200}), 200

if __name__ == "__main__":
    app.run(port=5001, debug=True)
