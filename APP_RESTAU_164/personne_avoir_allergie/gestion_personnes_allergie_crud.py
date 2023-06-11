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
from APP_RESTAU_164.personne.gestion_personnes_wtf_forms import FormWTFAjouterPersonne
from APP_RESTAU_164.personne.gestion_personnes_wtf_forms import FormWTFUpdatePersonne
from APP_RESTAU_164.personne.gestion_personnes_wtf_forms import FormWTFDeletePersonne

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher

    Test : ex : http://127.0.0.1:5575/genres_afficher

    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les allergie.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/personne_allergie/<int:current_selected_id_pers>", methods=['GET', 'POST'])
def personne_allergie_afficher(current_selected_id_pers):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_personne_allergie_afficher_data = """SELECT id_pers_avoir_allergie, nom_allergie, nom_pers, prenom_pers FROM t_pers_avoir_allergie
                                                            RIGHT JOIN t_allergie ON t_allergie.id_allergie = t_pers_avoir_allergie.fk_allergie
                                                            LEFT JOIN t_pers ON t_pers.id_pers = t_pers_avoir_allergie.fk_pers"""
                if current_selected_id_pers == 0:
                    # le paramètre 0 permet d'afficher tous les films
                    # Sinon le paramètre représente la valeur de l'id du film
                    mc_afficher.execute(strsql_personne_allergie_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_personne_selected_dictionnaire = {"value_id_personne_selected": current_selected_id_pers}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.

                    mc_afficher.execute(strsql_personne_allergie_afficher_data,
                                        valeur_id_personne_selected_dictionnaire)

                # Récupère les données de la requête.
                data_personnes_allergie_afficher = mc_afficher.fetchall()

                # Différencier les messages.
                if not data_personnes_allergie_afficher and current_selected_id_pers == 0:
                    flash("""La table "t_pers" est vide. !""", "warning")
                elif not data_personnes_allergie_afficher and current_selected_id_pers > 0:
                    # Si l'utilisateur change l'id_film dans l'URL et qu'il ne correspond à aucun film
                    flash(f"La personne {current_id_personne_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données personnes et allergies affichés !!", "success")

        except Exception as Exception_personnes_allergie_afficher:
            raise ExceptionPersonneAllergieAfficher(
                f"fichier : {Path(__file__).name}  ;  {personne_allergie_afficher.__name__} ;"
                f"{Exception_personnes_allergie_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("personne_avoir_allergie/personne_avoir_allergie_afficher.html",
                           data={"data_personnes_allergie": data_personnes_allergie_afficher})


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


@app.route("/id_pers_allergie_btn_edit_html", methods=['GET', 'POST'])
def edit_personne_allergie_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                # Récupère la valeur de "id_film" du formulaire html "films_genres_afficher.html"
                # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_film"
                # grâce à la variable "id_film_genres_edit_html" dans le fichier "films_genres_afficher.html"
                # href="{{ url_for('edit_genre_film_selected', id_film_genres_edit_html=row.id_film) }}"
                id_personne_allergie_edit = request.values['id_pers_allergie_btn_edit_html']

                # Mémorise l'id du film dans une variable de session
                # (ici la sécurité de l'application n'est pas engagée)
                # il faut éviter de stocker des données sensibles dans des variables de sessions.
                session['session_id_personne_allergie_edit'] = id_personne_allergie_edit

                # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                valeur_id_personne_selected_dictionnaire = {
                    "value_id_pers_allergie_selected": id_personne_allergie_edit}

                # Récupère les données grâce à 3 requêtes MySql définie dans la fonction genres_films_afficher_data
                # 1) Sélection du film choisi
                # 2) Sélection des genres "déjà" attribués pour le film.
                # 3) Sélection des genres "pas encore" attribués pour le film choisi.
                # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "genres_films_afficher_data"
                data_personne_allergie_attribues = allergies_selected_afficher_data(
                    valeur_id_personne_selected_dictionnaire)
                data_personne_allergie_non_attribues = allergie_non_selected_afficher_data(
                    valeur_id_personne_selected_dictionnaire)

                # Dans le composant "tags-selector-tagselect" on doit connaître
                # les genres qui ne sont pas encore sélectionnés.
                lst_data_personne_allergie_non_attribues = [item['id_allergie'] for item in
                                                            data_personne_allergie_non_attribues]
                session['session_lst_data_personne_allergie_non_attribues'] = lst_data_personne_allergie_non_attribues

                # Dans le composant "tags-selector-tagselect" on doit connaître
                # les genres qui sont déjà sélectionnés.
                lst_data_personne_allergie_old_attribues = [item['id_allergie'] for item in
                                                            data_personne_allergie_attribues]
                session['session_lst_data_personne_allergie_old_attribues'] = lst_data_personne_allergie_old_attribues

                # Extrait les valeurs contenues dans la table "t_genres", colonne "intitule_genre"
                # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_genre
                lst_data_personne_allergie_non_attribues = [item['nom_allergie'] for item in
                                                            data_personne_allergie_non_attribues]

        except Exception as Exception_edit_personne_allergie_selected:
            raise ExceptionEditPersonneAllergieSelected(f"fichier : {Path(__file__).name}  ;  "
                                                 f"{edit_personne_allergie_selected.__name__} ; "
                                                 f"{Exception_edit_personne_allergie_selected}")

    return render_template("personne_avoir_allergie/personne_allergie_modifier_tags_dropbox.html",
                           data_personne_allergie_attribues=data_personne_allergie_attribues,
                           data_personne_allergie_non_attribues=data_personne_allergie_non_attribues)


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


@app.route("/personne_allergie_update", methods=['GET', 'POST'])
def personne_allergie_update():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_personne_allergie_selected = session['session_id_personne_allergie_edit']

            # Récupère la liste des genres qui ne sont pas associés au film sélectionné.
            old_lst_data_personne_allergie_non_attribues = session['session_lst_data_personne_allergie_non_attribues']

            # Récupère la liste des genres qui sont associés au film sélectionné.
            old_lst_data_personne_allergie_attribues = session['session_lst_data_personne_allergie_old_attribues']

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme genres dans le composant "tags-selector-tagselect"
            # dans le fichier "genres_films_modifier_tags_dropbox.html"
            new_lst_str_personne_allergie = request.form.getlist('name_allergie_select_tags')

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_personne_allergie_old = list(map(int, new_lst_str_personne_allergie))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_genre" qui doivent être effacés de la table intermédiaire "t_genre_film".
            lst_diff_personne_allergie_delete_b = list(set(old_lst_data_personne_allergie_attribues) -
                                                       set(new_lst_int_personne_allergie_old))

            # Une liste de "id_genre" qui doivent être ajoutés à la "t_genre_film"
            lst_diff_personne_allergie_insert_a = list(
                set(new_lst_int_personne_allergie_old) - set(old_lst_data_personne_allergie_attribues))

            # SQL pour insérer une nouvelle association entre
            # "fk_film"/"id_film" et "fk_genre"/"id_genre" dans la "t_genre_film"

            strsql_insert_personne_allergie = """UPDATE t_pers_avoir_allergie SET fk_allergie = %(value_fk_allergie)s, fk_pers = %(value_fk_pers)s WHERE id_pers_avoir_allergie = %(value_id_pers_avoir_allergie)s"""

            # SQL pour effacer une (des) association(s) existantes entre "id_film" et "id_genre" dans la "t_genre_film"
            strsql_delete_personne_allergie = """DELETE FROM t_pers_avoir_allergie WHERE fk_allergie = %(value_fk_allergie)s AND fk_pers = %(value_fk_pers)s"""

            with DBconnection() as mconn_bd:
                # Pour le film sélectionné, parcourir la liste des genres à INSÉRER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_allergie_insert in lst_diff_personne_allergie_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_ins" (l'id du genre dans la liste) associé à une variable.
                    valeurs_personne_allergie_selected_dictionnaire = {
                        "value_id_pers_avoir_allergie": id_personne_allergie_selected,
                        "value_fk_pers": id_personne_allergie_selected,
                        "value_fk_allergie": id_allergie_insert}

                    mconn_bd.execute('SET FOREIGN_KEY_CHECKS = 0')
                    mconn_bd.execute(strsql_insert_personne_allergie, valeurs_personne_allergie_selected_dictionnaire)
                    mconn_bd.execute('SET FOREIGN_KEY_CHECKS = 1')
                # Pour le film sélectionné, parcourir la liste des genres à EFFACER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_allergie_delete in lst_diff_personne_allergie_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_del" (l'id du genre dans la liste) associé à une variable.
                    valeurs_personne_allergie_selected_dictionnaire = {"value_fk_pers": id_personne_allergie_selected,
                                                                       "value_fk_allergie": id_allergie_delete}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "execute" dans la classe "DBconnection"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "DBconnection"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.execute(strsql_delete_personne_allergie, valeurs_personne_allergie_selected_dictionnaire)

        except Exception as Exception_update_genre_film_selected:
            raise ExceptionUpdatePersonneAllergieSelected(f"fichier : {Path(__file__).name}  ;  "
                                                   f"{Exception_update_genre_film_selected}")

    # Après cette mise à jour de la table intermédiaire "t_genre_film",
    # on affiche les films et le(urs) genre(s) associé(s).
    return redirect(url_for('personne_allergie_afficher', current_selected_id_pers=id_personne_allergie_selected))


def allergies_selected_afficher_data(valeur_id_pers_allergie_selected_dict):
    try:

        strsql_allergies_attribueted = """SELECT id_allergie, nom_allergie FROM t_pers_avoir_allergie
                                                INNER JOIN t_pers ON t_pers.id_pers = t_pers_avoir_allergie.fk_pers
                                                INNER JOIN t_allergie ON t_allergie.id_allergie = t_pers_avoir_allergie.fk_allergie
                                                WHERE id_pers = %(value_id_pers_allergie_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with DBconnection() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_allergies_attribueted, valeur_id_pers_allergie_selected_dict)
            # Récupère les données de la requête.
            data_allergies_attributed = mc_afficher.fetchall()

            return data_allergies_attributed

    except Exception as Exception_genres_films_afficher_data:
        raise ExceptionPersonneAllergieAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{Exception_genres_films_afficher_data}")


def allergie_non_selected_afficher_data(valeur_id_pers_allergie_dict):
    try:
        strsql_pers_allergie_non_attributed = """SELECT id_allergie, nom_allergie FROM t_allergie WHERE id_allergie not in(SELECT id_allergie FROM t_pers_avoir_allergie
                                                        INNER JOIN t_pers ON t_pers.id_pers = t_pers_avoir_allergie.fk_pers
                                                        INNER JOIN t_allergie ON t_allergie.id_allergie = t_pers_avoir_allergie.fk_allergie
                                                        WHERE id_pers = %(value_id_pers_allergie_selected)s)"""

        with DBconnection() as mc_afficher:
            mc_afficher.execute(strsql_pers_allergie_non_attributed, valeur_id_pers_allergie_dict)
            data_pers_allergies_non_attributed = mc_afficher.fetchall()

            return data_pers_allergies_non_attributed

    except Exception as Exception_genres_films_afficher_data:
        raise ExceptionPersonneAllergieAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{Exception_genres_films_afficher_data}")


def personne_afficher_data():
    try:

        strsql_all_personnes = """SELECT id_pers, nom_pers FROM t_pers"""

        with DBconnection() as mc_afficher:
            mc_afficher.execute(strsql_all_personnes)
            personne_all = mc_afficher.fetchall()

            return personne_all

    except Exception as Exception_genres_films_afficher_data:
        raise ExceptionPersonneAllergieAfficherData(f"fichier : {Path(__file__).name}  ;"
                                               f"{Exception_genres_films_afficher_data}")