# Tema_IA_06
Tema A – Evitare cu revenire
Fișier: tema_a_recuperare.py

Descriere comportament:

FORWARD: robotul înaintează continuu până când senzorul detectează un obstacol în față la o distanță mai mică decât pragul STOP_DISTANCE.
BACKWARD: robotul se retrage pentru o durată de BACKWARD_TIME secunde.
TURNING: robotul execută o rotație aleatoare spre stânga sau dreapta, aproximativ 90°, timp de TURN_TIME.
După finalizarea rotației (TURNING), robotul reia deplasarea înainte (FORWARD)
