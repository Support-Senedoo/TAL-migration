# 🔌 Se reconnecter et vérifier l'état du script

## 🔌 Étape 1 : Se reconnecter à PythonAnywhere

### Via SSH (depuis votre terminal local)

```bash
ssh votre_compte@ssh.pythonanywhere.com
```

Remplacez `votre_compte` par votre nom d'utilisateur PythonAnywhere.

### Ou via le navigateur

1. Allez sur https://www.pythonanywhere.com
2. Connectez-vous
3. Cliquez sur "Consoles" dans le menu
4. Cliquez sur "Bash" pour ouvrir une console

---

## 🔍 Étape 2 : Vérifier si le script tourne toujours

### Méthode 1 : Vérifier les processus

```bash
# Voir si le script Python tourne
ps aux | grep transferer_factures_documents_v2.py

# Ou avec pgrep (plus propre)
pgrep -f transferer_factures_documents_v2.py
```

**Résultat attendu :**
- Si vous voyez une ligne avec `python3.10 transferer_factures_documents_v2.py`, le script tourne
- Si aucune ligne, le script s'est arrêté

### Méthode 2 : Utiliser l'outil de vérification

```bash
cd ~/TAL-migration
python3.10 verifier_blocage.py
```

Cet outil vous dira automatiquement si le script tourne et affichera l'état complet.

---

## 📊 Étape 3 : Voir la progression actuelle

### Voir la progression sauvegardée

```bash
cd ~/TAL-migration

# Résumé de la progression
python3.10 afficher_progression.py --resume
```

### Voir la progression en temps réel

```bash
python3.10 afficher_progression.py --watch
```

### Voir les dernières lignes du log

```bash
# Voir les 50 dernières lignes
tail -50 $(ls -t transfert_detaille_*.log | head -1)

# Ou suivre en temps réel
tail -f $(ls -t transfert_detaille_*.log | head -1)
```

---

## ✅ Commandes rapides (tout en un)

### Se reconnecter et vérifier l'état

```bash
# 1. Se reconnecter (depuis votre terminal local)
ssh votre_compte@ssh.pythonanywhere.com

# 2. Une fois connecté, aller dans le dossier
cd ~/TAL-migration

# 3. Vérifier si le script tourne
python3.10 verifier_blocage.py

# 4. Voir la progression
python3.10 afficher_progression.py --resume
```

---

## 🔄 Si le script s'est arrêté

Si le script s'est arrêté à cause de la déconnexion :

```bash
cd ~/TAL-migration

# Vérifier la progression actuelle
python3.10 afficher_progression.py --resume

# Mettre à jour depuis GitHub (si nécessaire)
git pull origin main

# Relancer le script
python3.10 gestion_transfert.py
```

---

## 📋 Vérification complète

### Script complet de vérification

```bash
cd ~/TAL-migration

echo "=== Vérification de l'état ==="
echo ""

# Vérifier si le script tourne
echo "1. Vérification processus..."
if pgrep -f transferer_factures_documents_v2.py > /dev/null; then
    echo "   ✅ Le script tourne"
    ps aux | grep transferer_factures_documents_v2.py | grep -v grep
else
    echo "   ❌ Le script ne tourne pas"
fi

echo ""
echo "2. Progression actuelle..."
python3.10 afficher_progression.py --resume

echo ""
echo "3. Dernières lignes du log..."
if ls transfert_detaille_*.log 1> /dev/null 2>&1; then
    tail -20 $(ls -t transfert_detaille_*.log | head -1)
else
    echo "   Aucun log trouvé"
fi
```

---

## 💡 Astuces

### Créer un alias pour se reconnecter rapidement

Dans votre fichier `~/.bashrc` ou `~/.bash_profile` sur votre machine locale :

```bash
alias pa='ssh votre_compte@ssh.pythonanywhere.com'
```

Ensuite, tapez simplement `pa` pour vous reconnecter.

### Vérifier depuis l'extérieur (sans se connecter)

Si vous avez configuré un cron job ou un script de monitoring, vous pouvez vérifier via l'API ou les logs.

---

## 📝 Notes importantes

1. **Le script continue de tourner** même après une déconnexion SSH s'il a été lancé en arrière-plan ou via `nohup` ou `screen`/`tmux`
2. **La progression est sauvegardée** après chaque facture, donc même si le script s'arrête, vous ne perdez pas le travail
3. **Au redémarrage**, le script reprendra automatiquement depuis la dernière facture traitée

---

## 🔧 Commandes de secours

### Si vous n'êtes pas sûr de l'état

```bash
# Arrêter tous les scripts (au cas où)
pkill -f transferer_factures_documents_v2.py

# Attendre 2 secondes
sleep 2

# Voir la progression sauvegardée
cd ~/TAL-migration
python3.10 afficher_progression.py --resume

# Relancer proprement
python3.10 gestion_transfert.py
```

