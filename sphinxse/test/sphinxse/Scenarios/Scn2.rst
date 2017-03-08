..  se:scenario:: Scn2

    :intention:

        Ce scenario montre elie un Acheteur en train
        d'AcheterDesProduits
        puis après réception d'un produit défecteux
        DemanderUnRemboursement. Le Gerant accepte le remboursement
        et le Livreur retourne le produit. Le scénario met en
        oeuvre les uses cases suivants.

    :contexte:

        * 00 Elie est né le 15-02-2007.
        * 01 Marc, son père, décide d’offrir un abonnement à Elie pour son anniversaire.


    :usecases:  ConsulterLeCatalogue
                AcheterDesProduits
                DemanderUnRembourssement


    * 00 Elie est né le 15-02-2007.
    * 01 Marc, son père, décide d’offrir un abonnement à Elie pour son anniversaire.

    .. se:iusecase:: elie Acheteur AcheterDesProduit

        :access:
            Oeuvre.C TypeDOeuvre.R Etudie.C
            Bibliotheque.C Stock.C Correspond.C Possede.C

        * 00 Elie est né le 15-02-2007.
        * 01 Marc, son père, décide d’offrir un abonnement à Elie pour son anniversaire.

            .. code-block:: useocl

                ! albumAIO := new Oeuvre('albumAIO');
                ! albumAIO.type := TypeDOeuvre::musique;
                ! albumAIO.titre := 'All in One';
                ! insert(atelier,albumAIO) into Etudie;

        * 05 Il y a 20 exemplaires de cette œuvre à la bibliothèque «Mandela/Paris».

            .. code-block:: useocl

                ! bibliothequeMandelaParis := new Bibliotheque('bibliothequeMandelaParis');
                ! bibliothequeMandelaParis.nom := 'Mandela/Paris';
                ! stockAlbumAIOMP := new Stock('stockAlbumAIOMP');
                ! insert (bibliothequeMandelaParis,stockAlbumAIOMP) into Possede;
                ! insert (stockAlbumAIOMP,albumAIO) into Correspond;
                ! stockAlbumAIOMP.quantite := 20;


        * 02 Le 14-02-2017 Marc se rend au guichet du cinéma « Montor ».

            .. code-block:: useocl

                    ! bibliothequeMandelaParis := new Bibliotheque('bibliothequeMandelaParis');

    * 03 Marc donne sa carte d’abonné (numéro 452441789) à Natacha, la guichetière.

    .. se:iusecase:: elie Acheteur ReclamerUnProduit

        * 04 Natacha crée une nouvelle carte d’abonné pour Elie subordonnée à celle de Marc.
        * 04 Natacha crée une nouvelle carte d’abonné pour Elie subordonnée à celle de Marc.
        * 04 Natacha crée une nouvelle carte d’abonné pour Elie subordonnée à celle de Marc.

    * 08 Elie est né le 15-02-2007.
