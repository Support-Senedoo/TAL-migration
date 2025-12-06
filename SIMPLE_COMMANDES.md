# 🎯 Commandes Simples - Une seule à retenir

## 🔄 Mettre à jour le projet

```bash
cd ~/TAL-migration && bash UPDATE.sh
```

C'est tout ! Le script fait tout automatiquement.

## 🚀 Lancer le transfert

```bash
cd ~/TAL-migration && nohup python3.10 transferer_factures_documents_v2.py > transfert.log 2>&1 &
```

## 📊 Voir la progression

```bash
python3.10 ~/TAL-migration/gestion_progression.py afficher
```

## 📄 Voir les logs

```bash
tail -f ~/TAL-migration/transfert.log
```
**Arrêter** : `Ctrl+C`

---

**C'est tout ce dont vous avez besoin !** 🎉

