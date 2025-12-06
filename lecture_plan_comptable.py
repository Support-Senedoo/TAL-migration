#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE LECTURE DU PLAN COMPTABLE
====================================

Ce script ouvre et lit le fichier Excel 'Plan Comptable.xlsx'
et affiche son contenu.

Auteur: Assistant IA
Date: 2025-11-29
"""

import pandas as pd
import os
import re
from pathlib import Path

def ouvrir_plan_comptable():
    """
    Ouvre le fichier Excel 'Plan Comptable.xlsx' et affiche son contenu.
    """
    # Chemin du fichier
    fichier_excel = Path(__file__).parent / 'Plan Comptable.xlsx'
    
    print("=" * 60)
    print("LECTURE DU PLAN COMPTABLE")
    print("=" * 60)
    print(f"\n📁 Fichier: {fichier_excel}")
    
    # Vérifier si le fichier existe
    if not fichier_excel.exists():
        print(f"❌ Erreur: Le fichier '{fichier_excel}' n'existe pas.")
        return None
    
    try:
        # Lire le fichier Excel
        print(f"\n🔍 Ouverture du fichier Excel...")
        
        # Lire toutes les feuilles
        excel_file = pd.ExcelFile(fichier_excel)
        feuilles = excel_file.sheet_names
        
        print(f"✅ Fichier ouvert avec succès!")
        print(f"\n📊 Nombre de feuilles: {len(feuilles)}")
        print(f"📋 Noms des feuilles: {', '.join(feuilles)}")
        
        # Afficher le contenu de chaque feuille
        for i, feuille in enumerate(feuilles, 1):
            print(f"\n" + "=" * 60)
            print(f"FEUILLE {i}: {feuille}")
            print("=" * 60)
            
            # Lire la feuille
            df = pd.read_excel(fichier_excel, sheet_name=feuille)
            
            print(f"\n📐 Dimensions brutes: {df.shape[0]} lignes × {df.shape[1]} colonnes")
            
            # Nettoyer les colonnes vides
            df_cleaned = df.dropna(axis=1, how='all')  # Supprimer les colonnes entièrement vides
            print(f"📐 Dimensions nettoyées: {df_cleaned.shape[0]} lignes × {df_cleaned.shape[1]} colonnes")
            
            # Afficher les colonnes non vides
            colonnes_non_vides = [col for col in df_cleaned.columns if not col.startswith('Unnamed')]
            print(f"📝 Colonnes principales: {', '.join(colonnes_non_vides)}")
            
            # Filtrer les lignes avec des données (au moins une colonne non vide)
            df_with_data = df_cleaned.dropna(axis=0, how='all')
            print(f"📊 Lignes avec données: {len(df_with_data)}")
            
            # Filtrer pour ne garder que les comptes à 8 chiffres
            if 'N° compte' in df_with_data.columns:
                print(f"\n🔍 Filtrage des comptes à 8 chiffres...")
                
                # Fonction pour vérifier si un numéro de compte a exactement 8 chiffres
                def est_compte_8_chiffres(value):
                    if pd.isna(value):
                        return False
                    # Convertir en string et enlever les espaces
                    compte_str = str(value).strip()
                    # Vérifier qu'il contient exactement 8 chiffres
                    return bool(re.match(r'^\d{8}$', compte_str))
                
                # Filtrer les lignes avec des comptes à 8 chiffres
                df_comptes_8 = df_with_data[df_with_data['N° compte'].apply(est_compte_8_chiffres)]
                
                print(f"✅ Comptes à 8 chiffres trouvés: {len(df_comptes_8)}")
                print(f"📉 Lignes filtrées: {len(df_with_data) - len(df_comptes_8)} lignes supprimées")
                
                # Afficher les premières lignes filtrées
                print(f"\n📄 Premières lignes (comptes à 8 chiffres uniquement):")
                if len(df_comptes_8) > 0:
                    # Afficher seulement les colonnes principales
                    cols_to_show = [col for col in colonnes_non_vides if col in df_comptes_8.columns]
                    if cols_to_show:
                        print(df_comptes_8[cols_to_show].head(30).to_string())
                    else:
                        print(df_comptes_8.head(30).to_string())
                else:
                    print("   Aucun compte à 8 chiffres trouvé.")
                
                # Afficher des statistiques
                print(f"\n📊 Informations sur les données filtrées:")
                print(f"   - Lignes totales: {len(df)}")
                print(f"   - Lignes avec données: {len(df_with_data)}")
                print(f"   - Lignes avec comptes à 8 chiffres: {len(df_comptes_8)}")
                print(f"   - Colonnes: {len(df.columns)}")
                print(f"   - Colonnes avec données: {len(df_cleaned.columns)}")
                
                # Compter les valeurs non nulles par colonne principale
                if colonnes_non_vides and len(df_comptes_8) > 0:
                    print(f"\n   - Valeurs non nulles par colonne principale (comptes à 8 chiffres):")
                    for col in colonnes_non_vides:
                        if col in df_comptes_8.columns:
                            nb_non_null = df_comptes_8[col].notna().sum()
                            print(f"     • {col}: {nb_non_null} valeurs")
                
                # Retourner le DataFrame filtré
                return df_comptes_8
            else:
                print(f"\n⚠️  Colonne 'N° compte' non trouvée dans les colonnes principales")
                print(f"📄 Premières lignes avec données:")
                if len(df_with_data) > 0:
                    cols_to_show = [col for col in colonnes_non_vides if col in df_with_data.columns]
                    if cols_to_show:
                        print(df_with_data[cols_to_show].head(20).to_string())
                    else:
                        print(df_with_data.head(20).to_string())
                
                # Afficher des statistiques
                print(f"\n📊 Informations sur les données:")
                print(f"   - Lignes totales: {len(df)}")
                print(f"   - Lignes avec données: {len(df_with_data)}")
                print(f"   - Colonnes: {len(df.columns)}")
                print(f"   - Colonnes avec données: {len(df_cleaned.columns)}")
                
                return df_with_data
        
        return None  # Retourne None car on retourne déjà le DataFrame filtré dans la boucle
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'ouverture du fichier: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def lire_feuille_specifique(nom_feuille):
    """
    Lit une feuille spécifique du fichier Excel.
    
    Args:
        nom_feuille: Nom de la feuille à lire
    
    Returns:
        DataFrame pandas ou None
    """
    fichier_excel = Path(__file__).parent / 'Plan Comptable.xlsx'
    
    if not fichier_excel.exists():
        print(f"❌ Erreur: Le fichier '{fichier_excel}' n'existe pas.")
        return None
    
    try:
        df = pd.read_excel(fichier_excel, sheet_name=nom_feuille)
        print(f"✅ Feuille '{nom_feuille}' lue avec succès!")
        print(f"📐 Dimensions: {df.shape[0]} lignes × {df.shape[1]} colonnes")
        return df
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de la feuille '{nom_feuille}': {str(e)}")
        return None


def filtrer_comptes_8_chiffres(fichier_excel=None, nom_feuille=None):
    """
    Filtre le plan comptable pour ne garder que les comptes à 8 chiffres.
    
    Args:
        fichier_excel: Chemin du fichier Excel (optionnel, utilise 'Plan Comptable.xlsx' par défaut)
        nom_feuille: Nom de la feuille à lire (optionnel, lit toutes les feuilles par défaut)
    
    Returns:
        DataFrame pandas avec uniquement les comptes à 8 chiffres
    """
    if fichier_excel is None:
        fichier_excel = Path(__file__).parent / 'Plan Comptable.xlsx'
    else:
        fichier_excel = Path(fichier_excel)
    
    if not fichier_excel.exists():
        print(f"❌ Erreur: Le fichier '{fichier_excel}' n'existe pas.")
        return None
    
    try:
        if nom_feuille:
            df = pd.read_excel(fichier_excel, sheet_name=nom_feuille)
        else:
            # Lire la première feuille par défaut
            excel_file = pd.ExcelFile(fichier_excel)
            df = pd.read_excel(fichier_excel, sheet_name=excel_file.sheet_names[0])
        
        # Nettoyer les colonnes vides
        df_cleaned = df.dropna(axis=1, how='all')
        df_with_data = df_cleaned.dropna(axis=0, how='all')
        
        # Filtrer pour ne garder que les comptes à 8 chiffres
        if 'N° compte' in df_with_data.columns:
            def est_compte_8_chiffres(value):
                if pd.isna(value):
                    return False
                compte_str = str(value).strip()
                return bool(re.match(r'^\d{8}$', compte_str))
            
            df_comptes_8 = df_with_data[df_with_data['N° compte'].apply(est_compte_8_chiffres)]
            return df_comptes_8
        else:
            print("⚠️  Colonne 'N° compte' non trouvée")
            return df_with_data
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return None


def exporter_vers_excel(df, nom_fichier=None, colonnes_a_exporter=None):
    """
    Exporte un DataFrame vers un fichier Excel.
    
    Args:
        df: DataFrame pandas à exporter
        nom_fichier: Nom du fichier de sortie (optionnel)
        colonnes_a_exporter: Liste des colonnes à exporter (optionnel, toutes par défaut)
    
    Returns:
        Chemin du fichier créé ou None en cas d'erreur
    """
    if df is None or df.empty:
        print("❌ Erreur: Aucune donnée à exporter.")
        return None
    
    if nom_fichier is None:
        nom_fichier = 'Plan_Comptable_Filtre_8chiffres.xlsx'
    
    fichier_sortie = Path(__file__).parent / nom_fichier
    
    try:
        print(f"\n💾 Export vers Excel...")
        print(f"   Fichier: {fichier_sortie}")
        
        # Filtrer les colonnes à exporter si spécifié
        if colonnes_a_exporter:
            # Garder seulement les colonnes qui existent dans le DataFrame
            colonnes_existantes = [col for col in colonnes_a_exporter if col in df.columns]
            if colonnes_existantes:
                df_export = df[colonnes_existantes].copy()
            else:
                print("⚠️  Aucune colonne spécifiée n'existe dans le DataFrame, export de toutes les colonnes")
                df_export = df.copy()
        else:
            # Par défaut, ne garder que les colonnes principales (pas les "Unnamed")
            colonnes_principales = [col for col in df.columns if not col.startswith('Unnamed')]
            if colonnes_principales:
                df_export = df[colonnes_principales].copy()
            else:
                df_export = df.copy()
        
        # Exporter vers Excel
        df_export.to_excel(fichier_sortie, index=False, engine='openpyxl')
        
        print(f"✅ Export réussi!")
        print(f"   📁 Fichier créé: {fichier_sortie}")
        print(f"   📊 Nombre de lignes exportées: {len(df_export)}")
        print(f"   📝 Colonnes exportées: {', '.join(df_export.columns.tolist())}")
        
        return fichier_sortie
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Ouvrir et afficher le contenu du fichier avec filtrage
    df_filtre = ouvrir_plan_comptable()
    
    if df_filtre is not None:
        print(f"\n" + "=" * 60)
        print("✅ Lecture et filtrage terminés avec succès!")
        print("=" * 60)
        print(f"\n💾 Le DataFrame filtré contient {len(df_filtre)} comptes à 8 chiffres")
        
        # Exporter le résultat filtré dans un nouveau fichier Excel
        # Ne garder que les colonnes principales (N° compte et Intitulé du compte)
        fichier_exporte = exporter_vers_excel(df_filtre, colonnes_a_exporter=['N° compte', 'Intitulé du compte'])
        
        if fichier_exporte:
            print(f"\n" + "=" * 60)
            print("✅ Export terminé avec succès!")
            print("=" * 60)

