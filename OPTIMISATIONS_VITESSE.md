# ⚡ Guide d'optimisation de la vitesse du script

## Optimisations déjà présentes

✅ **Session HTTP réutilisable** - La connexion HTTP est maintenue entre les factures  
✅ **Cache des modèles PDF** - Les modèles sont mis en cache  
✅ **Cache des dossiers** - Les dossiers clients sont mis en cache  
✅ **Pas de pause systématique** - Pas de délai entre les factures  

## Optimisations supplémentaires possibles

### 1. ⚡ Réduire les logs (gain: 10-20%)

Les logs prennent du temps. Pour réduire :

```python
# Dans transferer_factures_documents_v2.py
# Remplacer les logs détaillés par des logs moins fréquents
if i % 10 == 0:  # Logger seulement toutes les 10 factures
    log_detail(f"Progression: {i}/{total}")
```

### 2. 📦 Traitement par batch (gain: 30-50%)

Vérifier les documents existants par batch au lieu d'une par une :

**Avant** (lent) :
- 100 factures = 100 requêtes de vérification

**Après** (rapide) :
- 100 factures = 2 requêtes de vérification (batch de 50)

### 3. 💾 Sauvegardes moins fréquentes (gain: 5-10%)

Sauvegarder la progression toutes les 10 factures au lieu de chaque fois :

```python
if i % 10 == 0:  # Sauvegarder toutes les 10 factures
    sauvegarder_progression(progression)
```

### 4. 🚫 Réduire les vérifications inutiles (gain: 10-15%)

Ne pas vérifier si le document existe si on vient de le créer.

### 5. 📊 Afficher la progression moins souvent (gain: 5%)

Afficher le résumé toutes les 50 factures au lieu de toutes les 10.

## 🎯 Solutions rapides

### Option 1 : Modifier le script existant

Éditez `transferer_factures_documents_v2.py` et appliquez ces changements :

1. **Ligne 629-643** : Remplacer par une vérification par batch
2. **Ligne 699-826** : Réduire la fréquence des logs
3. **Ligne 816** : Sauvegarder moins souvent

### Option 2 : Utiliser la version optimisée

J'ai créé un script optimisé, mais il nécessite quelques ajustements.

### Option 3 : Configuration rapide

Ajoutez ces paramètres dans `config.py` :

```python
OPTIMISATIONS = {
    'LOG_FREQUENCY': 10,        # Logger toutes les 10 factures
    'SAVE_FREQUENCY': 10,       # Sauvegarder toutes les 10 factures
    'BATCH_SIZE': 50,           # Vérifier 50 factures à la fois
    'DISPLAY_FREQUENCY': 50,    # Afficher progression toutes les 50
}
```

## 📈 Gains estimés

- **Traitement par batch** : +30-50% de vitesse
- **Logs réduits** : +10-20% de vitesse
- **Sauvegardes moins fréquentes** : +5-10% de vitesse
- **Total estimé** : **+50-80% de vitesse** 🚀

## ⚙️ Configuration recommandée

Pour un maximum de vitesse, modifiez dans le script :

1. **Batch size de vérification** : 50 factures à la fois
2. **Fréquence de log** : Toutes les 10 factures
3. **Fréquence de sauvegarde** : Toutes les 10 factures
4. **Affichage progression** : Toutes les 50 factures

## 🚀 Commande pour utiliser la version optimisée

```bash
cd ~/TAL-migration
python3.10 transferer_factures_documents_ACCELERE.py
```

## ⚠️ Notes importantes

- Les optimisations réduisent la visibilité détaillée mais accélèrent le traitement
- La progression est toujours sauvegardée (toutes les 10 factures)
- Les erreurs sont toujours loggées
- Vous pouvez suivre la progression avec `python3.10 afficher_progression.py`

