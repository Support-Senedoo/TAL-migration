# ⚡ Comment accélérer le script - Modifications simples

## 🚀 Modifications à faire dans `transferer_factures_documents_v2.py`

### 1. Vérification par batch (gain: 30-50%)

**Remplacez les lignes 629-643** par ceci :

```python
# Vérifier les documents existants PAR BATCH (optimisation)
print(f"🔍 Vérification des documents existants (batch de 50)...")
factures_ids_a_traiter = [f['id'] for f in factures_a_traiter]
documents_existants = []
BATCH_SIZE = 50  # Vérifier 50 factures à la fois

# Traiter par batch
for i in range(0, len(factures_ids_a_traiter), BATCH_SIZE):
    batch = factures_ids_a_traiter[i:i + BATCH_SIZE]
    if batch:  # Éviter de passer une liste vide
        try:
            batch_docs = models.execute_kw(
                db, uid, password,
                'documents.document',
                'search_read',
                [[
                    ['res_model', '=', 'account.move'],
                    ['res_id', 'in', batch]
                ]],
                {'fields': ['res_id']}
            )
            if batch_docs:
                documents_existants.extend([doc['res_id'] for doc in batch_docs if doc.get('res_id')])
        except Exception as e:
            log_detail(f"⚠️  Erreur batch: {str(e)}")
    
    if (i // BATCH_SIZE + 1) % 20 == 0:
        print(f"   ✅ Vérifié {i + len(batch)}/{len(factures_ids_a_traiter)} factures...")
```

### 2. Réduire les logs (gain: 10-20%)

**Dans la boucle de traitement (ligne 691), remplacez** :

```python
# Logger seulement toutes les 10 factures
if i % 10 == 0 or i == 1:
    log_detail(f"[{i}/{len(factures_a_traiter_final)}] Traitement facture {facture_numero}...")
```

Au lieu de logger chaque facture.

### 3. Sauvegarder moins souvent (gain: 5-10%)

**Ligne 816, remplacez** :

```python
# Sauvegarder toutes les 10 factures au lieu de chaque fois
if i % 10 == 0:
    sauvegarder_progression(progression)
```

Et gardez la sauvegarde finale après la boucle.

### 4. Affichage progression moins fréquent (gain: 5%)

**Ligne 829, changez** :

```python
# Afficher toutes les 50 factures au lieu de 50
if i % 50 == 0:
```

## 📋 Résumé des modifications

1. ✅ Vérification par batch (50 factures à la fois)
2. ✅ Logs toutes les 10 factures
3. ✅ Sauvegarde toutes les 10 factures  
4. ✅ Affichage progression toutes les 50 factures

## 🎯 Gain estimé total : +50-80% de vitesse ! 🚀

## 💡 Solution plus simple

Si vous voulez une solution **immédiate sans modifier le code**, vous pouvez :

1. **Réduire les logs** : Dans le script, commentez les lignes de log détaillé
2. **Augmenter le batch** : Modifiez le BATCH_SIZE dans config.py (mais ce n'est pas encore utilisé)
3. **Traiter moins de factures par test** : Utilisez `--test` pour voir la vitesse

## 🔧 Script d'optimisation automatique

Je peux créer un script qui applique automatiquement ces modifications. Souhaitez-vous que je le fasse ?

