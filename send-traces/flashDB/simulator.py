import random
import time
import db as db


while(True):
    i = random.randint(0,100)
    if i < 20:
        db.read("test")
    elif i > 20 & i < 35:
        r = random.randint(0, 100)
        db.create(f"test{r}", "1" * random.randint(1, 1000))
    elif i > 35 & i < 45:
        r = random.randint(0, 100)
        db.update(f"test{r}", "1" * random.randint(1, 1000))
    else:
        db.delete("test{r}")

    time.sleep(0.1)
