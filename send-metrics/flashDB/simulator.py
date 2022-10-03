import random
import time
import db as db


while(True):
    i = random.randint(0,100)
    if i < 35:
        db.read("test")
    elif i > 35 & i < 50:
        r = random.randint(0, 100)
        db.create(f"test{r}", "1" * random.randint(1, 1000))
    elif i > 50 & i < 75:
        r = random.randint(0, 100)
        db.update(f"test{r}", "1" * random.randint(1, 1000))
    else:
        db.delete("test{r}")

    time.sleep(0.1)
