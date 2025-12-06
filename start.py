#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE DÉMARRAGE SIMPLE - TAL-migration
===========================================

Un seul script pour tout gérer :
- Vérifie l'état
- Teste la connexion
- Lance le transfert
- Monitore automatiquement
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent))

from gestion_transfert import gerer_transfert

if __name__ == "__main__":
    print("=" * 80)
    print("GESTION AUTOMATIQUE DU TRANSFERT DES FACTURES")
    print("=" * 80)
    print()
    
    gerer_transfert()

