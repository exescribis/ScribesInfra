Testing SE Domain
-----------------

* ``se:requirement::``
* ``se:remark::``
* ``se:question::``
* ``se:hypothesis::``



..  se:requirement:: E001

    Les vendeurs de l'entreprise.

    :type: Fonctionnelle.
    :priority: Prénoms et noms du vendeur.
    :maturity: Basse

Here is a unqualified reference `E001` and here a qualified
one :se:requirement:`E001` (``:se:requirement:`E001```).

Remarques
"""""""""

:Dernier numéro: R001

..  se:remark:: R001
    Titre de la remarque.

    Le corps de la remarque sur plusieurs lignes
    mais toujours indentées.

Questions
"""""""""

:Dernier numéro: Q002

Questions ouvertes
^^^^^^^^^^^^^^^^^^

..  se:question:: Q002

    Le titre

    Le corps sur plusieurs lignes
    mais toujours indentées.

Questions fermées
^^^^^^^^^^^^^^^^^

..  se:question:: Q001

    Le titre

    Le corps sur plusieurs lignes
    mais toujours indentées.

    La réponse qui a été donnée, etc.

Hypothèses
""""""""""

:Dernier numéro: H002

Hypothèses ouvertes
^^^^^^^^^^^^^^^^^^^

..  se:remark:: H002
    Le titre

Hypothèses fermées
^^^^^^^^^^^^^^^^^^

..  se:hypothesis:: H001
    Le titre

    Le corps de l'hypothèse
    avec des explications, etc.

    Les réponses indiquant si l'hypothèse a été validée, etc.



Testing xglossary
-----------------



..  xglossary:: glossaire
    :sorted:

    environment
        A structure where information

    source
    source directory
        The directory which, including its subdirectories, contains all files for one Sphinx project.

    cetace
    cetaces
        toto

    alpha
        :toto:
        :titi:

Index
-----
:ref:`genindex`

