"""Gestion des "routes" FLASK et des données pour les allergie.
Fichier : gestion_allergies_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_RESTAU_164 import app
from APP_RESTAU_164.database.database_tools import DBconnection
from APP_RESTAU_164.erreurs.exceptions import *
from APP_RESTAU_164.allergie.gestion_allergies_wtf_forms import FormWTFAjouterAllergie
from APP_RESTAU_164.allergie.gestion_allergies_wtf_forms import FormWTFUpdateAllergie
from APP_RESTAU_164.allergie.gestion_allergies_wtf_forms import FormWTFDeleteAllergie

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les allergie.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/allergie_afficher/<string:order_by>/<int:current_selected_id_allergie>", methods=['GET', 'POST'])
def allergie_afficher(order_by, current_selected_id_allergie):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and current_selected_id_allergie == 0:
                    mc_afficher.execute("""SELECT id_allergie, nom_allergie, allergene_allergie, gravite_allergie, symptomes_allergie, precautions_allergie, traitement_allergie, notes_allergie 
                    FROM t_allergie ORDER BY id_allergie""")
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable

                    mc_afficher.execute("""SELECT id_allergie, nom_allergie, allergene_allergie, gravite_allergie, symptomes_allergie, precautions_allergie, traitement_allergie, notes_allergie 
                    FROM t_allergie WHERE id_allergie = %(value_id_allergie_selected)s""",
                                        {"value_id_allergie_selected": current_selected_id_allergie})
                else:
                    mc_afficher.execute("""SELECT id_allergie, nom_allergie, allergene_allergie, gravite_allergie, symptomes_allergie, precautions_allergie, traitement_allergie, notes_allergie 
                    FROM t_allergie ORDER BY id_allergie DESC""")

                data_allergies = mc_afficher.fetchall()

                print("data_allergies ", data_allergies, " Type : ", type(data_allergies))
                # Différencier les messages si la table est vide.
                if not data_allergies and current_selected_id_allergie == 0:
                    flash("""La table "t_allergie" est vide. !!""", "warning")
                elif not data_allergies and current_selected_id_allergie > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"L'allergie demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données allergie affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionPersonnesAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("allergie/allergie_afficher.html", data={"data_allergies": data_allergies})


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "allergie/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/allergie_ajouter", methods=['GET', 'POST'])
def allergie_ajouter_wtf():
    form_insert = FormWTFAjouterAllergie()
    if request.method == "POST":
        try:
            if form_insert.validate_on_submit():
                valeurs_insertion_dictionnaire = {"nom_allergie": form_insert.nom_allergie_wtf.data.lower(),
                                                  "allergene_allergie": form_insert.allergene_wtf.data.lower(),
                                                  "gravite_allergie": form_insert.gravite_wtf.data.lower(),
                                                  "symptomes_allergie": form_insert.symptomes_wtf.data.lower(),
                                                  "precautions_allergie": form_insert.precautions_wtf.data.lower(),
                                                  "traitement_allergie": form_insert.traitement_wtf.data.lower(),
                                                  "notes_allergie": form_insert.notes_wtf.data.lower()
                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_allergie = """INSERT INTO t_allergie (nom_allergie, allergene_allergie, gravite_allergie, symptomes_allergie, precautions_allergie, traitement_allergie, notes_allergie)
                 VALUES (%(nom_allergie)s, %(allergene_allergie)s, %(gravite_allergie)s, %(symptomes_allergie)s, %(precautions_allergie)s, %(traitement_allergie)s, %(notes_allergie)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_allergie, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('allergie_afficher', order_by='DESC', current_selected_id_allergie=0))

        except Exception as Exception_allergie_ajouter_wtf:
            raise ExceptionPersonnesAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{allergie_ajouter_wtf.__name__} ; "
                                            f"{Exception_allergie_ajouter_wtf}")

    return render_template("allergie/allergie_ajouter_wtf.html", form=form_insert)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "allergie" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "ingre_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "allergie/ingre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/allergie_update", methods=['GET', 'POST'])
def allergie_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_allergie_update = request.values['id_allergie_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateAllergie()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "ingre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.

            valeurs_update_dictionnaire = {"value_id_allergie": id_allergie_update,
                                           "nom_allergie": form_update.nom_allergie_wtf.data.lower(),
                                           "allergene_allergie": form_update.allergene_wtf.data.lower(),
                                           "gravite_allergie": form_update.gravite_wtf.data.lower(),
                                           "symptomes_allergie": form_update.symptomes_wtf.data.lower(),
                                           "precautions_allergie": form_update.precautions_wtf.data.lower(),
                                           "traitement_allergie": form_update.traitement_wtf.data.lower(),
                                           "notes_allergie": form_update.notes_wtf.data.lower()
                                           }

            print("valeur_update_dictionnaire ", valeurs_update_dictionnaire)

            str_sql_update_allergie = """UPDATE t_allergie SET nom_allergie = %(nom_allergie)s, 
            allergene_allergie = %(allergene_allergie)s, gravite_allergie = %(gravite_allergie)s, 
            symptomes_allergie = %(symptomes_allergie)s, precautions_allergie = %(precautions_allergie)s, 
            traitement_allergie = %(traitement_allergie)s, notes_allergie = %(notes_allergie)s 
            WHERE id_allergie = %(value_id_allergie)s """

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_allergie, valeurs_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(
                url_for('allergie_afficher', order_by="ASC", current_selected_id_allergie=id_allergie_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_allergie = "SELECT id_allergie, nom_allergie, allergene_allergie, gravite_allergie, symptomes_allergie, precautions_allergie, traitement_allergie, notes_allergie FROM t_allergie " \
                                  "WHERE id_allergie = %(value_id_allergie)s"
            valeur_select_dictionnaire = {"value_id_allergie": id_allergie_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_allergie, valeur_select_dictionnaire)

                data_allergies = mybd_conn.fetchall()
                allergie_to_update = data_allergies[0]
                data = {
                    "nom_allergie_wtf": allergie_to_update["nom_allergie"],
                    "allergene_wtf": allergie_to_update["allergene_allergie"],
                    "gravite_wtf": allergie_to_update["gravite_allergie"],
                    "symptomes_wtf": allergie_to_update["symptomes_allergie"],
                    "precautions_wtf": allergie_to_update["precautions_allergie"],
                    "traitement_wtf": allergie_to_update["traitement_allergie"],
                    "notes_wtf": allergie_to_update["notes_allergie"]
                }
                form_update = FormWTFUpdateAllergie(data=data)

    except Exception as Exception_allergie_update_wtf:
        raise ExceptionPersonneUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{allergie_update_wtf.__name__} ; "
                                      f"{Exception_allergie_update_wtf}")

    return render_template("allergie/allergie_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "allergie" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "ingre_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "allergie/ingre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/allergie_delete", methods=['GET', 'POST'])
def allergie_delete_wtf():
    btn_submit_del = None
    submit_btn_conf_del = True
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_allergie_delete = request.values['id_allergie_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteAllergie()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("allergie_afficher", order_by="ASC", current_selected_id_allergie=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "allergie/ingre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.

                flash(f"Effacer l'allergie de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True
                submit_btn_conf_del = False

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_allergie": id_allergie_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                # str_sql_delete_films_genre = """DELETE FROM t_genre_film WHERE fk_genre = %(value_id_genre)s"""
                str_sql_delete_id_allergie = """DELETE FROM t_allergie WHERE id_allergie = %(value_id_allergie)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_id_allergie, valeur_delete_dictionnaire)

                flash(f"Allergie définitivement effacé !!", "success")
                print(f"Allergie définitivement effacé !!")

                # afficher les données
                return redirect(url_for('allergie_afficher', order_by="ASC", current_selected_id_allergie=0))

        if request.method == "GET":
            print(id_allergie_delete, type(id_allergie_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            # str_sql_genres_films_delete = """SELECT id_genre_film, nom_film, id_genre, intitule_genre FROM t_genre_film
            #                                 INNER JOIN t_film ON t_genre_film.fk_film = t_film.id_film
            #                                 INNER JOIN t_genre ON t_genre_film.fk_genre = t_genre.id_genre
            #                                 WHERE fk_genre = %(value_id_genre)s"""

            with DBconnection() as mydb_conn:
                # mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                # data_films_attribue_genre_delete = mydb_conn.fetchall()
                # print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)
                #
                # # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # # le formulaire "allergie/ingre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                # session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_genre = "SELECT id_allergie, nom_allergie, allergene_allergie, gravite_allergie, symptomes_allergie, precautions_allergie, traitement_allergie, notes_allergie " \
                                   "FROM t_allergie WHERE id_allergie = %(value_id_allergie)s"

                mydb_conn.execute(str_sql_id_genre, {"value_id_allergie": id_allergie_delete})
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE

            # Le bouton pour l'action "DELETE" dans le form. "ingre_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_allergie_delete_wtf:
        raise ExceptionPersonneDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{allergie_delete_wtf.__name__} ; "
                                      f"{Exception_allergie_delete_wtf}")

    return render_template("allergie/allergie_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           submit_btn_conf_del=submit_btn_conf_del)
