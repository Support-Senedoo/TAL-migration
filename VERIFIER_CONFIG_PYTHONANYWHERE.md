# ✅ Vérifier config.py sur PythonAnywhere

## 🔍 Vérification rapide

Sur PythonAnywhere, exécutez :

```bash
cat ~/TAL-migration/config.py
```

## ✅ Configuration correcte

Le fichier `config.py` doit contenir :

```python
ODOO_CONFIG = {
    'URL': 'https://tal-senegal.odoo.com/',
    'DB': 'tal-senegal',
    'USER': 'support@senedoo.com',
    'PASS': 'senedoo@2025'
}
```

## ✏️ Si vous devez modifier

Si les valeurs sont différentes ou incorrectes :

```bash
nano ~/TAL-migration/config.py
```

**Modifiez uniquement les valeurs** :
- `URL` : doit être `'https://tal-senegal.odoo.com/'`
- `DB` : doit être `'tal-senegal'`
- `USER` : doit être `'support@senedoo.com'`
- `PASS` : doit être `'senedoo@2025'`

**Pour sauvegarder dans nano** :
- `Ctrl+X` puis `Y` puis `Enter`

## ✅ Test après modification

```bash
python3.10 ~/TAL-migration/connexion_odoo.py
```

Si vous voyez `✅ Connexion réussie!`, c'est bon ! ✅

## 📝 Note

Le script d'installation crée automatiquement un `config.py` avec les bonnes valeurs. Si le fichier existe déjà avec les bonnes valeurs, **vous n'avez rien à modifier**.

