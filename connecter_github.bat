@echo off
chcp 65001 >nul
cls

echo ======================================================================
echo CONNEXION DU DEPOT LOCAL A GITHUB
echo ======================================================================
echo.
echo Cette commande va connecter votre depot local a GitHub.
echo.
echo Vous devez avoir cree le depot sur GitHub au prealable.
echo.
echo ======================================================================
echo.
set /p github_url="Entrez l'URL de votre depot GitHub (ex: https://github.com/USERNAME/TAL-migration.git): "

if "%github_url%"=="" (
    echo.
    echo Erreur: URL vide
    pause
    exit /b 1
)

echo.
echo Ajout du remote origin...
git remote add origin %github_url%

if errorlevel 1 (
    echo.
    echo Le remote existe deja. Mise a jour...
    git remote set-url origin %github_url%
)

echo.
echo Passage en branche main...
git branch -M main

echo.
echo ======================================================================
echo CONFIGURATION TERMINEE
echo ======================================================================
echo.
echo Prochaine etape: Pusher vers GitHub
echo.
echo Executez: git push -u origin main
echo.
echo ======================================================================
pause

