# 🔌 Ouvrir un Terminal SSH dans VS Code/Cursor

## 🚀 Méthode 1 : Terminal Intégré (Le Plus Simple)

### 1. Ouvrir le Terminal dans VS Code/Cursor

**Raccourci clavier** :
- `Ctrl + ù` (Ctrl + backtick/backquote)
- Ou `Ctrl + Shift + ù`

**Menu** :
- Terminal → New Terminal
- Ou View → Terminal

### 2. Le Terminal s'ouvre en bas

Vous verrez un terminal dans le panneau du bas de VS Code/Cursor.

### 3. Se Connecter en SSH

Dans ce terminal, tapez :

```bash
ssh senedoo@ssh.pythonanywhere.com
```

(Pourquoi pas le remplacer par votre vrai nom d'utilisateur PythonAnywhere)

### 4. Entrer le Mot de Passe

- Tapez votre mot de passe PythonAnywhere
- Le mot de passe ne s'affichera pas (normal)
- Appuyez sur Entrée

### 5. C'est Connecté !

Une fois connecté, vous verrez le prompt PythonAnywhere :
```
16:50 ~ $ 
```

## 🚀 Méthode 2 : Terminal SSH Dédié

### 1. Menu Terminal

- Cliquez sur le menu déroulant en haut du terminal
- Ou `Terminal` → `New Terminal...`

### 2. Choisir "SSH"

- Dans le menu déroulant, vous pouvez sélectionner "SSH" si disponible
- Ou utilisez directement la commande SSH comme ci-dessus

## 📝 Exemple Complet

1. **Ouvrir Terminal** : `Ctrl + ù`
2. **Se connecter** :
   ```bash
   ssh senedoo@ssh.pythonanywhere.com
   ```
3. **Entrer mot de passe** (ne s'affiche pas)
4. **Aller dans le projet** :
   ```bash
   cd ~/TAL-migration
   ```
5. **Vérifier le script** :
   ```bash
   bash VERIFIER_SCRIPT_BLOQUE.sh
   ```

## ✅ Avantages

- Terminal intégré dans VS Code/Cursor
- Vous pouvez avoir plusieurs terminaux ouverts
- Copier-coller facile
- Historique des commandes

## 💡 Astuce

Une fois connecté, le terminal reste actif. Vous pouvez :
- Ouvrir plusieurs terminaux (`Ctrl + Shift + ù` plusieurs fois)
- Basculer entre eux avec les onglets
- Fermer avec `Ctrl + D` ou en tapant `exit`

