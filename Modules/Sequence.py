# -*- coding: utf-8 -*-
"""
FR, EN below:
Générateur séquentiel de numéros (par type et par année) avec persistance JSON,
verrou cross-plateforme via lockfile et écritures atomiques.

API stable et minimale :
    - `next_number(Type: str, width: int = 6) -> tuple[int, str]`
    - `get_number(Type: str, name: str) -> str`

Format de sortie :
------------------
`TYPE-YYYY-DDMM-NNNNNN`
- `TYPE` : chaîne passée à `next_number()` / `get_number()` (ex. "DEV", "INV")
- `YYYY` : année courante
- `DDMM` : jour et mois courants (ordre *jour-mois* pour conserver la compatibilité
           attendue : ex. 31 décembre → `3112`)
- `NNNNNN` : compteur entier (largeur configurable via `width`, 6 par défaut)

Persistance :
-------------
- Fichier JSON : `Data/sequences.json` (créé au besoin)
- Lockfile     : `Data/sequences.json.lock`
- Schéma JSON  :
    {
        "DEV": {"2025": 124, "2024": 317},
        "INV": {"2025": 42}
    }
  → Compteur **par type et par année**, remis à zéro à chaque nouvelle année.

Sécurité / robustesse :
-----------------------
- Verrouillage par lockfile (sans dépendances tierces), tolérance aux verrous
  périmés (stale lock) avec délai configurable.
- Écriture **atomique** : fichier temporaire + `os.replace()` (renommage atomique)
- Compatible Windows / macOS / Linux.
 
Avertissement :
---------------
- L'API et le format sont pensés comme *drop-in replacement* d'une version existante.
  Si votre code appelant repose sur des détails différents (p. ex. schéma JSON),
  adaptez la migration avec précaution.

%============

EN:
Sequential number generator (by type and year) with JSON persistence,
cross-platform locking via lockfile and atomic writes.

Stable and minimal API:
    - `next_number(Type: str, width: int = 6) -> tuple[int, str]`
    - `get_number(Type: str, name: str) -> str`

Output format :
------------------
TYPE-YYYY-DDMM-NNNNNN`
- `TYPE`: string passed to `next_number()` / `get_number()` (e.g. "DEV", "INV")
- `YYYY` : current year
- `DDMM`: current day and month (in *day-month* order to maintain the expected
           compatibility: e.g. 31 December → `3112`)
- `NNNNNN`: integer counter (width configurable via `width`, 6 by default)

Persistence:
-------------
- JSON file: `Data/sequences.json` (created as required)
- Lockfile: `Data/sequences.json.lock` (created as required)
- JSON schema :
    {
        "DEV": {"2025": 124, "2024": 317},
        "INV": { "2025": 42}
    }
  → Counter **by type and year**, reset to zero each new year.

Safety / robustness :
-----------------------
- Locking via lockfile (no third-party dependencies), tolerance of stale locks
  tolerance (stale lock) with configurable delay.
- Atomic** writing: temporary file + `os.replace()` (atomic renaming)
- Windows / macOS / Linux compatible.
 
Warning:
---------------
- The API and format are designed as *drop-in replacement* of an existing version.
  If your calling code is based on different details (e.g. JSON schema)
  adapt the migration carefully.
"""
from __future__ import annotations

import json
import os
import re
import time
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# Constantes & chemins
# ---------------------------------------------------------------------------
MODULE_DIR: Path = Path(__file__).resolve().parent
DATA_DIR: Path = MODULE_DIR / "Data"
JSON_PATH: Path = DATA_DIR / "sequences.json"
LOCK_PATH: Path = DATA_DIR / "sequences.json.lock"
TEMP_SUFFIX: str = ".tmp"

DEFAULT_LOCK_TIMEOUT: float = 5.0      # secondes à attendre pour obtenir le verrou
STALE_LOCK_SECONDS: float = 30.0       # au-delà → on considère le verrou périmé

DEFAULT_WIDTH: int = 6                 # largeur du compteur dans la chaîne

# Caractères autorisés pour le type (strict mais lisible)
TYPE_ALLOWED_PATTERN = re.compile(r"^[A-Z0-9_-]{1,16}$")


# ---------------------------------------------------------------------------
# Utilitaires : verrou via lockfile
# ---------------------------------------------------------------------------
@dataclass
class LockInfo:
    pid: int
    timestamp: float


def _now_ts() -> float:
    """Retourne l'horodatage *epoch* en secondes (float)."""
    return time.time()


def _is_lock_stale(path: Path, max_age: float) -> bool:
    """Vrai si le lockfile existe et qu'il est plus vieux que `max_age` secondes."""
    try:
        mtime = path.stat().st_mtime
    except FileNotFoundError:
        return False
    return (_now_ts() - mtime) > max_age


def _write_lockfile(path: Path) -> None:
    """Crée le lockfile de manière exclusive.

    - Utilise `os.open(..., os.O_CREAT | os.O_EXCL | os.O_WRONLY)` pour éviter
      les courses (race conditions).
    - Écrit PID et timestamp à titre informatif (diagnostic).
    """
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    # Sur Windows, ajouter o_BINARY pour éviter les surprises
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(str(path), flags, 0o644)
    try:
        payload = json.dumps({"pid": os.getpid(), "ts": _now_ts()}).encode("utf-8")
        os.write(fd, payload)
    finally:
        os.close(fd)


def _remove_lockfile(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass


class FileLock:
    """Contexte de verrouillage basé sur lockfile.

    Usage :
        with FileLock(LOCK_PATH, timeout=5.0, stale=30.0):
            ... # accès exclusif
    """

    def __init__(self, path: Path, timeout: float, stale: float) -> None:
        self.path = path
        self.timeout = max(0.0, float(timeout))
        self.stale = max(0.0, float(stale))

    def __enter__(self):
        deadline = _now_ts() + self.timeout
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        while True:
            try:
                _write_lockfile(self.path)
                # Verrou acquis
                return self
            except FileExistsError:
                # Si le verrou est périmé, on le supprime prudemment
                if _is_lock_stale(self.path, self.stale):
                    try:
                        _remove_lockfile(self.path)
                        # boucle et retente immédiatement
                        continue
                    except Exception:
                        # En cas d'échec de suppression, on attend et on retente
                        pass
                # Si pas périmé → attendre un peu et retenter jusqu'au deadline
                if _now_ts() >= deadline:
                    raise TimeoutError(
                        f"Impossible d'obtenir le verrou {self.path.name} dans le délai alloué"
                    )
                time.sleep(0.05)  # attente courte pour réduire le busy-wait

    def __exit__(self, exc_type, exc, tb):
        _remove_lockfile(self.path)
        # ne supprime pas les exceptions éventuelles
        return False


# ---------------------------------------------------------------------------
# E/S JSON atomiques
# ---------------------------------------------------------------------------

def _atomic_write_json(path: Path, data: Dict[str, Dict[str, int]]) -> None:
    """Écrit `data` au format JSON de manière **atomique**.

    - Écrit dans un fichier temporaire situé dans le même dossier
    - `os.replace()` garantit une substitution atomique sur les OS modernes
    """
    tmp_path = path.with_suffix(path.suffix + TEMP_SUFFIX)
    encoded = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(encoded)
        f.flush()
        os.fsync(f.fileno())  # s'assurer que les octets sont poussés sur le disque
    os.replace(tmp_path, path)


def _read_json_or_default(path: Path) -> Dict[str, Dict[str, int]]:
    """Lit le fichier JSON si présent, sinon retourne une structure vide.

    Lève `ValueError` si le fichier est présent mais corrompu.
    """
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            obj = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Fichier JSON corrompu: {path}") from e
    # normalisation légère (garantie de types attendus)
    if not isinstance(obj, dict):
        raise ValueError("Schéma JSON inattendu (racine non dictionnaire)")
    normalized: Dict[str, Dict[str, int]] = {}
    for k, v in obj.items():
        if isinstance(v, dict):
            normalized[k] = {str(year): int(count) for year, count in v.items()}
    return normalized


# ---------------------------------------------------------------------------
# API publique
# ---------------------------------------------------------------------------

def next_number(Type: str, width: int = DEFAULT_WIDTH) -> Tuple[int, str]:
    """Retourne le **prochain numéro séquentiel** pour `Type` et la **chaîne formatée**.

    Paramètres
    ----------
    Type : str
        Identifiant du type de document (ex. "DEV", "INV"). Accepté : A-Z, 0-9,
        tiret et underscore, longueur 1..16. Sera **uppercased**.
    width : int, par défaut 6
        Largeur du compteur dans la chaîne (zéro-complété).

    Retour
    ------
    (seq_int, code_str) : tuple[int, str]
        - `seq_int` : valeur entière du compteur après incrément
        - `code_str`: chaîne formatée `TYPE-YYYY-DDMM-NNNNNN`

    Effets de bord
    --------------
    - Met à jour de façon atomique `Data/sequences.json`.
    - Empêche les accès concurrents via lockfile.
    """
    if not isinstance(Type, str) or not Type.strip():
        raise ValueError("`Type` doit être une chaîne non vide")

    doc_type = Type.strip().upper()
    if not TYPE_ALLOWED_PATTERN.match(doc_type):
        raise ValueError(
            "`Type` contient des caractères non autorisés (autorisé: A-Z, 0-9, -, _; 1..16)"
        )

    # Date courante (année pour le compteur, DDMM pour l'affichage)
    now = datetime.now()
    year_str = f"{now.year:d}"
    day_month_str = f"{now.day:02d}{now.month:02d}"  # DDMM (31 déc → 3112)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with FileLock(LOCK_PATH, timeout=DEFAULT_LOCK_TIMEOUT, stale=STALE_LOCK_SECONDS):
        data = _read_json_or_default(JSON_PATH)
        by_type: Dict[str, Dict[str, int]] = data.setdefault(doc_type, {})
        current_count = int(by_type.get(year_str, 0))
        next_count = current_count + 1
        by_type[year_str] = next_count
        _atomic_write_json(JSON_PATH, data)

    seq_int = next_count
    padded = str(seq_int).zfill(int(width))
    code_str = f"{doc_type}-{now.year}-{day_month_str}-{padded}"
    return seq_int, code_str


def get_initials(name: str, ascii_only: bool = True) -> str:
    """Extrait des **initiales** à partir d'un nom (avec accents pris en charge).

    Règles
    ------
    - On récupère les premiers caractères de chaque *segment alphabetique* du nom
      (lettres latines avec accents inclus). Ex.: "Jean-Luc Picard" → "JLP".
    - Si `ascii_only=True`, on supprime les diacritiques : "Élodie" → "E".
    - Retourne une chaîne **en majuscules**. Retourne "" si aucun segment.
    """
    if not isinstance(name, str) or not name.strip():
        return ""

    # Inclut les lettres accentuées (plages Unicode latines étendues)
    parts = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", name)
    if not parts:
        return ""

    initials = ''.join(p[0] for p in parts).upper()
    if ascii_only:
        # Normalisation NFD : décompose les lettres accentuées → suppression des marques diacritiques
        normalized = unicodedata.normalize('NFD', initials)
        initials = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return initials


def get_number(Type: str, name: str) -> str:
    """Retourne une **chaîne code** avec initiales ajoutées à la fin.

    - Utilise `next_number(Type)` pour produire et persister le compteur
    - Appelle `get_initials(name, ascii_only=True)`
    - Concatène sous la forme : `TYPE-YYYY-DDMM-NNNNNN-INITIALS`

    Note : si aucune initiale n'est trouvée, la chaîne se termine par un tiret
    final (comportement maintenu pour compatibilité : `...-`).
    """
    _, code_str = next_number(Type)
    initials = get_initials(name, ascii_only=True)
    return f"{code_str}-{initials}"


# ---------------------------------------------------------------------------
# Exécution directe (petite démonstration manuelle)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Exemple : génère un numéro pour des devis (DEV) et facture (INV)
    seq, code = next_number("DEV")
    print("DEV:", seq, code)

    seq, code = next_number("INV")
    print("INV:", seq, code)

    # Exemple avec initiales
    print("With initials:", get_number("DEV", "Jean-Luc Picard"))
