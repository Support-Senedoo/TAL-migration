#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT D'IMPORTATION DU PLAN COMPTABLE DANS ODOO
================================================

Ce script lit le fichier Excel filtré 'Plan_Comptable_Filtre_8chiffres.xlsx'
et importe uniquement les comptes à 8 chiffres dans Odoo.

Auteur: Assistant IA
Date: 2025-11-29
"""

import pandas as pd
import re
import sys
from pathlib import Path
from connexion_odoo import connecter_odoo
import time

# Configurer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def lire_plan_comptable_filtre():
    """
    Lit le fichier Excel filtré avec les comptes à 8 chiffres.
    
    Returns:
        DataFrame pandas ou None
    """
    fichier_excel = Path(__file__).parent / 'Plan_Comptable_Filtre_8chiffres.xlsx'
    
    if not fichier_excel.exists():
        print(f"❌ Erreur: Le fichier '{fichier_excel}' n'existe pas.")
        print(f"   Veuillez d'abord exécuter lecture_plan_comptable.py pour créer le fichier filtré.")
        return None
    
    try:
        df = pd.read_excel(fichier_excel, engine='openpyxl')
        print(f"✅ Fichier Excel lu avec succès!")
        print(f"   📊 {len(df)} lignes lues")
        
        # Filtrer pour ne garder que les comptes à 8 chiffres
        if 'N° compte' in df.columns:
            def est_compte_8_chiffres(value):
                if pd.isna(value):
                    return False
                compte_str = str(value).strip()
                return bool(re.match(r'^\d{8}$', compte_str))
            
            df_filtre = df[df['N° compte'].apply(est_compte_8_chiffres)].copy()
            print(f"   ✅ {len(df_filtre)} comptes à 8 chiffres trouvés")
            print(f"   📉 {len(df) - len(df_filtre)} lignes filtrées (non conformes)")
            
            return df_filtre
        else:
            print(f"❌ Colonne 'N° compte' non trouvée dans le fichier Excel")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {str(e)}")
        return None


def determiner_type_compte(code_compte):
    """
    Détermine le type de compte comptable basé sur son code (plan OHADA).
    
    Args:
        code_compte: Code du compte (string de 8 chiffres)
    
    Returns:
        Type de compte Odoo (internal_group)
    """
    if not code_compte or len(str(code_compte)) < 2:
        return 'expense'
    
    code = str(code_compte)[:2]
    
    # Plan comptable OHADA
    if code.startswith('1'):  # Classe 1: Financement permanent
        if code.startswith('10') or code.startswith('11') or code.startswith('12') or code.startswith('15'):
            return 'equity'
        elif code.startswith('13'):
            return 'equity_unaffected'
        elif code.startswith('16') or code.startswith('17') or code.startswith('18'):
            return 'liability_non_current'
        else:
            return 'equity'
    
    elif code.startswith('2'):  # Classe 2: Actif immobilisé
        return 'asset_fixed'
    
    elif code.startswith('3'):  # Classe 3: Stocks
        return 'asset_current'
    
    elif code.startswith('4'):  # Classe 4: Tiers
        if code.startswith('411'):
            return 'asset_receivable'
        elif code.startswith('41'):
            return 'liability_payable'
        elif code.startswith('42') or code.startswith('43') or code.startswith('44') or code.startswith('45'):
            return 'liability_current'
        elif code.startswith('46'):
            return 'asset_current'
        elif code.startswith('47'):
            return 'liability_current'
        else:
            return 'asset_current'
    
    elif code.startswith('5'):  # Classe 5: Trésorerie
        return 'asset_cash'
    
    elif code.startswith('6'):  # Classe 6: Charges
        return 'expense'
    
    elif code.startswith('7'):  # Classe 7: Produits
        return 'income'
    
    elif code.startswith('8'):  # Classe 8: Résultats
        return 'expense'
    
    else:
        return 'expense'


def importer_comptes_8_chiffres():
    """
    Importe les comptes à 8 chiffres depuis le fichier Excel dans Odoo.
    """
    print("=" * 60, flush=True)
    print("IMPORTATION DES COMPTES A 8 CHIFFRES DANS ODOO", flush=True)
    print("=" * 60, flush=True)
    
    # Lire le fichier Excel
    print("\nEtape 1: Lecture du fichier Excel...", flush=True)
    df = lire_plan_comptable_filtre()
    if df is None:
        return False
    
    # Vérifier les colonnes nécessaires
    if 'N° compte' not in df.columns or 'Intitulé du compte' not in df.columns:
        print("Erreur: Colonnes 'N° compte' ou 'Intitulé du compte' manquantes", flush=True)
        return False
    
    # Connexion à Odoo
    print(f"\nEtape 2: Connexion a Odoo...", flush=True)
    uid, models, db, password = connecter_odoo()
    
    if not uid:
        print("❌ Impossible de se connecter à Odoo.")
        return False
    
    try:
        # Statistiques
        stats = {
            'total': len(df),
            'crees': 0,
            'deja_existants': 0,
            'echecs': 0
        }
        
        comptes_crees = []
        comptes_existants = []
        echecs = []
        
        print(f"\nEtape 3: Importation de tous les comptes...", flush=True)
        print(f"   Total de comptes a importer: {len(df)}", flush=True)
        print(f"   Traitement par lots de 50 comptes\n", flush=True)
        
        # Traiter par lots
        BATCH_SIZE = 50
        total_lots = (len(df) + BATCH_SIZE - 1) // BATCH_SIZE
        
        for lot_num in range(total_lots):
            debut = lot_num * BATCH_SIZE
            fin = min(debut + BATCH_SIZE, len(df))
            lot_df = df.iloc[debut:fin]
            
            print(f"   Lot {lot_num + 1}/{total_lots}: {len(lot_df)} comptes", flush=True)
            
            for idx, row in lot_df.iterrows():
                code_compte = str(row['N° compte']).strip()
                intitule = str(row['Intitulé du compte']).strip() if pd.notna(row['Intitulé du compte']) else f"Compte {code_compte}"
                
                # Vérifier que le compte a bien 8 chiffres
                if not re.match(r'^\d{8}$', code_compte):
                    stats['echecs'] += 1
                    echecs.append(f"{code_compte}: Le compte n'a pas 8 chiffres")
                    continue
                
                try:
                    # Vérifier si le compte existe déjà
                    existing = models.execute_kw(
                        db, uid, password,
                        'account.account', 'search',
                        [[['code', '=', code_compte]]]
                    )
                    
                    if existing:
                        stats['deja_existants'] += 1
                        comptes_existants.append(code_compte)
                        print(f"         -> Deja existant: {code_compte} - {intitule}", flush=True)
                        continue
                    
                    # Déterminer le type de compte
                    account_type = determiner_type_compte(code_compte)
                    
                    # Déterminer si le compte doit être réconciliable
                    # Les comptes clients (411) et fournisseurs (401) doivent être réconciliables
                    doit_reconcilier = False
                    if code_compte.startswith('411') or code_compte.startswith('401'):
                        doit_reconcilier = True
                    
                    # Créer le compte avec account_type directement (Odoo 19)
                    account_data = {
                        'code': code_compte,
                        'name': intitule,
                        'account_type': account_type,
                        'reconcile': doit_reconcilier,
                    }
                    
                    account_id = models.execute_kw(
                        db, uid, password,
                        'account.account', 'create',
                        [account_data]
                    )
                    
                    stats['crees'] += 1
                    comptes_crees.append(f"{code_compte} - {intitule}")
                    print(f"         -> Cree: {code_compte} - {intitule} (ID: {account_id})", flush=True)
                    
                except Exception as e:
                    error_msg = str(e)
                    # Si c'est une erreur de compte client/fournisseur, essayer avec reconcile=True
                    if "client/fournisseur" in error_msg.lower() and not doit_reconcilier:
                        try:
                            print(f"      Nouvelle tentative avec reconcile=True pour {code_compte}...", flush=True)
                            account_data['reconcile'] = True
                            account_id = models.execute_kw(
                                db, uid, password,
                                'account.account', 'create',
                                [account_data]
                            )
                            stats['crees'] += 1
                            comptes_crees.append(f"{code_compte} - {intitule}")
                            print(f"         -> Cree (avec reconcile): {code_compte} - {intitule} (ID: {account_id})", flush=True)
                            continue
                        except Exception as e2:
                            # Si ça échoue encore, on garde l'erreur originale
                            pass
                    
                    stats['echecs'] += 1
                    echecs.append(f"{code_compte}: {str(error_msg)[:80]}")
                    print(f"      Erreur pour {code_compte}: {str(error_msg)[:80]}", flush=True)
            
            # Afficher la progression
            progress = (lot_num + 1) * 100 // total_lots
            print(f"      Progression: {stats['crees']} crees, {stats['deja_existants']} existants, {stats['echecs']} echecs - Total: {stats['crees'] + stats['deja_existants'] + stats['echecs']}/{stats['total']} ({progress}%)", flush=True)
            
            # Petite pause entre les lots
            if lot_num < total_lots - 1:
                time.sleep(0.3)
        
        # Résumé final
        print(f"\n" + "=" * 60)
        print("RÉSUMÉ DE L'IMPORTATION")
        print("=" * 60)
        print(f"\n📊 Statistiques:")
        print(f"   ✅ Comptes créés: {stats['crees']}")
        print(f"   📋 Comptes déjà existants: {stats['deja_existants']}")
        print(f"   ❌ Échecs: {stats['echecs']}")
        print(f"   📊 Total traité: {stats['crees'] + stats['deja_existants'] + stats['echecs']}/{stats['total']}")
        
        if comptes_crees:
            print(f"\n📄 Premiers comptes créés (max 20):")
            for i, compte in enumerate(comptes_crees[:20], 1):
                print(f"   {i}. {compte}")
            if len(comptes_crees) > 20:
                print(f"   ... et {len(comptes_crees) - 20} autres comptes")
        
        if echecs:
            print(f"\n❌ Échecs (max 10):")
            for i, echec in enumerate(echecs[:10], 1):
                print(f"   {i}. {echec}")
            if len(echecs) > 10:
                print(f"   ... et {len(echecs) - 10} autres échecs")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'importation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        print("Demarrage du script d'importation...")
        result = importer_comptes_8_chiffres()
        if result:
            print("\nImportation terminee avec succes!")
        else:
            print("\nImportation terminee avec des erreurs")
    except Exception as e:
        print(f"\nErreur fatale: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
