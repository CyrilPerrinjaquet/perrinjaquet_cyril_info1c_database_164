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
from APP_RESTAU_164.ingredient.gestion_ingre_wtf_forms import FormWTFAjouterIngredient
from APP_RESTAU_164.ingredient.gestion_ingre_wtf_forms import FormWTFUpdateIngredient
from APP_RESTAU_164.ingredient.gestion_ingre_wtf_forms import FormWTFDeleteIngredient

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les allergie.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/ingre_afficher/<string:order_by>/<int:current_selected_id_ingre>", methods=['GET', 'POST'])
def ingre_afficher(order_by, current_selected_id_ingre):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and current_selected_id_ingre == 0:
                    mc_afficher.execute("""SELECT id_ingre, nom_ingre FROM t_ingre ORDER BY id_ingre""")

                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable

                    mc_afficher.execute(
                        """SELECT id_ingre, nom_ingre FROM t_ingre WHERE id_ingre = %(value_id_ingre_selected)s""",
                        {"value_id_ingre_selected": current_selected_id_ingre})
                else:
                    mc_afficher.execute("""SELECT id_ingre, nom_ingre FROM t_ingre ORDER BY id_ingre DESC""")

                data_ingredients = mc_afficher.fetchall()

                print("data_ingredients ", data_ingredients, " Type : ", type(data_ingredients))
                # Différencier les messages si la table est vide.
                if not data_ingredients and current_selected_id_ingre == 0:
                    flash("""La table "t_ingre" est vide. !!""", "warning")
                elif not data_ingredients and current_selected_id_ingre > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"L'ingrédient demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données ingrédient affichés !!", "success")

        except Exception as Exception_ingre_afficher:
            raise ExceptionPersonnesAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{ingre_afficher.__name__} ; "
                                          f"{Exception_ingre_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("ingredient/ingre_afficher.html", data={"data_ingredients": data_ingredients})


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


@app.route("/ingre_ajouter", methods=['GET', 'POST'])
def ingre_ajouter_wtf():
    form_insert = FormWTFAjouterIngredient()
    if request.method == "POST":
        try:
            if form_insert.validate_on_submit():
                valeurs_insertion_dictionnaire = {"nom_ingre": form_insert.nom_ingre_wtf.data.lower(),
                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_ingre = """INSERT INTO t_ingre (nom_ingre) VALUES (%(nom_ingre)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_ingre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('ingre_afficher', order_by='DESC', current_selected_id_ingre=0))

        except Exception as Exception_ingre_ajouter_wtf:
            raise ExceptionPersonnesAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{ingre_ajouter_wtf.__name__} ; "
                                            f"{Exception_ingre_ajouter_wtf}")

    return render_template("ingredient/ingre_ajouter_wtf.html", form=form_insert)


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


@app.route("/ingre_update", methods=['GET', 'POST'])
def ingre_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_ingre_update = request.values['id_ingre_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateIngredient()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "ingre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.

            valeurs_update_dictionnaire = {"value_id_ingre": id_ingre_update,
                                           "nom_ingre": form_update.nom_ingre_wtf.data.lower(),
                                           }

            print("valeur_update_dictionnaire ", valeurs_update_dictionnaire)

            str_sql_update_ingre = """UPDATE t_ingre SET nom_ingre = %(nom_ingre)s WHERE id_ingre = %(value_id_ingre)s """

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_ingre, valeurs_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('ingre_afficher', order_by="ASC", current_selected_id_ingre=id_ingre_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_ingre = "SELECT id_ingre, nom_ingre FROM t_ingre " \
                               "WHERE id_ingre = %(value_id_ingre)s"

            valeur_select_dictionnaire = {"value_id_ingre": id_ingre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_ingre, valeur_select_dictionnaire)

                data_ingredients = mybd_conn.fetchall()
                ingredient_to_update = data_ingredients[0]
                data = {
                    "nom_ingre_wtf": ingredient_to_update["nom_ingre"]
                }
                form_update = FormWTFUpdateIngredient(data=data)
    except Exception as Exception_ingre_update_wtf:
        raise ExceptionPersonneUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{ingre_update_wtf.__name__} ; "
                                      f"{Exception_ingre_update_wtf}")

    return render_template("ingredient/ingre_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete

    Test : ex. cliquer sur le menu "allergie" puis cliquer sur le bouton "DELETE" d'un "genre"

    Paramètres : sans

    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "ingre_afficher.html"

    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "allergie/ingre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/ingre_delete", methods=['GET', 'POST'])
def ingre_delete_wtf():
    btn_submit_del = None
    submit_btn_conf_del = True
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_ingre_delete = request.values['id_ingre_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteIngredient()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("ingre_afficher", order_by="ASC", current_selected_id_ingre=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "allergie/ingre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.

                flash(f"Supprimer l'ingrédient de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True
                submit_btn_conf_del = False

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_ingre": id_ingre_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                # str_sql_delete_films_genre = """DELETE FROM t_genre_film WHERE fk_genre = %(value_id_genre)s"""
                str_sql_delete_id_ingre = """DELETE FROM t_ingre WHERE id_ingre = %(value_id_ingre)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_id_ingre, valeur_delete_dictionnaire)

                flash(f"Personne définitivement supprimée !!", "success")
                print(f"Personne définitivement supprimée !!")

                # afficher les données
                return redirect(url_for('ingre_afficher', order_by="ASC", current_selected_id_ingre=0))

        if request.method == "GET":
            print(id_ingre_delete, type(id_ingre_delete))

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
                str_sql_id_ingre = """SELECT id_ingre, nom_ingre FROM t_ingre WHERE id_ingre = %(value_id_ingre)s"""

                mydb_conn.execute(str_sql_id_ingre, {"value_id_ingre": id_ingre_delete})
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE

            # Le bouton pour l'action "DELETE" dans le form. "ingre_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_ingre_delete_wtf:
        raise ExceptionPersonneDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{ingre_delete_wtf.__name__} ; "
                                      f"{Exception_ingre_delete_wtf}")

    return render_template("ingredient/ingre_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           submit_btn_conf_del=submit_btn_conf_del)
