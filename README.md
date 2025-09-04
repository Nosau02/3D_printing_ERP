# 3D_printing_ERP
Logiciel de gestion conçu pour être utilisé dans une start-up/PME dans le domaine de l'impression 3D.

============================================================================================
Les fonctionalitées inclues sont les suivantes:

  -Création et modification d'une base de donnée de matière:
    Cette dernière permet de d'entrer les références disponibles ainsi que ses infromations (prix, fournisseur, etc..)
    
  -Calcul de prix pour un projet spécifique:
    Le prix est calculé selon une base de tarification en fonction des heures d'impression, de conception, de manutention. 
    Le coût matière ainsi que la marge souhaitée sur la matière sont également inclus.
    Il est également possible d' ajouter un rabais.
    Il est possbile d'enregister le projet en tant que devis dans une base de donnée afin d'émettre une facture par la suite.
    Chaque devis est émis sous un numéro unique, selon une convention interne au logociel. Cette denière est la suivante

      DEV-AAAA-JJMM-XXXXXX-IN  où: AAAA est l'année en cours, JJ et MM le jour et le mois d'émission du devis, XXXXXX est le n ième devis émis durant l'année et IN sont les initiales du client (JC pour Jean Chartier)

  -Suivi des devis et facturation:
    Possibilité d'annuler, de valider ou de facturer un devis. Un statut "paiement reçu" est également disponible.
    Le logiciel génère automatiquement une facture au format PDF, comforme au droit suisse et payable par QR-code bancaire fonctionnel. Cette dernière est prête à être postée dans une envelope à fenêtre A5.
    Chaque facture est émise sous un numéro unique, selon une convention interne au logociel. Cette denière est la suivante

      INV-AAAA-JJMM-XXXXXX-IN  où: AAAA est l'année en cours, JJ et MM le jour et le mois d'émission de la facture, XXXXXX est la n ième facture émise durant l'année et IN sont les initiales du client (JC pour Jean Chartier)
    
============================================================================================
Architecture:

-ERP                # Dossier principal
|-app.py            # Code principal
|-Data              # Dossier données
  |-creditors.csv   # Contient les différents créditeurs possibles
  |-materials.csv   # Contient la base de donnée mantière
  |-quote.csv       # Contient la base de donnée des devis
  |-pricing.csv     # Contient la table de tarification
  |-sequence.json   # Contient le dernier numéro attribué à un devis et à une facture pour chaque année 
  |-logo.png        # Logo à faire figurer sur la facture, optionel
|-Modules
  |-__init__.py     # Script: Permet d'utiliser le dossier en tant que module, autorise les imports relatifs -> from .Sequence import get_number
  |-Materials.py    # Script: Gère la page de gestion de la base de donnée matière
  |-Calculator.py   # Script: Gère la page de calcul de prix
  |-Tracking.py     # Script: Gère la page de suivi des devis
  |-Sequence.py     # Script: Gère la numérotation des devis et des factures, gestion des accès au .json
  |-Invoice_pdf.py  # Script: génère la facture PDF et le QR-code de paiement
|-Invoices          # Dossier de destination des factures PDF


============================================================================================
Mode d'emploi:
1) Copier le dossier ERP en local.
2) Remplir les fichier "creditors.csv" et "pricing.csv" dans un éditeur de texte.
     Exemple pour "creditors.csv":
       Prénom,Nom,Rue et numéro,NPA et ville,CH,CH12 1234 1234 1234 1234 1
   
     Exemple pour "pricing.csv:
       80,15,50,3
3) Lancer le fichier app.py dans un IDE, un lien apparaît dans la console.
4) Suive ce lien pour tomber sur la page d'accueil, le texte est modifiabler depuis le code source de "app.py".
5) Ouvrir l'onglet matière, remplir les champs et cliquer sur "Ad to database".
   -> Si une erreur a été commise, cliquer sur "X" de la ligne pour la supprimer.
   -> Un message de confiramtion s'affiche sous les boutons.
   -> Le tableau peut être trié par matière, couleur ou fournisseur à l'aide du Radio button. Ce dernier affecte également le graphique de distribution.
   ?  Si une matière vient d'être ajoutée et qu'elle n'apparaît pas dans le tableau, mettre à jour la table en cliquant sur le bouton
6) Ouvrir l'onglet de calcul, sélectionner une matière dans le tableau en cliquant sur la colonne de gauche de la ligne souhaitée.
   -> Remplir les champs et cliquer sur "Save quotation" pour enregistrer le devis.
   -> Un message de confiramtion s'affiche sous les boutons. 
   -> Le Graphique au bas du tableau montre la proportion du coût pour chaque poste.
   ?  Si une matière vient d'être ajoutée et qu'elle n'apparaît pas dans le tableau, mettre à jour la table en cliquant sur le bouton
7) Ouvrir l'onglet de suivi, sélectionner un devis dans le tableau en cliquant sur la colonne de gauche de la ligne souhaitée.
   -> Le statut du devis peut être changé de "émis" en "accepté", "annulé", "facturé" et "paiement reçu".
   -> Lorsque le statut est changé pour "facturé", une facture est générée automatiquement dans "ERP\Invoices".
   -> Un message de confiramtion s'affiche sous les boutons.
   -> Le graphique montre la distribution des devis enregistrés dans la base de donnée
   ?  Si une matière vient d'être ajoutée et qu'elle n'apparaît pas dans le tableau, mettre à jour la table en cliquant sur le bouton







