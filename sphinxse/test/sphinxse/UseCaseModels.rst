Usecase Models
==============


Actors
------

..  se:actor:: Client

    Un client est une personne externe à l'entreprise et
    interragissant avec le système pour acheter un ou plusieurs
    produits. Le public concerné est très large.

..  se:actor:: Gerant

    :superactor: Employe

    Le gerant est employé par l'entreprise. Son role est de
    gérer les stocks de produits et d'établir les devis
    pour les fournisseurs.

    :instance: bob elie djamila sophie

..  se:iactor:: djamila

    :actor: Gerant


Usecases
--------

..  se:usecase:: AcheterDesProduits

    :actor: :se:actor:`Client`

    Un :se:actor:`Client` achète un produit via une interface
    Internet en les sélectionnant, les mettant dans un panier,
    puis en règlant le montant de la commande par carte
    bancaire ou par PayPal.

    :accesses:  Produit.R Panier.C Commande.CD
                Reduction.total.RU
    :scenarios: Scn1, Scn2, Scn3


Scenario Scn1
-------------

..  include:: Scenarios/Scn1.rst

Scenario Scn2
-------------

..  include:: Scenarios/Scn2.rst