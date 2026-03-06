#!/usr/bin/env python

import os

#--- get clean base path
BasePath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))

#--- get full file paths
ActivateFile = os.path.join(BasePath,'.venv','bin','activate')

ScriptFile = os.path.join(BasePath,"SoundBox","SoundBox-RFID.py")
#ScriptFile = os.path.join(BasePath,"SoundBox","SoundBox-MetalBarCode.py")

#--- execute in terminal
print(f"activate .venv: source {ActivateFile}")
print(f"and autostart: {ScriptFile}")
os.system(f'bash -c "source {ActivateFile} && python {ScriptFile}"')
