"""Gestion des "routes" FLASK et des données pour les allergie.
Fichier : gestion_allergies_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.personnes.gestion_personnes_wtf_forms import FormWTFAjouterPersonne
from APP_FILMS_164.personnes.gestion_personnes_wtf_forms import FormWTFUpdatePersonne
from APP_FILMS_164.personnes.gestion_personnes_wtf_forms import FormWTFDeletePersonne

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les allergie.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/personnes_afficher/<string:order_by>/<int:current_selected_id_pers>", methods=['GET', 'POST'])
def personnes_afficher(order_by, current_selected_id_pers):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and current_selected_id_pers == 0:
                    mc_afficher.execute("""SELECT id_pers, nom_pers, prenom_pers FROM t_pers ORDER BY id_pers""")
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable

                    mc_afficher.execute("""SELECT id_pers, nom_pers, prenom_pers FROM t_pers WHERE id_pers = %(value_id_pers_selected)s""", {"value_id_pers_selected": current_selected_id_pers})
                else:
                    mc_afficher.execute("""SELECT id_pers, nom_pers, prenom_pers FROM t_pers ORDER BY id_pers DESC""")

                data_personnes = mc_afficher.fetchall()

                print("data_genres ", data_personnes, " Type : ", type(data_personnes))
                # Différencier les messages si la table est vide.
                if not data_personnes and current_selected_id_pers == 0:
                    flash("""La table "t_pers" est vide. !!""", "warning")
                elif not data_personnes and current_selected_id_pers > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"La personne demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données personne affichés !!", "success")

        except Exception as Exception_personnes_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{personnes_afficher.__name__} ; "
                                          f"{Exception_personnes_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("personnes/personnes_afficher.html", data={"data_personnes": data_personnes})


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


@app.route("/personnes_ajouter", methods=['GET', 'POST'])
def personnes_ajouter_wtf():
    form_insert = FormWTFAjouterPersonne()
    if request.method == "POST":
        try:
            if form_insert.validate_on_submit():
                valeurs_insertion_dictionnaire = {"nom_pers": form_insert.nom_pers_wtf.data.lower(),
                                                  "prenom_pers": form_insert.prenom_pers_wtf.data.lower(),
                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_allergie = """INSERT INTO t_pers (nom_pers, prenom_pers) VALUES (%(nom_pers)s, %(prenom_pers)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_allergie, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('personnes_afficher', order_by='DESC', current_selected_id_pers=0))

        except Exception as Exception_personnes_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{personnes_ajouter_wtf.__name__} ; "
                                            f"{Exception_personnes_ajouter_wtf}")

    return render_template("personnes/personnes_ajouter_wtf.html", form=form_insert)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "allergie" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "allergie_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "allergie/allergie_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/personnes_update", methods=['GET', 'POST'])
def personnes_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_pers_update = request.values['id_pers_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatePersonne()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "allergie_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.

            valeurs_update_dictionnaire = {"value_id_pers": id_pers_update,
                                           "nom_pers": form_update.nom_pers_wtf.data.lower(),
                                           "prenom_pers": form_update.prenom_pers_wtf.data.lower(),
                                           }

            print("valeur_update_dictionnaire ", valeurs_update_dictionnaire)

            str_sql_update_allergie = """UPDATE t_pers SET nom_pers = %(nom_pers)s, 
            prenom_pers = %(prenom_pers)s WHERE id_pers = %(value_id_pers)s """

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_allergie, valeurs_update_dictionnaire)


            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('personnes_afficher', order_by="ASC", current_selected_id_pers=id_pers_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_pers = "SELECT id_pers, nom_pers, prenom_pers FROM t_pers " \
                               "WHERE id_pers = %(value_id_pers)s"

            valeur_select_dictionnaire = {"value_id_pers": id_pers_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_pers, valeur_select_dictionnaire)

    except Exception as Exception_personnes_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{personnes_update_wtf.__name__} ; "
                                      f"{Exception_personnes_update_wtf}")

    return render_template("personnes/personnes_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "allergie" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "allergie_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "allergie/allergie_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/personnes_delete", methods=['GET', 'POST'])
def personnes_delete_wtf():

    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_pers_delete = request.values['id_pers_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeletePersonne()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("personnes_afficher", order_by="ASC", current_selected_id_pers=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "allergie/allergie_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.

                flash(f"Supprimer la personne de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_pers": id_pers_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                # str_sql_delete_films_genre = """DELETE FROM t_genre_film WHERE fk_genre = %(value_id_genre)s"""
                str_sql_delete_id_pers = """DELETE FROM t_pers WHERE id_pers = %(value_id_pers)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_id_pers, valeur_delete_dictionnaire)

                flash(f"Personne définitivement supprimée !!", "success")
                print(f"Personne définitivement supprimée !!")

                # afficher les données
                return redirect(url_for('personnes_afficher', order_by="ASC", current_selected_id_pers=0))

        if request.method == "GET":
            print(id_pers_delete, type(id_pers_delete))

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
                # # le formulaire "allergie/allergie_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                # session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_pers = "SELECT id_pers, nom_pers, prenom_pers FROM t_pers " \
                               "WHERE id_pers = %(value_id_pers)s"

                mydb_conn.execute(str_sql_id_pers, {"value_id_pers": id_pers_delete})
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE


            # Le bouton pour l'action "DELETE" dans le form. "allergie_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_personnes_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{personnes_delete_wtf.__name__} ; "
                                      f"{Exception_personnes_delete_wtf}")

    return render_template("personnes/personnes_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del)