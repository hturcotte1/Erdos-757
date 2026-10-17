# regression: connected (14,12,6) maxdeg3 must give the 2 classes; (17,13,7) maxdeg3 the 8 classes; (15,11,6) maxdeg3 the 19 kept classes
import engine,sys
for key in [(14,12,6,3),(15,11,6,3),(17,13,7,3)]:
    r=engine.cell(*key); print(key,len(r))
