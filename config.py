#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONFIGURATION POUR TAL-migration
=================================

Fichier de configuration centralisé pour le projet TAL-migration.
Modifiez les valeurs ci-dessous selon votre environnement.
"""

# Configuration Odoo SaaS
ODOO_CONFIG = {
    'URL': 'https://tal-senegal.odoo.com/',  # URL de votre instance Odoo SaaS (PRODUCTION)
    'DB': 'tal-senegal',                      # Nom de la base de données (PRODUCTION)
    'USER': 'support@senedoo.com',             # Nom d'utilisateur
    'PASS': 'senedoo@2025'                      # Mot de passe
}

# Paramètres par défaut
DEFAULT_PARAMS = {
    'BATCH_SIZE': 100,          # Taille des lots pour les opérations en batch
    'TIMEOUT': 300,             # Timeout en secondes pour les opérations longues
    'RETRY_ATTEMPTS': 3,        # Nombre de tentatives en cas d'échec
    'RETRY_DELAY': 5,           # Délai entre les tentatives (secondes)
}

# Pour permettre l'importation
__all__ = ['ODOO_CONFIG', 'DEFAULT_PARAMS']


