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


def suivre_logs_temps_reel(duree_secondes=60):
    """Suit les logs en temps réel pendant une durée limitée."""
    try:
        log_files = list(Path(__file__).parent.glob('transfert_detaille_*.log'))
        if not log_files:
            log_message("⚠️  Aucun fichier log trouvé")
            return
        
        latest_log = max(log_files, key=os.path.getmtime)
        log_message(f"📄 Suivi du log: {latest_log.name}")
        log_message("=" * 80)
        
        # Lire les dernières lignes d'abord
        try:
            with open(latest_log, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                if lines:
                    print("\n" + "=" * 80)
                    print("📊 DERNIÈRES LIGNES DU LOG")
                    print("=" * 80 + "\n")
                    print("\n".join(lines[-15:]))  # Afficher les 15 dernières lignes
        except Exception as e:
            log_message(f"⚠️  Erreur lecture initiale: {e}")
        
        # Suivre en temps réel
        start_time = time.time()
        last_size = latest_log.stat().st_size if latest_log.exists() else 0
        
        print("\n" + "=" * 80)
        print(f"📊 SUIVI EN TEMPS RÉEL (durée: {duree_secondes}s - Appuyez sur Ctrl+C pour arrêter)")
        print("=" * 80 + "\n")
        
        try:
            while time.time() - start_time < duree_secondes:
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
                            log_message(f"⚠️  Erreur lecture: {e}")
                
                time.sleep(0.5)  # Vérifier toutes les 0.5 secondes
        except KeyboardInterrupt:
            print("\n\n⚠️  Suivi interrompu par l'utilisateur")
        
    except Exception as e:
        log_message(f"⚠️  Erreur suivi logs: {e}")
        import traceback
        log_message(traceback.format_exc())


def gerer_transfert(afficher_progression=True):
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
        log_message("")
        if afficher_progression:
            log_message("")
            log_message("📊 Affichage de la progression en temps réel...")
            log_message("💡 Le script tourne en arrière-plan, suivi des logs ci-dessous")
            log_message("")
            suivre_logs_temps_reel(duree_secondes=300)  # 5 minutes
        else:
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
        
        if afficher_progression:
            log_message("📊 Attente de démarrage (3 secondes)...")
            time.sleep(3)
            log_message("")
            log_message("=" * 80)
            suivre_logs_temps_reel(duree_secondes=300)  # 5 minutes de suivi
            log_message("")
            log_message("💡 Le suivi s'est terminé mais le script continue en arrière-plan")
            log_message("📝 Pour continuer à suivre: tail -f transfert_detaille_*.log")
        else:
            log_message("📝 Pour suivre en temps réel:")
            log_message("   tail -f transfert_detaille_*.log")
        
        log_message("")
        log_message("✅ Tout est configuré ! Le script tourne maintenant.")
        return True
    else:
        log_message("❌ Impossible de lancer le script")
        return False


def mode_watchdog(intervalle_verification=60):
    """Mode watchdog qui surveille et relance automatiquement."""
    log_message("🔄 Mode WATCHDOG activé")
    log_message(f"⏱️  Vérification toutes les {intervalle_verification} secondes")
    log_message("💡 Le script sera relancé automatiquement s'il s'arrête")
    log_message("🛑 Appuyez sur Ctrl+C pour arrêter le watchdog")
    log_message("")
    
    try:
        while True:
            script_en_cours = verifier_script_en_cours()
            activite_recente = verifier_activite_recente()
            
            if not script_en_cours or not activite_recente:
                if not script_en_cours:
                    log_message("⚠️  Script arrêté détecté - Relance automatique...")
                else:
                    log_message("⚠️  Script bloqué détecté - Relance automatique...")
                
                # Arrêter le processus bloqué si nécessaire
                if script_en_cours:
                    try:
                        subprocess.run(['pkill', '-f', 'transferer_factures_documents_v2.py'], timeout=5)
                        time.sleep(2)
                    except:
                        pass
                
                # Relancer
                progression = obtenir_progression()
                nb_factures = len(progression.get('factures_traitees', []))
                log_message(f"📊 Progression avant relance: {nb_factures} factures")
                
                if lancer_script():
                    log_message("✅ Script relancé avec succès")
                else:
                    log_message("❌ Erreur lors de la relance")
                    log_message("⏱️  Nouvelle tentative dans 30 secondes...")
                    time.sleep(30)
                    continue
            else:
                # Le script tourne bien, afficher un statut périodique
                progression = obtenir_progression()
                nb_factures = len(progression.get('factures_traitees', []))
                derniere_id = progression.get('derniere_facture_id', 0)
                log_message(f"✅ Script actif - {nb_factures} factures traitées (dernière ID: {derniere_id})")
            
            # Attendre avant la prochaine vérification
            time.sleep(intervalle_verification)
            
    except KeyboardInterrupt:
        log_message("\n⚠️  Watchdog arrêté par l'utilisateur")
        log_message("💡 Le script de transfert continue de tourner en arrière-plan")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Gestion automatique du transfert des factures')
    parser.add_argument('--no-display', action='store_true', help='Ne pas afficher la progression en temps réel')
    parser.add_argument('--watchdog', action='store_true', help='Mode watchdog - surveille et relance automatiquement')
    parser.add_argument('--interval', type=int, default=60, help='Intervalle de vérification en secondes (défaut: 60)')
    args = parser.parse_args()
    
    try:
        if args.watchdog:
            # Mode watchdog - surveille en continu
            gerer_transfert(afficher_progression=False)
            time.sleep(5)  # Attendre un peu après le démarrage
            mode_watchdog(intervalle_verification=args.interval)
        else:
            # Mode normal - lance une fois
            gerer_transfert(afficher_progression=not args.no_display)
    except KeyboardInterrupt:
        log_message("\n⚠️  Interrompu par l'utilisateur")
    except Exception as e:
        log_message(f"❌ Erreur fatale: {e}")
        import traceback
        log_message(traceback.format_exc())

