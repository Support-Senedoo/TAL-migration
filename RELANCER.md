# 🔄 Comment relancer le script

## Sur PythonAnywhere (SSH)

### Méthode 1 : Relance simple (recommandé)
```bash
cd ~/TAL-migration
bash RELANCE_SIMPLE.sh
```

### Méthode 2 : Avec le script de démarrage
```bash
cd ~/TAL-migration
bash START.sh
```

### Méthode 3 : Relance complète (arrête tout et relance)
```bash
cd ~/TAL-migration
bash LANCER_TRANSFERT_COMPLET.sh
```

### Méthode 4 : Manuellement avec gestion automatique
```bash
cd ~/TAL-migration
python3.10 gestion_transfert.py
```

## Sur Windows (local)

```bash
# Option 1 : Avec le script batch
START.bat

# Option 2 : Directement avec Python
python gestion_transfert.py
```

## Voir la progression en temps réel

### Sur PythonAnywhere
```bash
cd ~/TAL-migration
python3.10 afficher_progression.py
```

### Ou directement les logs
```bash
tail -f ~/TAL-migration/transfert_detaille_*.log
```

## Commandes rapides

1. **Se connecter en SSH** (si sur PythonAnywhere) :
   ```bash
   ssh votre_compte@ssh.pythonanywhere.com
   ```

2. **Aller dans le dossier** :
   ```bash
   cd ~/TAL-migration
   ```

3. **Relancer** :
   ```bash
   bash RELANCE_SIMPLE.sh
   ```

4. **Voir la progression** (dans un autre terminal ou plus tard) :
   ```bash
   python3.10 afficher_progression.py
   ```

## ⚠️ Notes importantes

- ✅ Le script **reprend automatiquement** là où il s'est arrêté (grâce à `progression_transfert.json`)
- ✅ Aucun risque de perdre la progression déjà faite
- ✅ Le mode watchdog relance automatiquement si le script s'arrête

## Arrêter le script

```bash
bash ARRETER_SCRIPT.sh
```

