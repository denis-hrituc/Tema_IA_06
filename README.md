# Tema_IA_06
## Tema A – Evitare cu revenire  
**Fișier:** `tema_a_recuperare.py`

### Descriere comportament:

- **FORWARD**  
  Robotul se deplasează înainte până când detectează un obstacol în față la o distanță mai mică decât pragul `STOP_DISTANCE`.

- **BACKWARD**  
  Robotul se retrage pentru o perioadă de `BACKWARD_TIME` secunde.

- **TURNING**  
  Robotul se rotește aleator spre stânga sau dreapta, aproximativ 90°, timp de `TURN_TIME`.

- După finalizarea rotației (**TURNING**), robotul revine la starea **FORWARD**.
