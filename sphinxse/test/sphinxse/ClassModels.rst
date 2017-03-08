Class Models
============

..  se:classe:: Commande

    :superclass: Element

    Une commande est un ensemble d'Items pouvant être achetées par un
    Client.

    :att r: Boolean
    :att s: Boolean
    :att t: Boolean
    :att a: Integer[0..1]

        Documentation de a. Helas le resultat n'est pas tres
        élégant car la première ligne vient avec cette définition.

    :att b: Real. Ceci est une autre alternative pour documenter.
    :att v: Boolean

        **access:** Scn1.RU Scn3

    .. ..
        ..  se:attribute:: a : Integer

            This is the definition

        ..  se:attribute:: b : Real[0..1]

        ..  se:attribute:: b : Real[0..2]

..  se:classe:: Commande2

    :superclass: Element

    Une commande est un ensemble d'Items pouvant être achetés par un
    Client.

        ..  se:attribute:: a : Integer

            This is the definition

            :optional:
            :access: Scn1.RU Scn2

        ..  se:attribute:: b : Real[0..1]

        ..  se:attribute:: c : Real[0..2]


..  se:association:: EstFaitDe

    Une commande est un ensemble d'Items pouvant être achetées par un
    Client.

    :role commande: Commande[0..1]
    :role items: Item[0..*]

    :from commande: Commande[0..1]
    :to items: Item[0..*]


..  se:association:: EstFaitDe2

    Une commande est un ensemble d'Items pouvant être achetées par un
    Client.

        ..  se:role:: a : Command[1]

            Documentation of the a role.

            ..  se:role:: ef : Command[1]

                Documentation of the a role.

                ..  se:role:: edq : Command[1]

                    Documentation of the a role.

                    ..  se:role:: eddq : Command[1]

                         Documentation of the a role.

                        ..  se:role:: edfq : Command[1]

                             Documentation of the a role.

    ..  se:role:: b : Item[*]


..  se:associationclass:: Location

    Une location permet à un habitant de disposer d'une ou plusieurs
    chambre. Cette location a un prix.

    :role commande: Commande[0..1]
    :role items: Item[0..*]

    .. ..
        ..  se:role:: a : Command[1]
        ..  se:role:: b : Item[*]


..  se:role:: ds : Command[1]

    Documentation of the a role.

        ..  se:role:: fsa : Command[1]

            Documentation of the a role.

            ..  se:role:: OP : Command[1]

                ..  se:role:: UU : Command[1]

                    ..  se:role:: DS : Command[1]

                        ..  se:role:: edafq : Command[1]

                        ..  se:role:: edasdqdsfq : Command[1]

                        ..  se:role:: edasfq : Command[1]

            ..  se:role:: esf : Command[1]

                ..  se:role:: eedq : Command[1]

                    ..  se:role:: eddsq : Command[1]

                        ..  se:role:: edffq : Command[1]
