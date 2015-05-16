@echo off
SET files=Core/Arc.py ^
          Core/Bonus.py ^
          Core/GUI.py ^
          Core/InputManager.py ^
          Core/MusicManager.py ^
          Core/Particles.py ^
          Core/Snake.py ^
          Core/RandomBonus.py ^
          Core/ComboColorBox.py ^
          Core/Profile.py ^
          Core/BonusManager.py
SET output=flake8.txt
REM writes result of PEP8 analysis in output file
flake8 %files%>%output%