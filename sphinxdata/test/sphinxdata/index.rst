
LesVendeurs
"""""""""""

..  sql:table:: LesVendeurs(#codeVendeur:i, nom:t, region:t)

    Les vendeurs de l'entreprise.

    :col codeVendeur integer: Code du vendeur.
    :col nom text: Prénoms et noms du vendeur.
    :col region text: Région dans laquelle travaille le vendeur.
    :con example1: kdfqskdf
    :con example2: dhfkqjsdhf

LesFrais
""""""""

..  sql:table:: LesFrais(#codeNote:i, jour:d, montant:r, nature:t, vendeur:i>)

    Les notes de frais de l'année en cours pour chaque vendeur de l'entreprise.

    :col codeNote integer: Code associée à la note. Ce numéro débute à 1 en début
        d'année et incrémenté à chaque fois qu'une nouvelle note est enregistrée
        par le secrétariat.
    :col jour date: Date à laquelle les frais relatis à la note ont été établis.
    :col nature text: Nature de la note.
    :col vendeur integer: Code du vendeur ayant produit la note.

Requetes
^^^^^^^^

..   sql:query:: LesComplets(codeVendeur:i)

     Codes des vendeurs ayant une note de frais de chaque nature

    .. code-block:: sql
        :linenos:

        SELECT code_vendeur
        FROM LesFrais
        GROUP BY code_vendeur
        HAVING count(DISTINCT nature) = ( SELECT count( DISTINCT nature) FROM LesFrais);

Index
^^^^^

:ref:`genindex`