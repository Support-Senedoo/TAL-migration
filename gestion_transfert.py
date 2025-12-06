#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GESTION AUTOMATIQUE DU TRANSFERT DES FACTURES
==============================================

Script maître qui gère automatiquement :
- Vérification de l'état du script
- Relance automatique si arrêté
- Tests automatiques
- Monitoring continu
"""

import subprocess
import time
import os
import sys
from pathlib import Path
import json
from datetime import datetime

# Chemin du script principal
SCRIPT_PRINCIPAL = Path(__file__).parent / 'transferer_factures_documents_v2.py'
FICHIER_PROGRESSION = Path(__file__).parent / 'progression_transfert.json'
FICHIER_LOG_GESTION = Path(__file__).parent / 'gestion_transfert.log'


def log_message(message):
    """Log un message avec timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_complet = f"[{timestamp}] {message}"
    print(message_complet)
    try:
        with open(FICHIER_LOG_GESTION, 'a', encoding='utf-8') as f:
            f.write(message_complet + '\n')
    except:
        pass


def verifier_script_en_cours():
    """Vérifie si le script de transfert est en cours d'exécution."""
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'transferer_factures_documents_v2.py'],
            capture_output=True,
            text=True
        )
        return bool(result.stdout.strip())
    except:
        # Si pgrep n'est pas disponible, utiliser ps
        try:
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True
            )
            return 'transferer_factures_documents_v2.py' in result.stdout
        except:
            return False


def verifier_activite_recente():
    """Vérifie si le script a été actif récemment (dernières 5 minutes)."""
    try:
        # Trouver le dernier fichier log
        log_files = list(Path(__file__).parent.glob('transfert_detaille_*.log'))
        if not log_files:
            return False
        
        latest_log = max(log_files, key=os.path.getmtime)
        
        # Vérifier la dernière modification
        last_modified = os.path.getmtime(latest_log)
        time_diff = time.time() - last_modified
        
        # Si modifié il y a moins de 5 minutes, c'est actif
        if time_diff < 300:  # 5 minutes
            # Vérifier aussi la dernière ligne du log
            try:
                with open(latest_log, 'rb') as f:
                    f.seek(0, 2)  # Aller à la fin
                    size = f.tell()
                    if size > 1024:  # Si le fichier fait plus de 1KB
                        f.seek(max(0, size - 500))  # Lire les 500 derniers bytes
                        content = f.read().decode('utf-8', errors='ignore')
                        # Vérifier si on a une ligne récente (avec timestamp d'aujourd'hui)
                        today = datetime.now().strftime('%Y-%m-%d')
                        if today in content:
                            # Extraire le dernier timestamp
                            lines = content.split('\n')
                            for line in reversed(lines):
                                if '[' + today in line and ']' in line:
                                    try:
                                        timestamp_str = line.split('[')[1].split(']')[0]
                                        log_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                                        time_diff = (datetime.now() - log_time).total_seconds()
                                        return time_diff < 600  # 10 minutes
                                    except:
                                        pass
            except:
                pass
        
        return time_diff < 300
    except Exception as e:
        log_message(f"⚠️  Erreur vérification activité: {e}")
        return False


def obtenir_progression():
    """Obtient la progression actuelle."""
    if not FICHIER_PROGRESSION.exists():
        return {'factures_traitees': [], 'derniere_facture_id': 0}
    
    try:
        with open(FICHIER_PROGRESSION, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {'factures_traitees': [], 'derniere_facture_id': 0}


def lancer_script():
    """Lance le script de transfert en arrière-plan."""
    log_file = Path(__file__).parent / f'transfert_detaille_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    # Lancer en arrière-plan
    try:
        process = subprocess.Popen(
            [sys.executable, str(SCRIPT_PRINCIPAL)],
            stdout=open(log_file, 'w', encoding='utf-8'),
            stderr=subprocess.STDOUT,
            cwd=str(Path(__file__).parent)
        )
        log_message(f"✅ Script lancé (PID: {process.pid}, Log: {log_file.name})")
        return True
    except Exception as e:
        log_message(f"❌ Erreur lors du lancement: {e}")
        return False


def tester_connexion():
    """Teste la connexion à Odoo."""
    try:
        from connexion_odoo import connecter_odoo
        uid, models, db, password = connecter_odoo()
        if uid:
            log_message("✅ Connexion Odoo réussie")
            return True
        else:
            log_message("❌ Connexion Odoo échouée")
            return False
    except Exception as e:
        log_message(f"❌ Erreur test connexion: {e}")
        return False


def afficher_statut():
    """Affiche le statut actuel."""
    progression = obtenir_progression()
    nb_factures = len(progression.get('factures_traitees', []))
    derniere_id = progression.get('derniere_facture_id', 0)
    
    script_en_cours = verifier_script_en_cours()
    activite_recente = verifier_activite_recente()
    
    log_message("=" * 80)
    log_message("STATUT DU TRANSFERT")
    log_message("=" * 80)
    log_message(f"📊 Factures traitées: {nb_factures}")
    log_message(f"📋 Dernière facture ID: {derniere_id}")
    log_message(f"🔄 Script en cours: {'✅ Oui' if script_en_cours else '❌ Non'}")
    log_message(f"⏱️  Activité récente: {'✅ Oui' if activite_recente else '❌ Non'}")
    log_message("=" * 80)


def gerer_transfert():
    """Gère automatiquement le transfert."""
    log_message("🚀 Démarrage de la gestion automatique du transfert")
    log_message("")
    
    # Test de connexion
    log_message("🔍 Test de la connexion Odoo...")
    if not tester_connexion():
        log_message("❌ Impossible de se connecter à Odoo. Vérifiez config.py")
        return False
    
    # Afficher le statut
    afficher_statut()
    
    # Vérifier si le script tourne
    script_en_cours = verifier_script_en_cours()
    activite_recente = verifier_activite_recente()
    
    if script_en_cours and activite_recente:
        log_message("✅ Le script tourne correctement et est actif")
        log_message("💡 Le script continuera automatiquement")
        log_message("📝 Pour suivre: tail -f transfert_detaille_*.log")
        return True
    
    if script_en_cours and not activite_recente:
        log_message("⚠️  Le script tourne mais semble bloqué")
        log_message("🛑 Arrêt du processus bloqué...")
        try:
            subprocess.run(['pkill', '-f', 'transferer_factures_documents_v2.py'], timeout=5)
            time.sleep(2)
        except:
            pass
    
    # Lancer ou relancer le script
    log_message("🚀 Lancement du script de transfert...")
    if lancer_script():
        log_message("✅ Script lancé avec succès")
        log_message("")
        log_message("📊 Le script va :")
        log_message("   - Reprendre automatiquement après la dernière facture traitée")
        log_message("   - Traiter toutes les factures restantes")
        log_message("   - Sauvegarder la progression automatiquement")
        log_message("")
        log_message("📝 Pour suivre en temps réel:")
        log_message("   tail -f transfert_detaille_*.log")
        log_message("")
        log_message("✅ Tout est configuré ! Le script tourne maintenant.")
        return True
    else:
        log_message("❌ Impossible de lancer le script")
        return False


if __name__ == "__main__":
    try:
        gerer_transfert()
    except KeyboardInterrupt:
        log_message("\n⚠️  Interrompu par l'utilisateur")
    except Exception as e:
        log_message(f"❌ Erreur fatale: {e}")
        import traceback
        log_message(traceback.format_exc())

