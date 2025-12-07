# 📊 Guide d'affichage de la progression

## Vue d'ensemble

Le script de transfert affiche la progression de plusieurs façons :

### 1. **Pendant l'exécution** (dans la console)

Le script affiche :

- **Début** : Informations générales
  ```
  TRANSFERT DES FACTURES CLIENTS VERS LE MODULE DOCUMENT
  ==========================================================
  📊 Total de factures clients dans la base: XXX
  ✅ XXX factures récupérées
  📋 XXX factures à traiter
  ```

- **Toutes les 10 factures** (logs détaillés) :
  ```
  [10/500] Traitement facture F001 (ID: 123) - Client: Nom Client
     📁 Dossier créé pour client: Nom Client
     📄 Modèle PDF utilisé: Facture Client
     🔄 Génération PDF pour facture F001...
     📎 Création document dans Odoo pour facture F001...
     ✅ Document créé avec succès dans Odoo (ID document: 456)
     ⏱️  Temps de traitement: 3.45s
     ✅ Facture F001 traitée avec succès
  ```

- **Toutes les 50 factures** (résumé de progression) :
  ```
  ================================================================================
  📊 PROGRESSION: 50/500 (10%)
  ⏱️  Temps moyen: 3.42s/facture | ⚡ Vitesse: 17.5 factures/min
  ⏳ Temps restant estimé: 25.7 min
  ================================================================================
  ```

- **Fin** (résumé complet) :
  ```
  ============================================================
  RÉSUMÉ DU TRANSFERT
  ============================================================
  📊 Factures traitées        : 500
  📁 Dossiers créés          : 150
  📁 Dossiers réutilisés      : 350
  📎 Documents créés          : 500
  📎 Documents déjà existants: 0
  ⚠️  Factures sans PDF       : 0
  ❌ Erreurs                  : 0
  ⏱️  Temps total              : 28.50 minutes
  ⏱️  Temps moyen par facture  : 3.42 secondes
  💾 Progression sauvegardée: 500 factures
  ```

---

## 📁 Fichiers de progression

### 1. **progression_transfert.json**

Fichier JSON qui sauvegarde automatiquement la progression toutes les 10 factures.

**Localisation** : `~/TAL-migration/progression_transfert.json`

**Contenu** :
```json
{
  "factures_traitees": [123, 124, 125, ...],
  "derniere_facture_id": 125
}
```

### 2. **transfert_detaille_YYYYMMDD_HHMMSS.log**

Fichier log détaillé de chaque exécution.

**Localisation** : `~/TAL-migration/transfert_detaille_*.log`

**Contenu** : Tous les messages détaillés du script

---

## 🖥️ Commandes pour voir la progression

### 1. **Sur PythonAnywhere (via SSH)**

#### A. Voir la progression sauvegardée
```bash
cd ~/TAL-migration
python3.10 afficher_progression.py
```

#### B. Suivre en temps réel (actualisation toutes les 5 secondes)
```bash
python3.10 afficher_progression.py --watch
```

#### C. Voir un résumé complet
```bash
python3.10 afficher_progression.py --resume
```

#### D. Voir le dernier log en temps réel
```bash
tail -f transfert_detaille_*.log
```

#### E. Voir les 50 dernières lignes du dernier log
```bash
tail -50 $(ls -t transfert_detaille_*.log | head -1)
```

#### F. Voir la progression depuis le fichier JSON
```bash
cat progression_transfert.json | python3 -m json.tool
```

---

### 2. **Depuis Cursor (Windows)**

#### A. Utiliser le script d'affichage
```bash
cd TAL-migration
python afficher_progression.py
```

#### B. Suivre en temps réel
```bash
python afficher_progression.py --watch
```

#### C. Voir un résumé complet
```bash
python afficher_progression.py --resume
```

---

## 📊 Exemples d'affichage

### Affichage simple
```
================================================================================
📊 PROGRESSION DU TRANSFERT DES FACTURES
================================================================================

✅ Factures traitées     : 314
📋 Dernière facture ID   : 12345

📝 5 dernières factures traitées:
--------------------------------------------------------------------------------
   • Facture ID: 12341
   • Facture ID: 12342
   • Facture ID: 12343
   • Facture ID: 12344
   • Facture ID: 12345
--------------------------------------------------------------------------------

📄 Dernier fichier log: transfert_detaille_20241201_143022.log

📋 Dernières lignes du log:
--------------------------------------------------------------------------------
[2024-12-01 14:35:12] [314/500] Traitement facture F314 (ID: 12345) - Client: ABC Corp
[2024-12-01 14:35:13]    ✅ Document créé avec succès dans Odoo (ID document: 67890)
[2024-12-01 14:35:13]    ⏱️  Temps de traitement: 3.21s
--------------------------------------------------------------------------------

💡 Actualisation automatique toutes les 5 secondes...
🛑 Appuyez sur Ctrl+C pour arrêter
```

---

## 🔍 Vérifier que le script tourne

### Sur PythonAnywhere
```bash
# Vérifier les processus Python
ps aux | grep transferer_factures_documents_v2.py

# Vérifier si le log est mis à jour récemment
ls -lh transfert_detaille_*.log
```

---

## 💡 Astuces

1. **Mode watch continu** : Utilisez `--watch` pour voir la progression se mettre à jour automatiquement
2. **Résumé rapide** : Utilisez `--resume` pour un aperçu complet sans suivi
3. **Logs en temps réel** : Utilisez `tail -f` pour voir les logs au fur et à mesure
4. **Vérifier la dernière activité** : Regardez la date de modification du fichier log

---

## ⚙️ Paramètres d'affichage dans le script

Le script principal (`transferer_factures_documents_v2.py`) utilise :

- **LOG_FREQUENCY = 10** : Logs détaillés toutes les 10 factures
- **SAVE_FREQUENCY = 10** : Sauvegarde de progression toutes les 10 factures
- **Résumé toutes les 50 factures** : Affichage du résumé de progression

Ces paramètres sont optimisés pour un bon équilibre entre visibilité et performance.

