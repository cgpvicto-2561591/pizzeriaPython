import os
from flask import Flask, render_template, request, session
import mysql.connector
from dotenv import load_dotenv
import mysql.connector



load_dotenv()
app = Flask(__name__)
#app.secret pour utiliser mes variables session
#python3 -c "import secrets; print(secrets.token_urlsafe(32))"
app.secret_key = os.getenv("SECRET_KEY")

#autre source utiliser: 
#https://flask.palletsprojects.com/en/stable/
#https://jinja.palletsprojects.com/en/stable/
#utilisation AI pour question compréhension
#utilisation AI javas
"""
==================================================================
        def
==================================================================
"""

""" **********      affichage data commande complete             ********** """
"""
SELECT com.id as commande_id, com.numero_commande, com.statut, c.nom as client_nom, c.numero_telephone, c.adresse_livraison, tc.nom as croute_nom, ts.nom as sauce_nom
FROM commande as com 
INNER JOIN client as c ON com.client_id = c.id
INNER JOIN pizza as p ON com.pizza_id = p.id
INNER JOIN type_croute as tc ON p.croute_id = tc.id
INNER JOIN type_sauce as ts ON p.sauce_id = ts.id 
WHERE com.statut = %(statut)s


SELECT com.id AS commande_id, i.nom AS ingredient_nom
FROM commande AS com
INNER JOIN pizza AS p ON com.pizza_id = p.id
INNER JOIN liste_garniture AS lg ON lg.pizza_id = p.id
INNER JOIN ingredient AS i ON lg.ingredient_id = i.id;

"""


def afficher_liste_commande_en_preparation():
    #'En préparation', 'En chemin', 'Livré'
    cursor = db.cursor(dictionary=True)

    requete = "SELECT com.id as commande_id, com.numero_commande, com.statut, c.nom as client_nom, c.numero_telephone, c.adresse_livraison, tc.nom as croute_nom, ts.nom as sauce_nom FROM commande as com INNER JOIN client as c ON com.client_id = c.id INNER JOIN pizza as p ON com.pizza_id = p.id INNER JOIN type_croute as tc ON p.croute_id = tc.id INNER JOIN type_sauce as ts ON p.sauce_id = ts.id WHERE com.statut = %(statut)s"

    requete2 = "SELECT com.id AS commande_id, i.nom AS ingredient_nom FROM commande AS com INNER JOIN pizza AS p ON com.pizza_id = p.id INNER JOIN liste_garniture AS lg ON lg.pizza_id = p.id INNER JOIN ingredient AS i ON lg.ingredient_id = i.id WHERE com.statut = %(statut)s;"
    
    parametre = {
        "statut": "En préparation"
    }

   
    try:
        cursor.execute(requete, parametre)
        commandePrep = cursor.fetchall()
        cursor.execute(requete2, parametre)
        listIngredient = cursor.fetchall()

    except  Exception as e:
        db.rollback()
        return f"Erreur : {e}"
    finally:    
        cursor.close()
    return commandePrep, listIngredient

def afficher_liste_commande_en_chemin():
    #'En préparation', 'En chemin', 'Livré'
    cursor = db.cursor(dictionary=True)

    requete = "SELECT com.id as commande_id, com.numero_commande, com.statut, c.nom as client_nom, c.numero_telephone, c.adresse_livraison, tc.nom as croute_nom, ts.nom as sauce_nom FROM commande as com INNER JOIN client as c ON com.client_id = c.id INNER JOIN pizza as p ON com.pizza_id = p.id INNER JOIN type_croute as tc ON p.croute_id = tc.id INNER JOIN type_sauce as ts ON p.sauce_id = ts.id WHERE com.statut = %(statut)s"

    requete2 = "SELECT com.id AS commande_id, i.nom AS ingredient_nom FROM commande AS com INNER JOIN pizza AS p ON com.pizza_id = p.id INNER JOIN liste_garniture AS lg ON lg.pizza_id = p.id INNER JOIN ingredient AS i ON lg.ingredient_id = i.id WHERE com.statut = %(statut)s;"

    parametre = {
        "statut": "En chemin"
    }
    try:
        cursor.execute(requete, parametre)
        commandeChemin = cursor.fetchall()
        cursor.execute(requete2, parametre)
        listIngredient = cursor.fetchall()
    except  Exception as e:
        db.rollback()
        return f"Erreur : {e}"
    finally:    
        cursor.close()
    return commandeChemin, listIngredient

def afficher_liste_commande_livre():
    #'En préparation', 'En chemin', 'Livré'
    cursor = db.cursor(dictionary=True)

    requete = "SELECT com.id as commande_id, com.numero_commande, com.statut, c.nom as client_nom, c.numero_telephone, c.adresse_livraison, tc.nom as croute_nom, ts.nom as sauce_nom FROM commande as com INNER JOIN client as c ON com.client_id = c.id INNER JOIN pizza as p ON com.pizza_id = p.id INNER JOIN type_croute as tc ON p.croute_id = tc.id INNER JOIN type_sauce as ts ON p.sauce_id = ts.id WHERE com.statut = %(statut)s"

    requete2 = "SELECT com.id AS commande_id, i.nom AS ingredient_nom FROM commande AS com INNER JOIN pizza AS p ON com.pizza_id = p.id INNER JOIN liste_garniture AS lg ON lg.pizza_id = p.id INNER JOIN ingredient AS i ON lg.ingredient_id = i.id WHERE com.statut = %(statut)s;"
    parametre = {
        "statut": "Livré"
    }
    try:
        cursor.execute(requete, parametre)
        commandeLivre = cursor.fetchall()
        cursor.execute(requete2, parametre)
        listIngredient = cursor.fetchall()
    except  Exception as e:
        db.rollback()
        return f"Erreur : {e}"
    finally:    
        cursor.close()
    return commandeLivre, listIngredient

""" **********      enregistrement data              ********** """

def enregistre_commande_bd(dataClient, dataPizza):
    cursor = db.cursor(dictionary=True)
    
    requeteClient = "INSERT INTO client(nom, numero_telephone, adresse_livraison) VALUES (%(nom)s, %(numero_telephone)s, %(adresse_livraison)s)"

    parametresClient = {
    "nom": dataClient[0],
    "numero_telephone": dataClient[1],
    "adresse_livraison": dataClient[2]
    }

    requetePizza = "INSERT INTO pizza(croute_id, sauce_id) VALUES (%(croute_id)s, %(sauce_id)s)"
    parametresPizza = {
        "croute_id": dataPizza[0],
        "sauce_id": dataPizza[1]
    }

    requeteListeGarniture ="INSERT INTO liste_garniture(pizza_id, ingredient_id) VALUES(%(pizza_id)s, %(ingredient)s)"
    parametresGarniture ={
        "ingredient1_id": dataPizza[2],
        "ingredient2_id": dataPizza[3],
        "ingredient3_id": dataPizza[4],
        "ingredient4_id": dataPizza[5]
    }

    requeteCommande = "INSERT INTO commande(numero_commande, client_id, pizza_id) VALUES(%(numero_commande)s, %(client_id)s, %(pizza_id)s)"
  
    try:
    #insert table client
        cursor.execute(requeteClient, parametresClient)
        client_id = cursor.lastrowid
 
    #insert table pizza
        cursor.execute(requetePizza, parametresPizza)
        pizza_id = cursor.lastrowid 

    #insert dans liste_garniture
        for ingredient in parametresGarniture.values():
            if ingredient:
                parametres = {
                "pizza_id": pizza_id,
                "ingredient": ingredient
                }
                cursor.execute(requeteListeGarniture, parametres)
    #insert dans la commande 
        parametresCommande = {
            "numero_commande":  "pizza100" + str(pizza_id),
            "client_id": client_id,
            "pizza_id": pizza_id
        }
        cursor.execute(requeteCommande, parametresCommande)
        db.commit()
    except  Exception as e:
        db.rollback()
        return f"Erreur : {e}"
    finally:
        cursor.close()
    valide = "Votre commande à bien été valider!"
    return valide

""" **********      verification data              ********** """

def verrifer_data_type_croute(id, nom):
    cursor = db.cursor()
    requete = f"SELECT nom FROM type_croute WHERE id = %s AND nom = %s"
    cursor.execute(requete, (id, nom))
    resultat = cursor.fetchone()
    cursor.close()
    return resultat

def verrifer_data_type_sauce(id, nom):
    cursor = db.cursor()
    requete = f"SELECT nom FROM type_sauce WHERE id = %s AND nom = %s"
    cursor.execute(requete, (id, nom))
    resultat = cursor.fetchone()
    cursor.close()
    return resultat


def verrifer_data_ingredient(id, nom):
    cursor = db.cursor()
    requete = f"SELECT nom FROM ingredient WHERE id = %s AND nom = %s"
    cursor.execute(requete, (id, nom))
    resultat = cursor.fetchone()
    cursor.close()
    return resultat

def verifier_commande_statut(statut):
    # NOTE: J'aurais du faire une liste de Statut à coté un peu comme mes type_croute, type_sauce dans la bd 
    # Comme ca j'aurais pu faire la vérrification à partir de la bd 
    liste_statut = [
        "En préparation",
        "En chemin",
        "Livré"
    ]

    return statut in liste_statut

def verrifer_commande_id(id):
    cursor = db.cursor()
    parametre = {
        'id': id
    }
    requete = "SELECT id FROM commande WHERE id = %(id)s"
    cursor.execute(requete,parametre)
    data = cursor.fetchone()
    cursor.close()
    return data

""" **********      select de data              ********** """

def select_type_croute():
    cursor = db.cursor(dictionary=True)
    requete = "SELECT * FROM type_croute"
    try:
        cursor.execute(requete)
        data = cursor.fetchall()
        return data
    except Exception as e:
        return f"Erreur : {e}"
    finally:
        cursor.close()

def select_type_sauce():
    cursor = db.cursor(dictionary=True)
    requete = "SELECT * FROM type_sauce"
    try:
        cursor.execute(requete)
        data = cursor.fetchall()
        return data
    except Exception as e:
        return f"Erreur : {e}"
    finally:
        cursor.close()

def select_ingredient():
    cursor = db.cursor(dictionary=True)
    requete = "SELECT * FROM ingredient"
    try:
        cursor.execute(requete)
        data = cursor.fetchall()
        return data
    except Exception as e:
        return f"Erreur : {e}"
    finally:
        cursor.close()
"""
==================================================================
        Base de donnée
==================================================================
"""
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = int(os.getenv('DB_PORT'))

def connection():
    connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    port=db_port
    )
    return connection

# Configuration de la connexion à la base de données
db = connection()

"""
==================================================================
        Index
==================================================================
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
==================================================================
                Commande
==================================================================
"""
@app.route('/commande')
def commande(erreur=""):

    ingredient = select_ingredient()
    croute = select_type_croute()
    sauce = select_type_sauce()
    return render_template('commande.html', ingredient=ingredient, croute=croute, sauce=sauce, erreur=erreur)


@app.route('/commandeTraitement', methods=['POST'])
def commandeTraitement():
    try:
        croute_id, croute_nom = request.form.get('croute').split('|')
        sauce_id, sauce_nom = request.form.get('sauce').split('|')
        ing1_id, ing1_nom = request.form.get('ingredient1').split('|')
        ing2_id, ing2_nom = request.form.get('ingredient2').split('|')
        ing3_id, ing3_nom = request.form.get('ingredient3').split('|')
        ing4_id, ing4_nom = request.form.get('ingredient4').split('|')
    except Exception as e:
        erreur = "Vous devez remplir tout les choix si dessou"
        return commande(erreur)

    if verrifer_data_type_croute(croute_id, croute_nom):
        session['croute_id'] = croute_id
        session['croute'] = croute_nom
    else:
        return "Erreur : Type de croûte invalide", 404

    if verrifer_data_type_sauce(sauce_id, sauce_nom):
        session['sauce_id'] = sauce_id
        session['sauce'] = sauce_nom
    else:
        return "Erreur : Type de Sauce invalide", 404

    if verrifer_data_ingredient(ing1_id, ing1_nom):
        session['ingredient1_id'] = ing1_id
        session['ingredient1'] = ing1_nom
    else:
        return "Erreur : Type de ingredient invalide", 404

    if verrifer_data_ingredient(ing2_id, ing2_nom):
        session['ingredient2_id'] = ing2_id
        session['ingredient2'] = ing2_nom
    else:
        return "Erreur : Type de ingredient invalide", 404

    if verrifer_data_ingredient(ing3_id, ing3_nom):
        session['ingredient3_id'] = ing3_id
        session['ingredient3'] = ing3_nom
    else:
        return "Erreur : Type de ingredient invalide", 404

    if verrifer_data_ingredient(ing4_id, ing4_nom):
        session['ingredient4_id'] = ing4_id
        session['ingredient4'] = ing4_nom
    else:
        return "Erreur : Type de ingredient invalide", 404
    #NOTE : faire session.get(variable_session)|string pour acceder au valeur de variable session en jinja2
    return render_template('commandeTraitement.html')
"""
==================================================================
                Client
==================================================================
"""
@app.route('/commandeClient')
def commandeClient():
    return render_template('commandeClient.html')

@app.route('/commandeClientTraitement', methods=['POST'])
def commandeClientTraitement():
    try:
        session['clientnom'] = request.form.get('client_nom')
        session['clientNum'] = request.form.get('client_numero_telephone')
        session['clientAddr'] = request.form.get('client_adresse_livraison')
    except Exception as e:
            return f"Erreur : {e}"
    
    return render_template('commandeClientTraitement.html')
"""
==================================================================
                Confirmation
==================================================================
"""
@app.route('/confirmation')
def confirmation():
    return render_template('confirmationFinal.html')
"""
==================================================================
        History
==================================================================
"""
@app.route('/history')
def history(valide="", erreur=""):
    
    return render_template('history.html', valide=valide, erreur=erreur)

@app.route('/historyPreparation')
def historyPreparation():
    data, data2 = afficher_liste_commande_en_preparation()
    valide = ""
    if not data:
        valide = "Il n'y a aucune data"
    return render_template("historyPreparation.html", data=data, data2=data2, valide=valide)

@app.route('/historyChemin')
def historyChemin():
    data, data2 = afficher_liste_commande_en_chemin()
    valide = ""
    if not data:
        valide = "Il n'y a aucune data"
    return render_template("historyChemin.html", data=data, data2=data2, valide=valide)

@app.route('/historyLivre')
def historyLivre():
    data, data2 = afficher_liste_commande_livre()
    valide = ""
    if not data:
        valide = "Il n'y a aucune data"
    
    return render_template("historyLivre.html", data=data, data2=data2, valide=valide)

"""
==================================================================
        Status
==================================================================
"""
@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/modifierStatut', methods=['POST'])
def modifierStatut():
    print("JE rentre dans modifierStatut")
    cursor = db.cursor()
    modifier = request.form.get('modifier')
    supprimer = request.form.get('supprimer')
    valide = ""
    nv_commande_id = request.form.get('commande_id')
    nv_choix = request.form.get('modification_statut') 

    if verrifer_commande_id(nv_commande_id):
        commande_id = nv_commande_id
    else:
        erreur = "Nous n'avons pas pu traité la demande veuillez recommancer"
        return history(erreur=erreur)
    if verifier_commande_statut(nv_choix):
        choix = nv_choix
    else:
        erreur = "Nous n'avons pas pu traité la demande veuillez recommancer"
        return history(erreur=erreur)
    parametre = {
            "statut": choix,
            "commande_id": commande_id
        }

    if modifier:
        
        requete = "UPDATE commande SET statut = %(statut)s WHERE id = %(commande_id)s"

        try:
            cursor.execute(requete, parametre)
            db.commit()
            valide = "Le statut à bien été modifié"
        except Exception as e:
            db.rollback()
            return f"Erreur : {e}"
        finally:
            cursor.close()
        
    elif supprimer:
            requete = "SELECT client_id, pizza_id FROM commande WHERE id = %(commande_id)s"
            try:
                cursor.execute(requete, parametre)
                info = cursor.fetchone()
                parametre2 ={
                'client_id': info[0],
                'pizza_id': info[1]
                }
                cursor.execute("DELETE FROM liste_garniture WHERE pizza_id = %(pizza_id)s", parametre2)
                cursor.execute("DELETE FROM commande WHERE id = %(commande_id)s", parametre)
                cursor.execute("DELETE FROM pizza WHERE id = %(pizza_id)s", parametre2)
                cursor.execute("DELETE FROM client WHERE id = %(client_id)s", parametre2)
                db.commit()
            except Exception as e:
                db.rollback()
                return f"Erreur : {e}"
            finally:
                cursor.close()
                valide = "La commande a été supprimée"

    return history(valide=valide)
"""
==================================================================
        validation
==================================================================
"""
@app.route('/validation')
def validation():
    #client
    client_nom = session.get('clientnom')
    client_num = session.get('clientNum')
    client_addr = session.get('clientAddr')
    #pizza
    croute_id = session.get('croute_id')
    sauce_id = session.get('sauce_id')
    ingredient1_id = session.get('ingredient1_id')
    ingredient2_id = session.get('ingredient2_id')
    ingredient3_id = session.get('ingredient3_id')
    ingredient4_id = session.get('ingredient4_id')

    dataClient = [
        client_nom, client_num, client_addr
    ]

    dataPizza = [
        croute_id, sauce_id, ingredient1_id, ingredient2_id, ingredient3_id, ingredient4_id
    ]

    for x in dataPizza:
        if(x is None or x.strip() == ""):
            erreur = "Erreur information Pizza!"
            return render_template('commande.html', erreur=erreur)

    for x in dataClient:
        if(x is None or x.strip() == ""):
            erreur = "Erreur information Client"
            return render_template('commandeClient.html', erreur=erreur)

    valide = enregistre_commande_bd(dataClient, dataPizza)
    #https://stackoverflow.com/questions/27747578/how-do-i-clear-a-flask-session
    if valide:
        session.clear()
    return render_template('validation.html', valide=valide)

"""
==================================================================
                        Fin
==================================================================
"""

if __name__ == '__main__':
    app.run(debug=True)