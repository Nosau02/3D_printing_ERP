"""
FR, EN below:

Outil de cération de facture au format PDF : 

Cet Outil permet de générer en sortie une facture au format PDF (ReportLab layout). 
Cette facture est payable par un QR-code de paiement suisse (qrbill).

La TVA est définie à 8.1% par défaut, par item et globalement (modifiable dans le code source si besoin). -> varibale: vat, ligne 143 et 304

Entrées nécessaires (pour la fonction generate_invoice_pdf):
----------------------------------------------------------------
- creditor : dict          # Contient les infos du créditeur (l'entreprise)
    {
        "name":   str,     # Nom de l'entreprise ou de la personne
        "line1":  str,     # Rue et numéro
        "line2":  str,     # NPA et ville
        "country":str      # Code pays (ex: "CH")
    }
- iban : str               # IBAN du créditeur (ex: "CHxx xxxx xxxx xxxx x"), destination du paiement par QR-code
- debtor : dict            # Contient les infos du débiteur (le client)
    {
        "name":   str,
        "line1":  str,
        "line2":  str,
        "country":str
    }
- items_df : pandas.DataFrame  # Liste des items (lignes) de la facture:
    Requits:
        - "Description"  (str)
        - "Quantity"     (int/float)
        - "UnitPrice"    (float, CHF)
        - "Markdown"     (float, CHF)  # Montant en CHF à déduire du total HT à la ligne 0, les autres lignes sont remplies de 0
    Optionel:
        - "Unit"         (str, ex: "h", "pcs")
- quote_num : str          # Numéro du devis lié à cette facture (ex: "DEV-2025-3112-1-JC")
- invoice_num : str        # Numéro de la facture (ex: "INV-2025-3112-1-JC")
- output_folder : str      # Dossier de sortie (ex: "Invoices/") - sera créé s'il n'existe pas
- currency : str           # Currency (default "CHF")
- payment_terms : str      # Payment terms (e.g., "Paiement à 30 jours net")
- logo_path : str | None   # Optional logo path (PNG/JPG). Leave None if no logo.

SORTIES:
----------------------------------------------------------------
- Retourne le chemin du fichier de la facture. Ce dernier est défini comme:
    <Chemin_vers_ce_fichier>/<output_folder>/<invoice_num>.pdf

EXEMPLE D'UTILISATION:
----------------------------------------------------------------
    import pandas as pd
    import os

    # Testing_parameters:
    quote_ID = "DEV-2025-0209-1-JC"
    invoice_ID = "INV-2025-0209-000001-JC"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    items = pd.DataFrame({
        "Description": [    f'Design hours',
                            f'Printing hours',   
                            f'Handling hours',
                            f'Material ({quote["Material"]})'],
        "Quantity": [       5,
                            4,   
                            3,
                            150 / 1000,  # Convert g to kg                                        
        "UnitPrice": [      120,
                            5,   
                            60,
                            32,
        "Unit": [           "h", "h", "h", "kg"], 
        "Markdown": [       10,0,0,0]
    }) 
    creditor = {"name":"Acme SA","line1":"Rue de l'Exemple 1","line2":"1200 Genève","country":"CH"}
    debtor   = {"name":"Jean Dupont","line1":"Avenue des Fleurs 12","line2":"1000 Lausanne","country":"CH"}
    iban = "CH75 8080 8009 5401 4091 1"


    out = generate_invoice_pdf( # type: ignore
        creditor=creditor,
        debtor=debtor,
        items_df=items,
        quote_num=quote_ID,
        invoice_num=invoice_ID,
        output_folder=f"Invoices/",
        iban=iban,
        currency="CHF",
        payment_terms="Paiement à 30 jours net",
        logo_path=None
    )
    print(f"PDF: {out}")

%============

EN:
PDF Invoice Creation Tool:

This tool generates an invoice as a PDF output (ReportLab layout).  
The invoice is payable via a Swiss payment QR-code (qrbill).

VAT is set to 8.1% by default, per item and globally (modifiable in the source code if needed).  
-> variable: vat, line 143 and 304

Required inputs (for the function generate_invoice_pdf):
----------------------------------------------------------------
- creditor : dict          # Contains the creditor’s information (the company)
    {
        "name":   str,     # Company or person name
        "line1":  str,     # Street and number
        "line2":  str,     # ZIP and city
        "country":str      # Country code (e.g., "CH")
    }
- iban : str               # Creditor’s IBAN (e.g., "CHxx xxxx xxxx xxxx x"), payment destination via QR-code
- debtor : dict            # Contains the debtor’s information (the client)
    {
        "name":   str,
        "line1":  str,
        "line2":  str,
        "country":str
    }
- items_df : pandas.DataFrame  # List of invoice items (rows):
    Required:
        - "Description"  (str)
        - "Quantity"     (int/float)
        - "UnitPrice"    (float, CHF)
        - "Markdown"     (float, CHF)  # Amount in CHF to deduct from the subtotal at line 0, other rows filled with 0
    Optional:
        - "Unit"         (str, e.g., "h", "pcs")
- quote_num : str          # Quotation number linked to this invoice (e.g., "DEV-2025-3112-1-JC")
- invoice_num : str        # Invoice number (e.g., "INV-2025-3112-1-JC")
- output_folder : str      # Output folder (e.g., "Invoices/") - will be created if it doesn’t exist
- currency : str           # Currency (default "CHF")
- payment_terms : str      # Payment terms (e.g., "Payment within 30 days net")
- logo_path : str | None   # Optional logo path (PNG/JPG). Leave None if no logo.

OUTPUT:
----------------------------------------------------------------
- Returns the path to the generated invoice file. The path is defined as:
    <Path_to_this_file>/<output_folder>/<invoice_num>.pdf

USAGE EXAMPLE:
----------------------------------------------------------------
    import pandas as pd
    import os

    # Testing parameters:
    quote_ID = "DEV-2025-0209-1-JC"
    invoice_ID = "INV-2025-0209-000001-JC"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    items = pd.DataFrame({
        "Description": [    f'Design hours',
                            f'Printing hours',   
                            f'Handling hours',
                            f'Material ({quote["Material"]})'],
        "Quantity": [       5,
                            4,   
                            3,
                            150 / 1000,  # Convert g to kg                                      
        "UnitPrice": [      120,
                            5,   
                            60,
                            32,
        "Unit": [           "h", "h", "h", "kg"], 
        "Markdown": [       10,0,0,0]
    }) 
    creditor = {"name":"Acme SA","line1":"Rue de l'Exemple 1","line2":"1200 Geneva","country":"CH"}
    debtor   = {"name":"John Doe","line1":"Avenue des Fleurs 12","line2":"1000 Lausanne","country":"CH"}
    iban = "CH75 8080 8009 5401 4091 1"


    out = generate_invoice_pdf( # type: ignore
        creditor=creditor,
        debtor=debtor,
        items_df=items,
        quote_num=quote_ID,
        invoice_num=invoice_ID,
        output_folder=f"Invoices/",
        iban=iban,
        currency="CHF",
        payment_terms="Payment within 30 days net",
        logo_path=None
    )
    print(f"PDF: {out}")

"""

from __future__ import annotations

import os
import tempfile
from datetime import datetime
from typing import Tuple

import pandas as pd
from qrbill import QRBill
from svglib.svglib import svg2rlg
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


# === Fonctions utilitaires ===

# Vérifie que le DataFrame contient les colonnes requises
def _ensure_items_columns(df: pd.DataFrame) -> None:
    required = {"Description", "Quantity", "UnitPrice"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"items_df is missing required columns: {', '.join(sorted(missing))}")

# Formatte une valeur monétaire en CHF avec 2 décimales et séparateur de milliers pour l'affichage dans le PDF
def _format_money(v: float) -> str:
    return f"{v:,.2f}".replace(",", "'")  # 12'345.67

# Construit la table des items et calcule les totaux.
def _build_items_table(items_df: pd.DataFrame) -> Tuple[Table, float, dict, float]:
    # Initialisation
    data = [["Description", "Qté", "Unité", "Prix unitaire", "TVA %", "Prix HT"]]
    total_ht = 0.0

    # Remplissage des lignes
    for _, row in items_df.iterrows():
        desc = str(row["Description"])
        qty = float(row["Quantity"])
        unit = str(row["Unit"]) if "Unit" in row and pd.notna(row["Unit"]) else ""
        pu = float(row["UnitPrice"])
        vat = 8.1
        line_ht = qty * pu

        data.append([
            desc,
            f"{qty:g}",
            unit,
            _format_money(pu),
            f"{vat:.1f}%",
            _format_money(line_ht),
        ])
        total_ht += line_ht

    # Table des styles
    table = Table(data, colWidths=[220, 45, 45, 70, 60, 55, 80], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("ALIGN", (3, 1), (3, -1), "RIGHT"),
        ("ALIGN", (6, 1), (6, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    return table, total_ht

# Génère le QR-bill et le convertit en flowable ReportLab
def _qr_flowable(iban: str, creditor: dict, debtor: dict, amount_chf: float, currency: str) :

    # Crée le QR-bill
    bill = QRBill(
        account=iban,
        creditor={
            "name": creditor["name"],
            "line1": creditor["line1"],
            "line2": creditor["line2"],
            "country": creditor["country"],
        },
        amount=str(amount_chf),
        currency=currency,
        debtor={
            "name": debtor["name"],
            "line1": debtor["line1"],
            "line2": debtor["line2"],
            "country": debtor["country"],
        },
    )

    # Sauvegarde temporaire en SVG, puis convertit en flowable ReportLab
    tmp_svg_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".svg", delete=False, encoding="utf-8") as tmp_svg:
            bill.as_svg(tmp_svg)
            tmp_svg_path = tmp_svg.name
        drawing = svg2rlg(tmp_svg_path)
        return drawing
    finally:
        if tmp_svg_path and os.path.exists(tmp_svg_path):
            try:
                os.remove(tmp_svg_path)
            except OSError:
                pass

# === Fonction principale ===
def generate_invoice_pdf(
    *,
    creditor: dict,
    debtor: dict,
    items_df: pd.DataFrame,
    quote_num: str,
    invoice_num: str,
    output_folder: str,
    iban: str,
    currency: str = "CHF",
    payment_terms: str = "Paiement à 30 jours net",
    logo_path: str | None = None,
) -> Tuple[str, str]:

    # Vérifications
    _ensure_items_columns(items_df)

    # Construire la table des prestations et calculer le total HT
    items_table, total_ht = _build_items_table(items_df)
    markdown = items_df["Markdown"].iloc[0]

    # --- Définiton des styles ReportLab ---
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    body = ParagraphStyle("message",parent=styles["Normal"], fontsize=10, leading=12)
    left = ParagraphStyle("left", parent=styles["Normal"], alignment=TA_LEFT)
    right = ParagraphStyle("right", parent=styles["Normal"], alignment=TA_RIGHT)
    title = ParagraphStyle("title_right", parent=styles["Title"], alignment=TA_LEFT)

    elements = []

    # ============ HEADER: 2 colonnes ============
    # Eléments de la table d'entête
    creditor_info = (
    f"<b>{creditor['name']}</b><br/>{creditor['line1']}<br/>{creditor['line2']}<br/>{creditor['country']}"
    )

    debtor_info = (
    f"{debtor['name']}<br/>{debtor['line1']}<br/>{debtor['line2']}<br/>{debtor['country']}"
    )

    meta = (
    f"Facturé le: {datetime.today().strftime('%d.%m.%Y')}<br/>"
    f"Facture n° <b>{invoice_num}</b><br/>"
    f"Devis n° <b>{quote_num}</b><br/>"
    )

    Tittle = "FACTURE"

    message = (
    f"En vous remerciant de votre confiance et en espérant vous<br/>"
    f"revoir bientôt. Meilleures salutations, {creditor['name']}."
    )

    # Gauche:
    left_flow = []
    left_flow += [Paragraph(Tittle, title), Spacer(1, 10)]
    left_flow += [Paragraph(creditor_info, left), Spacer(1, 20)]
    left_flow += [Paragraph(meta, left)]


    # Droite:
    right_flow = []

    if logo_path and os.path.exists(logo_path):
        right_flow += [Image(logo_path, width=140, height=60,)]
    else: 
        right_flow += [Spacer(1,60)]
    right_flow += [Spacer(1, 30)]
    right_flow += [Paragraph(debtor_info, left)]


    # Construire la table d'entête (2 colonnes)
    header_table = Table(
        [[left_flow, right_flow]],
        colWidths=[300, 230],  
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN",  (1, 0), (1, 0),   "RIGHT"),  # colonne droite alignée à droite
        
    ]))
    elements.append(header_table)

    # Ajout des éléments du corps
    elements.append(Spacer(1, 25))
    elements.append(Paragraph(message, body))
    elements.append(Spacer(1,15))
    elements.append(Paragraph("<b>Détails des prestations, payables sous 30 jours net:</b>", normal))
    elements.append(Spacer(1, 5))

    # Tableau des prestations
    elements.append(items_table)
    elements.append(Spacer(1, 8))

    # Tableau des totaux
    vat = 8.1
    totals_data = [["", "Sous-total HT", f"{_format_money(total_ht)} {currency}"]]
    totals_data.append(["", "Rabais HT", f"{_format_money(markdown)} {currency}"])
    totals_data.append(["", "Base imposable", f"{_format_money(total_ht - markdown)} {currency}"])
    totals_data.append(["", "TVA", f"{vat} %"])
    total_ttc = (total_ht - markdown) * (1+vat/100)


    # Total TTC
    totals_data.append(["", Paragraph("<b>Total TTC</b>", right), Paragraph(f"<b>{_format_money(total_ttc)} {currency}</b>",right)])

    totals_table = Table(totals_data, colWidths=[330, 120, 120])
    totals_table.setStyle(TableStyle([
        ("ALIGN", (2, 0), (2, -1), "RIGHT"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("GRID", (1, 0), (-1, -1), 0.3, colors.grey),
        ("BACKGROUND", (1, -1), (-1, -1), colors.lightgrey),
    ]))
    elements.append(totals_table)
    elements.append(Spacer(1, 16))

    # Intégration du QR-code de paiement
    elements.append(Paragraph("<b>QR-facture</b>", normal))
    elements.append(Spacer(1, 6))
    qr_drawing = _qr_flowable(iban=iban, creditor=creditor, debtor=debtor, amount_chf=round(total_ttc,2), currency=currency)
    elements.append(qr_drawing)

    # Exportation du PDF
    folder_path = os.path.join(os.path.dirname(__file__), output_folder)
    output_path = os.path.join(folder_path, f"{invoice_num}.pdf")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    doc.build(elements)

    return output_path
