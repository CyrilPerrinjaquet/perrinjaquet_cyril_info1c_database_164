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


class FormWTFAjouterAllergie(FlaskForm):
    """
        Dans le formulaire "ingre_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    champ_allergie_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_allergie_wtf = StringField("Clavioter l'allergie ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                   Regexp(champ_allergie_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    allergene_wtf = StringField("Clavioter l'allergène ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                        Regexp(champ_allergie_regexp,
                                                                               message="Pas de chiffres, de caractères "
                                                                                       "spéciaux, "
                                                                                       "d'espace à double, de double "
                                                                                       "apostrophe, de double trait union")
                                                                        ])

    gravite_wtf = StringField("Clavioter la gravité ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                        Regexp(champ_allergie_regexp,
                                                                               message="Pas de chiffres, de caractères "
                                                                                       "spéciaux, "
                                                                                       "d'espace à double, de double "
                                                                                       "apostrophe, de double trait union")
                                                                        ])
    symptomes_wtf = StringField("Clavioter le(s) symptomes ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                   Regexp(champ_allergie_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    precautions_wtf = StringField("Clavioter la/les précautions à prendre ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                   Regexp(champ_allergie_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    traitement_wtf = StringField("Clavioter le traitement ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                   Regexp(champ_allergie_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    notes_wtf = StringField("Clavioter des notes supp. (facultatif) ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                   Regexp(champ_allergie_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])

    submit = SubmitField("Enregistrer allergie")


class FormWTFUpdateAllergie(FlaskForm):
    """
        Dans le formulaire "ingre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    champ_allergie_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_allergie_wtf = StringField("Clavioter l'allergie ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                        Regexp(champ_allergie_regexp,
                                                                               message="Pas de chiffres, de caractères "
                                                                                       "spéciaux, "
                                                                                       "d'espace à double, de double "
                                                                                       "apostrophe, de double trait union")
                                                                        ])
    allergene_wtf = StringField("Clavioter l'allergène ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                      Regexp(champ_allergie_regexp,
                                                                             message="Pas de chiffres, de caractères "
                                                                                     "spéciaux, "
                                                                                     "d'espace à double, de double "
                                                                                     "apostrophe, de double trait union")
                                                                      ])

    gravite_wtf = StringField("Clavioter la gravité ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                   Regexp(champ_allergie_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    symptomes_wtf = StringField("Clavioter le(s) symptomes ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                          Regexp(champ_allergie_regexp,
                                                                                 message="Pas de chiffres, de caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait union")
                                                                          ])
    precautions_wtf = StringField("Clavioter la/les précautions à prendre ",
                                  validators=[Length(min=2, max=50, message="min 2 max 50"),
                                              Regexp(champ_allergie_regexp,
                                                     message="Pas de chiffres, de caractères "
                                                             "spéciaux, "
                                                             "d'espace à double, de double "
                                                             "apostrophe, de double trait union")
                                              ])
    traitement_wtf = StringField("Clavioter le traitement ", validators=[Length(min=2, max=50, message="min 2 max 50"),
                                                                         Regexp(champ_allergie_regexp,
                                                                                message="Pas de chiffres, de caractères "
                                                                                        "spéciaux, "
                                                                                        "d'espace à double, de double "
                                                                                        "apostrophe, de double trait union")
                                                                         ])
    notes_wtf = StringField("Clavioter des notes supp. (facultatif) ",
                            validators=[Length(min=2, max=50, message="min 2 max 50"),
                                        Regexp(champ_allergie_regexp,
                                               message="Pas de chiffres, de caractères "
                                                       "spéciaux, "
                                                       "d'espace à double, de double "
                                                       "apostrophe, de double trait union")
                                        ])
    submit = SubmitField("Update allergie")


class FormWTFDeleteAllergie(FlaskForm):
    """
        Dans le formulaire "ingre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_allergie_delete_wtf = StringField("Effacer cette allergie")
    submit_btn_del = SubmitField("Effacer genre")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
