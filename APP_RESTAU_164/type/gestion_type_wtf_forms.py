"""
    Fichier : gestion_allergies_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp

champ_type_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
class FormWTFAjouterType(FlaskForm):
    """
        Dans le formulaire "ingre_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    nom_type_wtf = StringField("Clavioter le nom du type ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                   Regexp(champ_type_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    submit = SubmitField("Enregistrer type")


class FormWTFUpdateType(FlaskForm):
    """
        Dans le formulaire "ingre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    nom_type_wtf = StringField("Clavioter le nom du type ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                        Regexp(champ_type_regexp,
                                                                               message="Pas de chiffres, de caractères "
                                                                                       "spéciaux, "
                                                                                       "d'espace à double, de double "
                                                                                       "apostrophe, de double trait union")
                                                                        ])
    submit = SubmitField("Modifier type")

class FormWTFDeleteType(FlaskForm):
    """
        Dans le formulaire "ingre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_type_delete_wtf = StringField("Supprimer ce type")
    submit_btn_del = SubmitField("Supprimer type")
    submit_btn_conf_del = SubmitField("Etes-vous sur de supprimer ?")
    submit_btn_annuler = SubmitField("Annuler")