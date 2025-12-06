# 🔄 RELANCE RAPIDE DU TRANSFERT

## Sur PythonAnywhere (SSH)

### Option 1 : Relance automatique (recommandé)
```bash
cd ~/TAL-migration
bash START.sh
```

### Option 2 : Relance avec watchdog (surveillance continue)
```bash
cd ~/TAL-migration
bash LANCER_AVEC_WATCHDOG.sh
```

### Option 3 : Relance complète (arrête + relance)
```bash
cd ~/TAL-migration
bash LANCER_TRANSFERT_COMPLET.sh
```

### Option 4 : Relance manuelle avec gestion_transfert
```bash
cd ~/TAL-migration
python3.10 gestion_transfert.py
```

## Vérifier que le script tourne

```bash
cd ~/TAL-migration
python3.10 gestion_transfert.py --status
```

## Voir la progression en temps réel

```bash
cd ~/TAL-migration
python3.10 afficher_progression.py
```

Ou directement :
```bash
tail -f ~/TAL-migration/transfert_detaille_*.log
```

## Arrêter le script

```bash
cd ~/TAL-migration
bash ARRETER_SCRIPT.sh
```

## Commandes rapides

### 1. Se connecter en SSH
```
ssh votre_compte@ssh.pythonanywhere.com
```

### 2. Aller dans le dossier
```bash
cd ~/TAL-migration
```

### 3. Relancer
```bash
bash START.sh
```

### 4. Voir la progression (dans un autre terminal)
```bash
tail -f ~/TAL-migration/transfert_detaille_*.log
```

## 📝 Notes

- Le script `START.sh` lance automatiquement le mode watchdog qui surveille et relance si arrêt
- Le script reprend automatiquement là où il s'est arrêté (grâce à `progression_transfert.json`)
- Vous pouvez arrêter avec Ctrl+C puis relancer sans perdre la progression

