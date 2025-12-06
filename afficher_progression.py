#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Affiche la progression en temps réel
"""

from pathlib import Path
import time
import sys

def afficher_progression_temps_reel():
    """Affiche la progression en temps réel."""
    print("=" * 80)
    print("AFFICHAGE PROGRESSION EN TEMPS RÉEL")
    print("=" * 80)
    print()
    print("📊 Suivi des logs du transfert")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    print()
    print("=" * 80)
    print()
    
    # Trouver le dernier fichier log
    log_files = list(Path(__file__).parent.glob('transfert_detaille_*.log'))
    if not log_files:
        print("❌ Aucun fichier log trouvé")
        return
    
    latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
    print(f"📄 Fichier log: {latest_log.name}")
    print()
    
    # Lire les dernières lignes d'abord
    try:
        with open(latest_log, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            if lines:
                print("📋 Dernières lignes:")
                print("-" * 80)
                for line in lines[-20:]:
                    print(line.rstrip())
                print("-" * 80)
                print()
    except Exception as e:
        print(f"⚠️  Erreur lecture: {e}")
        return
    
    # Suivre en temps réel
    last_size = latest_log.stat().st_size if latest_log.exists() else 0
    
    print("📊 SUIVI EN TEMPS RÉEL (nouveautés uniquement)")
    print("=" * 80)
    print()
    
    try:
        while True:
            if latest_log.exists():
                current_size = latest_log.stat().st_size
                if current_size > last_size:
                    # Lire les nouvelles lignes
                    try:
                        with open(latest_log, 'r', encoding='utf-8', errors='ignore') as f:
                            f.seek(last_size)
                            new_content = f.read()
                            if new_content:
                                print(new_content, end='', flush=True)
                                last_size = current_size
                    except Exception as e:
                        print(f"⚠️  Erreur: {e}")
            
            time.sleep(0.5)  # Vérifier toutes les 0.5 secondes
    except KeyboardInterrupt:
        print("\n\n✅ Affichage arrêté")


if __name__ == "__main__":
    try:
        afficher_progression_temps_reel()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()



