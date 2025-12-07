# 🔌 Reconnexion rapide après déconnexion

## 🚀 Commandes rapides (copier-coller)

### 1. Se reconnecter à PythonAnywhere

```bash
ssh senedoo@ssh.pythonanywhere.com
```

### 2. Vérifier si le script tourne toujours

```bash
cd ~/TAL-migration
python3.10 verifier_blocage.py
```

**OU manuellement :**

```bash
# Vérifier les processus
ps aux | grep transferer_factures_documents_v2.py

# Voir la progression
python3.10 afficher_progression.py --resume
```

### 3. Voir la progression en temps réel

```bash
python3.10 afficher_progression.py --watch
```

---

## 📋 Commandes complètes

### Option 1 : Tout en une fois

```bash
ssh senedoo@ssh.pythonanywhere.com
cd ~/TAL-migration && python3.10 verifier_blocage.py
```

### Option 2 : Étape par étape

```bash
# 1. Se reconnecter
ssh senedoo@ssh.pythonanywhere.com

# 2. Aller dans le dossier
cd ~/TAL-migration

# 3. Vérifier l'état
python3.10 verifier_blocage.py

# 4. Si le script tourne, voir la progression
python3.10 afficher_progression.py --watch

# 5. Si le script ne tourne pas, le relancer
python3.10 gestion_transfert.py
```

---

## 🔍 Vérifications rapides

### Vérifier si le script tourne

```bash
pgrep -f transferer_factures_documents_v2.py
```

- **Si une ligne s'affiche** : Le script tourne ✅
- **Si rien** : Le script s'est arrêté ❌

### Voir la progression sauvegardée

```bash
cat progression_transfert.json | python3 -m json.tool | head -20
```

### Voir les dernières lignes du log

```bash
tail -30 $(ls -t transfert_detaille_*.log | head -1)
```

---

## 🔄 Si le script s'est arrêté

```bash
cd ~/TAL-migration

# Vérifier la progression
python3.10 afficher_progression.py --resume

# Mettre à jour (si nécessaire)
git pull origin main

# Relancer
python3.10 gestion_transfert.py
```

---

## 💡 Astuce : Créer un alias

Dans votre `~/.bashrc` ou `~/.bash_profile` local :

```bash
alias pa='ssh senedoo@ssh.pythonanywhere.com'
alias patal='ssh senedoo@ssh.pythonanywhere.com "cd ~/TAL-migration && bash"'
```

Ensuite, tapez simplement `pa` pour vous reconnecter !

---

## 📱 Via le navigateur (alternative)

1. Allez sur https://www.pythonanywhere.com
2. Connectez-vous
3. Cliquez sur **"Consoles"** dans le menu
4. Cliquez sur **"Bash"** pour ouvrir une console
5. Puis :

```bash
cd ~/TAL-migration
python3.10 verifier_blocage.py
```

