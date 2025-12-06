# ❓ Réponse : Dois-je modifier config.py ?

## ✅ Réponse rapide

**Probablement NON** si le script vient de créer le fichier.

Le script `INSTALL_PYTHONANYWHERE.sh` crée automatiquement un `config.py` avec les **bonnes valeurs** :
- URL : `https://tal-senegal.odoo.com/`
- DB : `tal-senegal`
- USER : `support@senedoo.com`
- PASS : `senedoo@2025`

## 🔍 Vérification rapide

Sur PythonAnywhere, vérifiez le contenu :

```bash
cat ~/TAL-migration/config.py | grep -A 5 "ODOO_CONFIG"
```

Vous devriez voir :
```python
ODOO_CONFIG = {
    'URL': 'https://tal-senegal.odoo.com/',
    'DB': 'tal-senegal',
    'USER': 'support@senedoo.com',
    'PASS': 'senedoo@2025'
}
```

## ✅ Si les valeurs sont correctes

**Vous n'avez rien à modifier !** Passez directement au test :

```bash
python3.10 ~/TAL-migration/connexion_odoo.py
```

## ✏️ Si vous devez modifier

Si les valeurs sont différentes :

```bash
nano ~/TAL-migration/config.py
```

**Sauvegarder** : `Ctrl+X` puis `Y` puis `Enter`

## 🎯 Prochaine étape

Après avoir vérifié (ou modifié) `config.py`, testez la connexion :

```bash
python3.10 ~/TAL-migration/connexion_odoo.py
```

Si ça fonctionne, vous verrez : `✅ Connexion réussie!`

Ensuite, vous pouvez lancer le transfert :
```bash
python3.10 ~/TAL-migration/transferer_factures_documents_v2.py
```

