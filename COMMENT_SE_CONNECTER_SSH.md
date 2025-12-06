# 🔐 Comment se Connecter en SSH à PythonAnywhere

## 📋 Méthode 1 : PowerShell (Windows)

1. **Ouvrir PowerShell** :
   - Appuyez sur `Windows + X`
   - Cliquez sur "Windows PowerShell" ou "Terminal"

2. **Se connecter** :
   ```bash
   ssh votre_username@ssh.pythonanywhere.com
   ```

   Remplacez `votre_username` par votre nom d'utilisateur PythonAnywhere.

3. **Entrer le mot de passe** quand demandé

## 📋 Méthode 2 : CMD (Invite de commandes)

1. **Ouvrir CMD** :
   - Appuyez sur `Windows + R`
   - Tapez `cmd` et appuyez sur Entrée

2. **Se connecter** :
   ```bash
   ssh votre_username@ssh.pythonanywhere.com
   ```

## 📋 Méthode 3 : Terminal intégré VS Code / Cursor

1. **Ouvrir le terminal** :
   - Dans VS Code / Cursor : `Ctrl + ù` (ou `Ctrl + Shift + ù`)
   - Ou menu : Terminal → New Terminal

2. **Se connecter** :
   ```bash
   ssh votre_username@ssh.pythonanywhere.com
   ```

## 📋 Méthode 4 : Client SSH Graphique (PuTTY)

1. **Télécharger PuTTY** : https://www.putty.org/

2. **Configurer** :
   - **Host Name** : `ssh.pythonanywhere.com`
   - **Port** : `22`
   - **Connection type** : SSH

3. **Cliquer sur "Open"**

## ✅ Après la Connexion

Une fois connecté, vous êtes dans votre home directory sur PythonAnywhere.

Pour aller dans le projet :
```bash
cd ~/TAL-migration
```

## 🔑 Authentification

- **Première connexion** : On vous demandera de confirmer (tapez `yes`)
- **Mot de passe** : Entrez votre mot de passe PythonAnywhere

## 📝 Notes

- Le mot de passe ne s'affiche pas pendant la saisie (c'est normal)
- Si vous avez des problèmes de connexion, vérifiez que SSH est activé sur votre compte PythonAnywhere
- Sur le dashboard PythonAnywhere, allez dans "Account" → "SSH settings" pour vérifier

## 🆘 Problèmes Courants

### "Permission denied"
- Vérifiez votre nom d'utilisateur et mot de passe
- Vérifiez que SSH est activé sur PythonAnywhere

### "Connection refused"
- Vérifiez votre connexion Internet
- Vérifiez que SSH est activé sur votre compte PythonAnywhere

### "Host key verification failed"
- Supprimez la clé : `ssh-keygen -R ssh.pythonanywhere.com`

