@echo off
SET files=Arc.py Bonus.py GUI.py InputManager.py MusicManager.py Particles.py Snake.py
SET output=flake8.txt
flake8 %files%>%output%