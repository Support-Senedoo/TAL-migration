@echo off
chcp 65001 >nul
cls

echo ======================================================================
echo GESTION AUTOMATIQUE DU TRANSFERT DES FACTURES
echo ======================================================================
echo.
echo Ce script va :
echo   - Verifier l'etat du transfert
echo   - Tester la connexion Odoo
echo   - Lancer/relancer le transfert automatiquement
echo.
echo ======================================================================
echo.

cd /d "%~dp0"
python gestion_transfert.py

pause



