# 3D Printing ERP
Logiciel de gestion conçu pour être utilisé dans une start-up / PME dans le domaine de l’impression 3D.

---
**FR, EN below**
## ✨ Fonctionnalités

- **Gestion des matières**  
  Création et modification d’une base de données des matières.  
  Informations incluses : référence, prix, fournisseur, etc.

- **Calcul de prix pour un projet**  
  - Basé sur une grille tarifaire (heures d’impression, conception, manutention).  
  - Intègre le coût matière + marge souhaitée + rabais éventuel.  
  - Sauvegarde des devis en base de données.  
  - Génération d’un **numéro de devis unique** :  
    ```
    DEV-AAAA-JJMM-XXXXXX-IN
    ```
    - `AAAA` → année  
    - `JJMM` → jour et mois  
    - `XXXXXX` → compteur de devis  
    - `IN` → initiales du client (ex. JC pour Jean Chartier)

- **Suivi des devis et facturation**  
  - Statuts disponibles : *émis*, *accepté*, *annulé*, *facturé*, *paiement reçu*.  
  - Génération automatique de factures PDF conformes au droit suisse, payables par QR-code bancaire.  
  - Factures prêtes à être imprimées dans une enveloppe à fenêtre A5.  
  - Numérotation unique :  
    ```
    INV-AAAA-JJMM-XXXXXX-IN
    ```

---

## 📂 Architecture du projet

```plaintext
ERP/                      # Dossier principal
├─ app.py                 # Code principal
├─ Data/                  # Données
│  ├─ creditors.csv       # Créanciers
│  ├─ materials.csv       # Matières
│  ├─ quote.csv           # Devis
│  ├─ pricing.csv         # Tarification
│  ├─ sequence.json       # Suivi des numéros devis/factures
│  └─ logo.png            # Logo sur les factures (optionnel)
├─ Modules/               # Modules Python
│  ├─ __init__.py
│  ├─ Materials.py        # Gestion matières
│  ├─ Calculator.py       # Calcul des prix
│  ├─ Tracking.py         # Suivi devis
│  ├─ Sequence.py         # Numérotation
│  └─ Invoice_pdf.py      # Génération facture + QR-code
└─ Invoices/              # Destination des factures PDF
```

---

## 🛠️ Mode d’emploi

1) Installer le projet en local  
   Copier le dossier ERP.

2) Remplir les fichiers CSV  
   Exemple creditors.csv :
   Prénom,Nom,Rue et numéro,NPA et ville,CH,CH12 1234 1234 1234 1234 1

   Exemple pricing.csv :
   80,15,50,3

3) Lancer le programme
   python app.py
   → Un lien s’affiche dans la console. Ouvre-le dans ton navigateur.

4) Utiliser l’interface web
   - Matières : ajouter / supprimer des entrées, trier par matière, couleur, fournisseur.
   - Calcul de devis : sélectionner une matière, entrer les paramètres, sauvegarder le devis.
   - Suivi devis : changer les statuts, générer les factures.

---

## 📌 Remarques

- Les tableaux peuvent être mis à jour en cliquant sur le bouton refresh.  
- Des messages de confirmation s’affichent après chaque opération.  
- Des graphiques affichent la répartition des coûts et des devis.
- Les radios button de l`onglet matière trient le tableau, la répartition choisie est également affichée dans le graphique.  

---

## 📜 Licence

Ce projet est distribué sous licence GNU GPL v3.0.  
Voir le fichier LICENSE pour plus d’informations.

---
**EN**
## ✨ Features

- **Material management**  
  Create and update a material database.  
  Information included: reference, price, supplier, etc.

- **Project price calculation**  
  - Based on a pricing grid (printing hours, design, handling).  
  - Includes material cost + desired margin + optional discount.  
  - Save quotations in a database.  
  - Generate a **unique quotation number**:
    ```
    DEV-YYYY-MMDD-XXXXXX-IN
    ```
    - `YYYY` → year  
    - `MMDD` → month and day  
    - `XXXXXX` → quotation counter  
    - `IN` → client initials (e.g. JC for John Carter)

- **Quotation tracking and invoicing**  
  - Available statuses: *issued*, *accepted*, *cancelled*, *invoiced*, *payment received*.  
  - Automatic generation of PDF invoices compliant with Swiss law, payable by QR-bank code.  
  - Invoices ready to be printed in A5 windowed envelopes.  
  - Unique numbering:
    ```
    INV-YYYY-MMDD-XXXXXX-IN
    ```
    
---

## 📂 Project structure

```plaintext
ERP/                      # Main folder
├─ app.py                 # Main code
├─ Data/                  # Data folder
│  ├─ creditors.csv       # Creditors
│  ├─ materials.csv       # Materials
│  ├─ quote.csv           # Quotations
│  ├─ pricing.csv         # Pricing grid
│  ├─ sequence.json       # Tracks quotation/invoice numbers
│  └─ logo.png            # Logo to be displayed on invoices (optional)
├─ Modules/               # Python modules
│  ├─ __init__.py
│  ├─ Materials.py        # Material management
│  ├─ Calculator.py       # Price calculation
│  ├─ Tracking.py         # Quotation tracking
│  ├─ Sequence.py         # Numbering system
│  └─ Invoice_pdf.py      # PDF invoice and QR-code generation
└─ Invoices/              # Output folder for generated invoices
```

---

## 🛠️ User guide

1) Install the project locally  
   Copy the ERP folder.

2) Fill in the CSV files  
   Example creditors.csv:
   Firstname,Lastname,Street and number,ZIP and City,CH,CH12 1234 1234 1234 1234 1

   Example pricing.csv:
   80,15,50,3

3) Run the program  
   python app.py  
   → A link will appear in the console. Open it in your browser.

4) Use the web interface  
   - Materials: add / remove entries, sort by material, color, supplier.  
   - Quotation: select a material, enter parameters, save the quotation.  
   - Tracking: change quotation status, generate invoices.

---

## 📌 Notes

- Tables can be updated by clicking the refresh button.  
- Confirmation messages are displayed after each operation.  
- Graphs display the distribution of costs and quotations.  
- The radio buttons in the materials tab also sort the table; the chosen distribution is reflected in the graph.  

---

## 📜 License

This project is licensed under the GNU GPL v3.0.  
See the LICENSE file for more details.
