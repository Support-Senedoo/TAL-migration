#!/bin/bash
cd ~/TAL-migration && [ -f config.py ] && cp config.py config.py.backup && rm config.py || true && git pull origin main && [ -f config.py.backup ] && mv config.py.backup config.py && pip3.10 install --user -r requirements.txt && echo "✅ Terminé!"

