@echo off
chcp 65001 >nul
cls

echo ======================================================================
echo EFFACER LES CREDENTIALS GIT EN CACHE
echo ======================================================================
echo.
echo Cette commande va effacer les credentials Git en cache
echo pour permettre l'utilisation du token Support-Senedoo.
echo.
echo ======================================================================
echo.
pause

echo.
echo Effacement des credentials Windows pour GitHub...
cmdkey /delete:git:https://github.com

echo.
echo Effacement des credentials Git Credential Manager...
git credential-manager-core erase <<EOF
protocol=https
host=github.com
EOF

echo.
echo ======================================================================
echo CREDENTIALS EFFACES
echo ======================================================================
echo.
echo Vous pouvez maintenant executer:
echo git push -u origin main
echo.
echo Quand Git demande:
echo - Username: Support-Senedoo
echo - Password: Collez votre TOKEN
echo.
echo ======================================================================
pause

