@echo off
SET files=Core/Arc.py ^
          Core/Bonus.py ^
          Core/GUI.py ^
          Core/InputManager.py ^
          Core/MusicManager.py ^
          Core/Particles.py ^
          Core/Snake.py ^
          Core/RandomBonus.py ^
          Core/ComboColorBox.py
SET output=flake8.txt
flake8 %files%>%output%