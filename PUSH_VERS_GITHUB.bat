@echo off
chcp 65001 >nul
cls

echo ======================================================================
echo PUSH VERS GITHUB - Support-Senedoo
echo ======================================================================
echo.
echo Cette commande va pousser vos commits vers GitHub.
echo.
echo IMPORTANT: Vous devez avoir cree un Personal Access Token
echo pour le compte Support-Senedoo.
echo.
echo Si vous n'avez pas encore de token:
echo 1. Allez sur https://github.com/settings/tokens
echo 2. Connectez-vous avec le compte Support-Senedoo
echo 3. Generate new token (classic)
echo 4. Cochez "repo"
echo 5. Copiez le token (commence par ghp_...)
echo.
echo ======================================================================
echo.
pause

echo.
echo Configuration locale pour Support-Senedoo...
git config --local user.name "Support-Senedoo"

echo.
echo Verification de la configuration...
git config --local user.name
git remote -v

echo.
echo ======================================================================
echo PUSH VERS GITHUB
echo ======================================================================
echo.
echo Quand Git vous demande:
echo - Username: Support-Senedoo
echo - Password: Collez votre TOKEN (pas votre mot de passe)
echo.
echo ======================================================================
echo.
pause

git push -u origin main

if errorlevel 1 (
    echo.
    echo ======================================================================
    echo ERREUR LORS DU PUSH
    echo ======================================================================
    echo.
    echo Causes possibles:
    echo 1. Token invalide ou expire
    echo 2. Token sans permission "repo"
    echo 3. Mauvais username (doit etre Support-Senedoo)
    echo.
    echo Solution: Creez un nouveau token sur:
    echo https://github.com/settings/tokens
    echo.
) else (
    echo.
    echo ======================================================================
    echo SUCCES!
    echo ======================================================================
    echo.
    echo Vos fichiers ont ete pushes vers:
    echo https://github.com/Support-Senedoo/TAL-migration
    echo.
)

pause

