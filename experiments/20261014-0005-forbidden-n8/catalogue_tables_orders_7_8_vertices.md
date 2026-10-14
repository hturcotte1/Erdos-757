### H2: star of three edges (common vertex) (7 vertices): orders

Edges: {a,b,c}, {a,d,e}, {a,f,g}.

**2.1** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=a`
- order `b d f a c e g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (f,a,g)
- order `b d f a c g e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (f,a,g)
- order `b d f a g c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- (5 orders in total; first realizable shown, none realizable: first 3 orders shown)

**2.2** `mid(b,c)=a; mid(d,e)=a; mid(a,g)=f`
- order `b d a c e f g` : O: no increasing point; minimal order-infeasible sub-pattern (a,e,f), (c,e,g)
- order `b d a e c f g` : D: forces x_e-x_a = x_g-x_f
- order `b d a c f e g` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- (12 orders in total; first realizable shown, none realizable: first 3 orders shown)

**2.3** `mid(b,c)=a; mid(a,e)=d; mid(a,g)=f`
- order `b a c d e f g` : R  realization b=0, a=1, c=2, d=6, e=11, f=14, g=27
- (21 orders in total; first realizable shown)

**2.4** `mid(a,c)=b; mid(a,e)=d; mid(a,g)=f`
- order `a b c d e f g` : R  realization a=0, b=1, c=2, d=6, e=12, f=15, g=30
- (18 orders in total; first realizable shown)

### H3: path of three edges (7 vertices): orders

Edges: {a,b,c}, {a,d,e}, {b,f,g}.

**3.1** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=b`
- order `f b g d a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `f b g d a e c` : D: forces x_d-x_b = x_c-x_e
- order `f b d g a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- (26 orders in total; first realizable shown, none realizable: first 3 orders shown)

**3.2** `mid(b,c)=a; mid(d,e)=a; mid(b,g)=f`
- order `b f g d a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `b f g d a e c` : D: forces x_d-x_b = x_c-x_e
- order `d c a e b f g` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,f), (e,b,g)
- (58 orders in total; first realizable shown, none realizable: first 3 orders shown)

**3.3** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=b`
- order `f b g a c d e` : R  realization f=0, b=1, g=2, a=5, c=9, d=15, e=25
- (37 orders in total; first realizable shown)

**3.4** `mid(b,c)=a; mid(a,e)=d; mid(b,g)=f`
- order `b a c f g d e` : R  realization b=0, a=1, c=2, f=6, g=12, d=15, e=29
- (89 orders in total; first realizable shown)

**3.5** `mid(a,b)=c; mid(d,e)=a; mid(f,g)=b`
- order `d a e c f b g` : R  realization d=0, a=3, e=6, c=11, f=18, b=19, g=20
- (11 orders in total; first realizable shown)

**3.6** `mid(a,b)=c; mid(d,e)=a; mid(b,g)=f`
- order `b f g c d a e` : R  realization b=0, f=3, g=6, c=10, d=19, a=20, e=21
- (45 orders in total; first realizable shown)

**3.7** `mid(a,b)=c; mid(a,e)=d; mid(b,g)=f`
- order `a c b d e f g` : R  realization a=0, c=3, b=6, d=7, e=14, f=16, g=26
- (55 orders in total; first realizable shown)

### H5: triangle + pendant edge at a corner (8 vertices): orders

Edges: {a,b,c}, {a,d,e}, {a,f,g}, {b,d,h}.

**5.1** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=a; mid(d,h)=b`
- order `f c e a g h b d` : O: no increasing point; minimal order-infeasible sub-pattern (c,g,b), (a,g,d)
- order `c f e a g h b d` : O: no increasing point; minimal order-infeasible sub-pattern (c,g,h), (a,g,b)
- order `f e c a g h b d` : O: no increasing point; minimal order-infeasible sub-pattern (e,g,h), (a,g,d)
- (192 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.2** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=a; mid(b,d)=h`
- order `f c e a g b h d` : O: no increasing point; minimal order-infeasible sub-pattern (e,g,h), (a,g,d)
- order `c f e a g b h d` : O: no increasing point; minimal order-infeasible sub-pattern (c,g,b), (a,g,h)
- order `f e c a g b h d` : O: no increasing point; minimal order-infeasible sub-pattern (c,g,b), (a,g,d)
- (96 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.3** `mid(b,c)=a; mid(d,e)=a; mid(a,g)=f; mid(d,h)=b`
- order `d b h a e c f g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- order `d b h a e f c g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- order `d b h a e f g c` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- (256 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.4** `mid(b,c)=a; mid(d,e)=a; mid(a,g)=f; mid(b,d)=h`
- order `b h d a c e f g` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `b h d a c f e g` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `b h d a c f g e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- (128 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.5** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=a; mid(d,h)=b`
- order `f c a g d e b h` : O: no increasing point; minimal order-infeasible sub-pattern (c,e,b), (d,e,h)
- order `c f a g d e b h` : D: forces x_d-x_f = x_h-x_b
- order `f c h a g b d e` : O: no increasing point; minimal order-infeasible sub-pattern (h,g,d), (a,g,e)
- (100 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.6** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=a; mid(b,h)=d`
- order `b f a c d h g e` : O: no increasing point; minimal order-infeasible sub-pattern (b,d,h), (a,d,e)
- order `b f a c d h e g` : O: no increasing point; minimal order-infeasible sub-pattern (b,d,h), (a,d,e)
- order `b f a c d g h e` : O: no increasing point; minimal order-infeasible sub-pattern (b,d,h), (a,d,e)
- (168 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.7** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=a; mid(b,d)=h`
- order `f c a g d e h b` : O: no increasing point; minimal order-infeasible sub-pattern (f,e,h), (d,e,b)
- order `c f a g d e h b` : D: forces x_d-x_c = x_b-x_h
- order `b h f a d c g e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (f,a,g)
- (116 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.8** `mid(b,c)=a; mid(a,e)=d; mid(a,g)=f; mid(d,h)=b`
- order `c a d b e f h g` : R  realization c=0, a=15, d=23, b=30, e=31, f=35, h=37, g=55
- (152 orders in total; first realizable shown)

**5.9** `mid(b,c)=a; mid(a,e)=d; mid(a,g)=f; mid(b,h)=d`
- order `b a c d h e f g` : O: no increasing point; minimal order-infeasible sub-pattern (b,d,h), (a,d,e)
- order `b a c d h f e g` : O: no increasing point; minimal order-infeasible sub-pattern (b,d,h), (a,d,e)
- order `b a c d h f g e` : O: no increasing point; minimal order-infeasible sub-pattern (a,d,e), (a,f,g)
- (280 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.10** `mid(b,c)=a; mid(a,e)=d; mid(a,g)=f; mid(b,d)=h`
- order `b a c h d e f g` : R  realization b=0, a=1, c=2, h=5, d=10, e=19, f=25, g=49
- (192 orders in total; first realizable shown)

**5.11** `mid(b,c)=a; mid(a,d)=e; mid(f,g)=a; mid(d,h)=b`
- order `f c a g e h b d` : O: no increasing point; minimal order-infeasible sub-pattern (c,h,b), (e,h,d)
- order `c f a g e h b d` : D: forces x_e-x_f = x_d-x_b
- order `f c a e g h b d` : O: no increasing point; minimal order-infeasible sub-pattern (c,h,b), (e,h,d)
- (124 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.12** `mid(b,c)=a; mid(a,d)=e; mid(f,g)=a; mid(b,h)=d`
- order `f c a g e h d b` : O: no increasing point; minimal order-infeasible sub-pattern (f,h,d), (e,h,b)
- order `f c a e g h d b` : O: no increasing point; minimal order-infeasible sub-pattern (f,h,d), (e,h,b)
- order `c f a g e h d b` : D: forces x_e-x_c = x_b-x_d
- (104 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.13** `mid(b,c)=a; mid(a,d)=e; mid(f,g)=a; mid(b,d)=h`
- order `f c a g e b h d` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,h), (e,b,d)
- order `c f a g e b h d` : D: forces x_e-x_a = x_d-x_h
- order `f c a e g b h d` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,h), (e,b,d)
- (156 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.14** `mid(b,c)=a; mid(a,d)=e; mid(a,g)=f; mid(d,h)=b`
- order `g f c a e h b d` : R  realization g=0, f=3, c=6, a=7, e=14, h=25, b=27, d=40
- (184 orders in total; first realizable shown)

**5.15** `mid(b,c)=a; mid(a,d)=e; mid(a,g)=f; mid(b,h)=d`
- order `b a c e d h f g` : R  realization b=0, a=3, c=6, e=7, d=11, h=22, f=24, g=45
- (176 orders in total; first realizable shown)

**5.16** `mid(b,c)=a; mid(a,d)=e; mid(a,g)=f; mid(b,d)=h`
- order `g f c a e b h d` : R  realization g=0, f=3, c=6, a=7, e=14, b=22, h=24, d=34
- (264 orders in total; first realizable shown)

**5.17** `mid(a,c)=b; mid(a,e)=d; mid(f,g)=a; mid(d,h)=b`
- order `f a g d e b c h` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (d,b,h)
- order `f a g d e b h c` : D: forces x_d-x_a = x_c-x_h
- order `f a g d b e c h` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (d,b,h)
- (120 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.18** `mid(a,c)=b; mid(a,e)=d; mid(f,g)=a; mid(b,d)=h`
- order `f a g b c h d e` : R  realization f=0, a=1, g=2, b=5, c=9, h=15, d=25, e=49
- (36 orders in total; first realizable shown)

**5.19** `mid(a,c)=b; mid(a,e)=d; mid(a,g)=f; mid(d,h)=b`
- order `a d e b c f g h` : O: no increasing point; minimal order-infeasible sub-pattern (a,f,g), (d,b,h)
- order `a d e f g b c h` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (d,b,h)
- order `a f g d e b c h` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (d,b,h)
- (328 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.20** `mid(a,c)=b; mid(a,e)=d; mid(a,g)=f; mid(b,d)=h`
- order `a b c f g h d e` : R  realization a=0, b=3, c=6, f=7, g=14, h=16, d=29, e=58
- (104 orders in total; first realizable shown)

**5.21** `mid(a,c)=b; mid(a,d)=e; mid(f,g)=a; mid(d,h)=b`
- order `f a g e d b c h` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (d,b,h)
- order `f a g e d b h c` : D: forces x_d-x_a = x_c-x_h
- order `f a g e h b d c` : D: forces x_h-x_a = x_c-x_d
- (128 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.22** `mid(a,c)=b; mid(a,d)=e; mid(f,g)=a; mid(b,h)=d`
- order `f a g b c e d h` : R  realization f=0, a=1, g=2, b=6, c=11, e=14, d=27, h=48
- (76 orders in total; first realizable shown)

**5.23** `mid(a,c)=b; mid(a,d)=e; mid(f,g)=a; mid(b,d)=h`
- order `f a g b c e h d` : R  realization f=0, a=3, g=6, b=7, c=11, e=21, h=23, d=39
- (108 orders in total; first realizable shown)

**5.24** `mid(a,c)=b; mid(a,d)=e; mid(a,g)=f; mid(d,h)=b`
- order `a e d b c f g h` : O: no increasing point; minimal order-infeasible sub-pattern (a,f,g), (d,b,h)
- order `a e d f g b c h` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (d,b,h)
- order `a f g e d b c h` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (d,b,h)
- (320 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.25** `mid(a,c)=b; mid(a,d)=e; mid(a,g)=f; mid(b,h)=d`
- order `a b c f g e d h` : R  realization a=0, b=2, c=4, f=9, g=18, e=19, d=38, h=74
- (232 orders in total; first realizable shown)

**5.26** `mid(a,c)=b; mid(a,d)=e; mid(a,g)=f; mid(b,d)=h`
- order `a b c f g e h d` : R  realization a=0, b=2, c=4, f=11, g=22, e=27, h=28, d=54
- (312 orders in total; first realizable shown)

**5.27** `mid(a,b)=c; mid(a,d)=e; mid(f,g)=a; mid(d,h)=b`
- order `f a g c e h b d` : R  realization f=0, a=4, g=8, c=15, e=17, h=27, b=30, d=33
- (108 orders in total; first realizable shown)

**5.28** `mid(a,b)=c; mid(a,d)=e; mid(f,g)=a; mid(b,d)=h`
- order `f a g c e b h d` : D: forces x_a-x_f = x_e-x_c
- order `f a c g e b h d` : D: forces x_a-x_f = x_b-x_g
- order `f a g e c b h d` : O: no increasing point; minimal order-infeasible sub-pattern (f,c,h), (g,e,h)
- (48 orders in total; first realizable shown, none realizable: first 3 orders shown)

**5.29** `mid(a,b)=c; mid(a,d)=e; mid(a,g)=f; mid(d,h)=b`
- order `a e d f g c b h` : R  realization a=0, e=3, d=6, f=7, g=14, c=16, b=32, h=58
- (312 orders in total; first realizable shown)

**5.30** `mid(a,b)=c; mid(a,d)=e; mid(a,g)=f; mid(b,d)=h`
- order `a c b f g e h d` : D: forces x_c-x_a = x_h-x_e
- order `a f g c b e h d` : D: forces x_c-x_a = x_h-x_e
- order `a c b f g h e d` : O: no increasing point; minimal order-infeasible sub-pattern (a,e,d), (b,h,d)
- (120 orders in total; first realizable shown, none realizable: first 3 orders shown)

### H6: star of three edges + transversal edge (three triangles) (7 vertices): orders

Edges: {a,b,c}, {a,d,e}, {a,f,g}, {b,d,f}.

**6.1** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=a; mid(d,f)=b`
- order `d b f a e c g` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (f,a,g)
- order `d b f a e g c` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (f,a,g)
- order `d b f a c e g` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (f,a,g)
- (24 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.2** `mid(b,c)=a; mid(d,e)=a; mid(a,g)=f; mid(d,f)=b`
- order `d b a f e c g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- order `d b a f e g c` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- order `d b a f c e g` : O: no increasing point; minimal order-infeasible sub-pattern (d,b,f), (d,a,e), (b,a,c), (a,f,g)
- (28 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.3** `mid(b,c)=a; mid(d,e)=a; mid(a,g)=f; mid(b,d)=f`
- order `c e a b f g d` : O: no increasing point; minimal order-infeasible sub-pattern (c,f,g), (b,f,d)
- order `b e a c f d g` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,d), (a,f,g)
- order `e c a b f g d` : O: no increasing point; minimal order-infeasible sub-pattern (e,a,b), (c,a,f)
- (20 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.4** `mid(b,c)=a; mid(d,e)=a; mid(a,f)=g; mid(d,f)=b`
- order `e c a g d b f` : O: no increasing point; minimal order-infeasible sub-pattern (c,d,b), (a,d,f)
- order `c e a g d b f` : D: forces x_e-x_c = x_f-x_b
- order `c e a g f b d` : O: no increasing point; minimal order-infeasible sub-pattern (c,f,b), (e,f,d)
- (36 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.5** `mid(b,c)=a; mid(d,e)=a; mid(a,f)=g; mid(b,d)=f`
- order `c e a g b f d` : O: no increasing point; minimal order-infeasible sub-pattern (c,b,f), (a,b,d)
- order `e c a g b f d` : D: forces x_a-x_e = x_d-x_f
- order `c e a b g f d` : O: no increasing point; minimal order-infeasible sub-pattern (c,g,f), (b,g,d)
- (12 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.6** `mid(b,c)=a; mid(a,e)=d; mid(a,g)=f; mid(d,f)=b`
- order `c a d b e f g` : R  realization c=0, a=7, d=11, b=14, e=15, f=17, g=27
- (7 orders in total; first realizable shown)

**6.7** `mid(b,c)=a; mid(a,e)=d; mid(a,g)=f; mid(b,f)=d`
- order `b a c d f e g` : O: no increasing point; minimal order-infeasible sub-pattern (b,d,f), (a,d,e)
- order `b a c d f g e` : O: no increasing point; minimal order-infeasible sub-pattern (a,d,e), (a,f,g)
- order `b a c d e f g` : D: forces x_a-x_b = x_f-x_e
- (32 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.8** `mid(b,c)=a; mid(a,e)=d; mid(a,f)=g; mid(d,f)=b`
- order `f g b a d c e` : R  realization f=0, g=7, b=9, a=14, d=18, c=19, e=22
- (21 orders in total; first realizable shown)

**6.9** `mid(b,c)=a; mid(a,e)=d; mid(a,f)=g; mid(b,f)=d`
- order `b a c d g f e` : O: no increasing point; minimal order-infeasible sub-pattern (a,d,e), (a,g,f)
- order `b a c d e g f` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (b,d,f), (a,d,e), (a,g,f)
- order `b a c d g e f` : E: forces unlisted AP (c,g,e)
- (40 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.10** `mid(b,c)=a; mid(a,e)=d; mid(a,f)=g; mid(b,d)=f`
- order `b a c g f d e` : R  realization b=0, a=1, c=2, g=5, f=9, d=18, e=35
- (17 orders in total; first realizable shown)

**6.11** `mid(b,c)=a; mid(a,d)=e; mid(a,f)=g; mid(d,f)=b`
- order `c a e g d b f` : D: forces x_a-x_c = x_d-x_g
- order `c a g e d b f` : O: no increasing point; minimal order-infeasible sub-pattern (c,d,b), (g,e,b)
- order `c a e d g b f` : D: forces x_a-x_c = x_g-x_e
- (10 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.12** `mid(b,c)=a; mid(a,d)=e; mid(a,f)=g; mid(b,f)=d`
- order `c a e g b d f` : R  realization c=0, a=4, e=8, g=9, b=11, d=18, f=28
- (29 orders in total; first realizable shown)

**6.13** `mid(a,c)=b; mid(a,e)=d; mid(a,g)=f; mid(d,f)=b`
- order `a d e b c f g` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (d,b,f)
- order `a d e b f c g` : E: forces unlisted AP (e,c,g)
- order `a d e b f g c` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (a,f,g)
- (18 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.14** `mid(a,c)=b; mid(a,e)=d; mid(a,f)=g; mid(d,f)=b`
- order `a d e b c g f` : O: no increasing point; minimal order-infeasible sub-pattern (a,g,f), (d,b,f)
- order `a g f b c d e` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (f,b,d)
- order `f g a b d c e` : O: no increasing point; minimal order-infeasible sub-pattern (f,b,d), (a,b,c)
- (44 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.15** `mid(a,c)=b; mid(a,e)=d; mid(a,f)=g; mid(b,d)=f`
- order `a b c g f d e` : R  realization a=0, b=2, c=4, g=5, f=10, d=18, e=36
- (10 orders in total; first realizable shown)

**6.16** `mid(a,c)=b; mid(a,d)=e; mid(a,f)=g; mid(d,f)=b`
- order `a e d b c g f` : O: no increasing point; minimal order-infeasible sub-pattern (a,g,f), (d,b,f)
- order `a e d b g c f` : O: no increasing point; minimal order-infeasible sub-pattern (a,g,f), (d,b,f)
- order `a e d g b f c` : D: forces x_e-x_a = x_b-x_g
- (14 orders in total; first realizable shown, none realizable: first 3 orders shown)

**6.17** `mid(a,c)=b; mid(a,d)=e; mid(a,f)=g; mid(b,f)=d`
- order `a g f e d b c` : R  realization a=0, g=2, f=4, e=5, d=10, b=16, c=32
- (40 orders in total; first realizable shown)

**6.18** `mid(a,b)=c; mid(a,d)=e; mid(a,f)=g; mid(d,f)=b`
- order `a e d c b g f` : O: no increasing point; minimal order-infeasible sub-pattern (a,g,f), (d,b,f)
- order `a e d c g b f` : E: forces unlisted AP (e,c,g)
- order `a e d g c b f` : O: no increasing point; minimal order-infeasible sub-pattern (a,g,f), (a,c,b)
- (18 orders in total; first realizable shown, none realizable: first 3 orders shown)

### H7: triangle + pendant edge at an edge-private vertex (8 vertices): orders

Edges: {a,b,c}, {a,d,e}, {b,f,g}, {c,d,h}.

**7.1** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(d,h)=c`
- order `d c h a e f b g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- order `d c h a f e b g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- order `d c h a f b e g` : D: forces x_c-x_d = x_e-x_b
- (136 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.2** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(c,h)=d`
- order `c d h a f b e g` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `c d h a f b g e` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `c d h a e f b g` : D: forces x_d-x_c = x_b-x_e
- (144 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.3** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(c,d)=h`
- order `d h c a e f b g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- order `c h d a f b e g` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `d h c a f e b g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- (136 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.4** `mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(d,h)=c`
- order `d c h a e b f g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- order `d c h a e g f b` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- order `d c h a b e f g` : D: forces x_c-x_d = x_e-x_b
- (312 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.5** `mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(c,h)=d`
- order `c d h a b e f g` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `c d h a b f e g` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `c d h a b f g e` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- (304 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.6** `mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(c,d)=h`
- order `c h d a b e f g` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `d h c a e b f g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- order `c h d a b f e g` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- (312 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.7** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(d,h)=c`
- order `h e c d a f b g` : R  realization h=0, e=5, c=10, d=16, a=23, f=27, b=30, g=31
- (68 orders in total; first realizable shown)

**7.8** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(c,h)=d`
- order `f b g a c d e h` : O: no increasing point; minimal order-infeasible sub-pattern (a,d,e), (c,d,h)
- order `f b g a c d h e` : D: forces x_a-x_b = x_e-x_h
- order `e c d h a f b g` : D: forces x_h-x_c = x_g-x_a
- (136 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.9** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(c,d)=h`
- order `f b g a c h d e` : R  realization f=0, b=1, g=2, a=7, c=13, h=17, d=21, e=35
- (92 orders in total; first realizable shown)

**7.10** `mid(b,c)=a; mid(a,e)=d; mid(b,g)=f; mid(d,h)=c`
- order `h e c d a g f b` : R  realization h=0, e=6, c=12, d=13, a=21, g=26, f=29, b=31
- (184 orders in total; first realizable shown)

**7.11** `mid(b,c)=a; mid(a,e)=d; mid(b,g)=f; mid(c,h)=d`
- order `c a b d h e f g` : O: no increasing point; minimal order-infeasible sub-pattern (c,d,h), (a,d,e)
- order `c a b d h f e g` : O: no increasing point; minimal order-infeasible sub-pattern (c,d,h), (a,d,e)
- order `c a b d h f g e` : O: no increasing point; minimal order-infeasible sub-pattern (c,d,h), (a,d,e)
- (312 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.12** `mid(b,c)=a; mid(a,e)=d; mid(b,g)=f; mid(c,d)=h`
- order `c a b h d e f g` : R  realization c=0, a=3, b=6, h=7, d=14, e=25, f=27, g=48
- (216 orders in total; first realizable shown)

**7.13** `mid(b,c)=a; mid(a,d)=e; mid(f,g)=b; mid(d,h)=c`
- order `d c h e a f b g` : R  realization d=0, c=1, h=2, e=7, a=14, f=23, b=27, g=31
- (84 orders in total; first realizable shown)

**7.14** `mid(b,c)=a; mid(a,d)=e; mid(f,g)=b; mid(c,h)=d`
- order `c d h e a f b g` : R  realization c=0, d=1, h=2, e=7, a=13, f=22, b=26, g=30
- (80 orders in total; first realizable shown)

**7.15** `mid(b,c)=a; mid(a,d)=e; mid(f,g)=b; mid(c,d)=h`
- order `d h c e a f b g` : R  realization d=0, h=4, c=8, e=9, a=18, f=25, b=28, g=31
- (132 orders in total; first realizable shown)

**7.16** `mid(b,c)=a; mid(a,d)=e; mid(b,g)=f; mid(d,h)=c`
- order `d c h e a b f g` : R  realization d=0, c=1, h=2, e=7, a=14, b=27, f=31, g=35
- (224 orders in total; first realizable shown)

**7.17** `mid(b,c)=a; mid(a,d)=e; mid(b,g)=f; mid(c,h)=d`
- order `b a c f g e d h` : R  realization b=0, a=3, c=6, f=7, g=14, e=16, d=29, h=52
- (200 orders in total; first realizable shown)

**7.18** `mid(b,c)=a; mid(a,d)=e; mid(b,g)=f; mid(c,d)=h`
- order `b a c f g e h d` : R  realization b=0, a=6, c=12, f=13, g=26, e=28, h=31, d=50
- (288 orders in total; first realizable shown)

**7.19** `mid(a,c)=b; mid(d,e)=a; mid(f,g)=b; mid(d,h)=c`
- order `d a e f b c h g` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (f,b,g)
- order `d a e f b c g h` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,c), (f,b,g)
- order `e a f b g h c d` : D: forces x_b-x_a = x_c-x_h
- (60 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.20** `mid(a,c)=b; mid(d,e)=a; mid(f,g)=b; mid(c,h)=d`
- order `c d h f b a e g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (f,b,g)
- order `c d h f b a g e` : O: no increasing point; minimal order-infeasible sub-pattern (c,b,a), (f,b,g)
- order `c d h f b g a e` : D: forces x_f-x_c = x_a-x_g
- (124 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.21** `mid(a,c)=b; mid(d,e)=a; mid(f,g)=b; mid(c,d)=h`
- order `f c b g h e a d` : O: no increasing point; minimal order-infeasible sub-pattern (c,e,a), (h,e,d)
- order `c f b g h e a d` : D: forces x_h-x_f = x_d-x_a
- order `c h d f b a e g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (f,b,g)
- (172 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.22** `mid(a,c)=b; mid(d,e)=a; mid(b,g)=f; mid(d,h)=c`
- order `d a e b c h f g` : R  realization d=0, a=2, e=4, b=7, c=12, h=24, f=25, g=43
- (80 orders in total; first realizable shown)

**7.23** `mid(a,c)=b; mid(d,e)=a; mid(b,g)=f; mid(c,h)=d`
- order `c d h b a e f g` : R  realization c=0, d=2, h=4, b=7, a=14, e=26, f=27, g=47
- (184 orders in total; first realizable shown)

**7.24** `mid(a,c)=b; mid(d,e)=a; mid(b,g)=f; mid(c,d)=h`
- order `c h d b a e f g` : R  realization c=0, h=2, d=4, b=7, a=14, e=24, f=25, g=43
- (248 orders in total; first realizable shown)

**7.25** `mid(a,c)=b; mid(a,e)=d; mid(f,g)=b; mid(c,h)=d`
- order `a f b c d e g h` : O: no increasing point; minimal order-infeasible sub-pattern (a,d,e), (c,d,h)
- order `a f b c d e h g` : O: no increasing point; minimal order-infeasible sub-pattern (a,d,e), (c,d,h)
- order `a f b c d g e h` : O: no increasing point; minimal order-infeasible sub-pattern (a,d,e), (c,d,h)
- (88 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.26** `mid(a,c)=b; mid(a,e)=d; mid(f,g)=b; mid(c,d)=h`
- order `a d e f b h c g` : O: no increasing point; minimal order-infeasible sub-pattern (d,h,c), (f,b,g)
- order `c f h b g e d a` : D: forces x_b-x_c = x_a-x_d
- order `c h f b g e d a` : D: forces x_b-x_c = x_a-x_e
- (164 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.27** `mid(a,c)=b; mid(a,e)=d; mid(b,g)=f; mid(c,h)=d`
- order `a b c d e f g h` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,g), (c,d,h)
- order `a b c d e f h g` : O: no increasing point; minimal order-infeasible sub-pattern (a,d,e), (c,d,h)
- order `a b c d e h f g` : O: no increasing point; minimal order-infeasible sub-pattern (a,d,e), (c,d,h)
- (136 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.28** `mid(a,c)=b; mid(a,e)=d; mid(b,g)=f; mid(c,d)=h`
- order `c b a h d f e g` : R  realization c=0, b=1, a=2, h=7, d=14, f=18, e=26, g=35
- (256 orders in total; first realizable shown)

**7.29** `mid(a,c)=b; mid(a,d)=e; mid(f,g)=b; mid(c,d)=h`
- order `f a b g e c h d` : O: no increasing point; minimal order-infeasible sub-pattern (b,c,h), (e,c,d)
- order `a f b g e c h d` : D: forces x_f-x_a = x_c-x_g
- order `a e d f b h c g` : O: no increasing point; minimal order-infeasible sub-pattern (d,h,c), (f,b,g)
- (64 orders in total; first realizable shown, none realizable: first 3 orders shown)

**7.30** `mid(a,c)=b; mid(a,d)=e; mid(b,g)=f; mid(c,d)=h`
- order `a b c e h d f g` : D: forces x_b-x_a = x_h-x_e
- order `a e d b h c f g` : D: forces x_e-x_a = x_h-x_b
- order `g f a b e c h d` : D: forces x_f-x_g = x_e-x_b
- (104 orders in total; first realizable shown, none realizable: first 3 orders shown)

### H8: 4-cycle of edges (no triangle) (8 vertices): orders

Edges: {a,b,c}, {a,d,e}, {b,f,g}, {d,f,h}.

**8.1** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(f,h)=d`
- order `f b g d h a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `f b g d h a e c` : D: forces x_d-x_b = x_c-x_e
- order `f b g d a h c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- (140 orders in total; first realizable shown, none realizable: first 3 orders shown)

**8.2** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(d,h)=f`
- order `d f h b a e g c` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- order `d f h b a e c g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- order `d f h c a e b g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- (256 orders in total; first realizable shown, none realizable: first 3 orders shown)

**8.3** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(d,f)=h`
- order `f b g h d a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `f b g h d a e c` : D: forces x_d-x_b = x_c-x_e
- order `f h d b g a e c` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (b,a,c)
- (296 orders in total; first realizable shown, none realizable: first 3 orders shown)

**8.4** `mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(d,h)=f`
- order `b d a c f g e h` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,g), (d,f,h)
- order `b d a c f g h e` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (d,f,h)
- order `b d a c f e g h` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,g), (d,f,h)
- (102 orders in total; first realizable shown, none realizable: first 3 orders shown)

**8.5** `mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(d,f)=h`
- order `b f g e a c h d` : O: no increasing point; minimal order-infeasible sub-pattern (f,h,d), (e,a,d)
- order `b f g e a h c d` : O: no increasing point; minimal order-infeasible sub-pattern (f,h,d), (e,a,d)
- order `b f g e a h d c` : O: no increasing point; minimal order-infeasible sub-pattern (f,h,d), (e,a,d)
- (288 orders in total; first realizable shown, none realizable: first 3 orders shown)

**8.6** `mid(b,c)=a; mid(d,e)=a; mid(b,f)=g; mid(d,f)=h`
- order `f g b h d a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `f g b h d a e c` : D: forces x_d-x_b = x_c-x_e
- order `f g b h e a d c` : D: forces x_e-x_b = x_c-x_d
- (172 orders in total; first realizable shown, none realizable: first 3 orders shown)

**8.7** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(d,h)=f`
- order `c a g b d f e h` : R  realization c=0, a=13, g=16, b=26, d=27, f=36, e=41, h=45
- (41 orders in total; first realizable shown)

**8.8** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(d,f)=h`
- order `f b g h a d c e` : R  realization f=0, b=1, g=2, h=12, a=15, d=24, c=29, e=33
- (188 orders in total; first realizable shown)

**8.9** `mid(b,c)=a; mid(a,e)=d; mid(b,g)=f; mid(d,f)=h`
- order `b f g a c h d e` : R  realization b=0, f=3, g=6, a=7, c=14, h=16, d=29, e=51
- (176 orders in total; first realizable shown)

**8.10** `mid(b,c)=a; mid(a,e)=d; mid(b,f)=g; mid(d,f)=h`
- order `b a c g f h d e` : R  realization b=0, a=1, c=2, g=7, f=14, h=18, d=22, e=43
- (228 orders in total; first realizable shown)

**8.11** `mid(b,c)=a; mid(a,d)=e; mid(b,g)=f; mid(d,f)=h`
- order `b a c f g e h d` : R  realization b=0, a=5, c=10, f=11, g=22, e=26, h=29, d=47
- (124 orders in total; first realizable shown)

**8.12** `mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(f,h)=d`
- order `b a c g f e d h` : R  realization b=0, a=3, c=6, g=7, f=14, e=16, d=29, h=44
- (112 orders in total; first realizable shown)

**8.13** `mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(d,h)=f`
- order `b a c g e d f h` : R  realization b=0, a=5, c=10, g=17, e=18, d=31, f=34, h=37
- (134 orders in total; first realizable shown)

**8.14** `mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(d,f)=h`
- order `b a c g f e h d` : R  realization b=0, a=2, c=4, g=9, f=18, e=21, h=29, d=40
- (244 orders in total; first realizable shown)

**8.15** `mid(a,b)=c; mid(a,d)=e; mid(b,f)=g; mid(d,f)=h`
- order `a c b e d g h f` : D: forces x_e-x_c = x_h-x_g
- order `a c b e d h g f` : O: no increasing point; minimal order-infeasible sub-pattern (b,g,f), (d,h,f)
- order `a c b e g d h f` : D: forces x_e-x_c = x_h-x_g
- (43 orders in total; first realizable shown, none realizable: first 3 orders shown)

### H9: two triangles sharing two edges (7 vertices): orders

Edges: {a,b,c}, {a,d,e}, {b,f,g}, {c,d,f}.

**9.1** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(d,f)=c`
- order `d c f a e b g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- order `d c f a b e g` : D: forces x_c-x_d = x_e-x_b
- order `d c f a b g e` : O: no increasing point; minimal order-infeasible sub-pattern (d,c,f), (d,a,e), (c,a,b), (f,b,g)
- (32 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.2** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(c,f)=d`
- order `c d f a b e g` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `c d f a b g e` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `c d f a e b g` : E: forces unlisted AP (c,e,g)
- (43 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.3** `mid(b,c)=a; mid(d,e)=a; mid(f,g)=b; mid(c,d)=f`
- order `c f d a b g e` : O: no increasing point; minimal order-infeasible sub-pattern (f,b,g), (d,a,e)
- order `c f d a b e g` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `d f c a e b g` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- (29 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.4** `mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(d,f)=c`
- order `b f g e a c d` : O: no increasing point; minimal order-infeasible sub-pattern (f,c,d), (e,a,d)
- order `d c a e b f g` : O: no increasing point; minimal order-infeasible sub-pattern (a,b,f), (e,b,g)
- order `b e a f g c d` : O: no increasing point; minimal order-infeasible sub-pattern (e,g,d), (a,f,d)
- (33 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.5** `mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(c,f)=d`
- order `b f g d a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `b f g d a e c` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (f,d,c)
- order `b f g e a d c` : D: forces x_f-x_b = x_d-x_e
- (39 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.6** `mid(b,c)=a; mid(d,e)=a; mid(b,g)=f; mid(c,d)=f`
- order `b d f g a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- order `e b a d f g c` : O: no increasing point; minimal order-infeasible sub-pattern (e,f,g), (d,f,c)
- order `b e a c f g d` : O: no increasing point; minimal order-infeasible sub-pattern (b,f,g), (c,f,d)
- (23 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.7** `mid(b,c)=a; mid(d,e)=a; mid(b,f)=g; mid(d,f)=c`
- order `d c f a e g b` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- order `d c f a g e b` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,e), (c,a,b)
- order `f c d g a b e` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- (47 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.8** `mid(b,c)=a; mid(d,e)=a; mid(b,f)=g; mid(c,f)=d`
- order `c d f a g b e` : O: no increasing point; minimal order-infeasible sub-pattern (c,a,b), (d,a,e)
- order `f d c g a b e` : D: forces x_d-x_f = x_a-x_g
- order `f g b d a c e` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (d,a,e)
- (30 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.9** `mid(b,c)=a; mid(d,e)=a; mid(b,f)=g; mid(c,d)=f`
- order `d f c a e g b` : O: no increasing point; minimal order-infeasible sub-pattern (f,g,b), (c,a,b)
- order `c f d a g b e` : O: no increasing point; minimal order-infeasible sub-pattern (f,g,b), (d,a,e)
- order `d f c a g e b` : O: no increasing point; minimal order-infeasible sub-pattern (f,g,b), (c,a,b)
- (39 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.10** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(d,f)=c`
- order `f b g a c d e` : R  realization f=0, b=1, g=2, a=5, c=9, d=18, e=31
- (16 orders in total; first realizable shown)

**9.11** `mid(b,c)=a; mid(a,e)=d; mid(f,g)=b; mid(c,d)=f`
- order `c a f b d g e` : R  realization c=0, a=7, f=8, b=14, d=16, g=20, e=25
- (10 orders in total; first realizable shown)

**9.12** `mid(b,c)=a; mid(a,e)=d; mid(b,g)=f; mid(d,f)=c`
- order `b f g a c d e` : R  realization b=0, f=2, g=4, a=5, c=10, d=18, e=31
- (17 orders in total; first realizable shown)

**9.13** `mid(b,c)=a; mid(a,e)=d; mid(b,f)=g; mid(d,f)=c`
- order `b g f a c d e` : R  realization b=0, g=2, f=4, a=5, c=10, d=16, e=27
- (30 orders in total; first realizable shown)

**9.14** `mid(b,c)=a; mid(a,e)=d; mid(b,f)=g; mid(c,d)=f`
- order `b a c g f d e` : R  realization b=0, a=2, c=4, g=5, f=10, d=16, e=30
- (29 orders in total; first realizable shown)

**9.15** `mid(b,c)=a; mid(a,d)=e; mid(f,g)=b; mid(d,f)=c`
- order `d c f e a b g` : R  realization d=0, c=2, f=4, e=5, a=10, b=18, g=32
- (22 orders in total; first realizable shown)

**9.16** `mid(b,c)=a; mid(a,d)=e; mid(f,g)=b; mid(c,f)=d`
- order `f b g d e a c` : R  realization f=0, b=4, g=8, d=13, e=14, a=15, c=26
- (23 orders in total; first realizable shown)

**9.17** `mid(b,c)=a; mid(a,d)=e; mid(b,g)=f; mid(d,f)=c`
- order `b f g a c e d` : R  realization b=0, f=3, g=6, a=7, c=14, e=16, d=25
- (27 orders in total; first realizable shown)

**9.18** `mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(d,f)=c`
- order `d c f e a g b` : R  realization d=0, c=2, f=4, e=7, a=14, g=15, b=26
- (28 orders in total; first realizable shown)

**9.19** `mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(c,f)=d`
- order `b a c g e d f` : O: no increasing point; minimal order-infeasible sub-pattern (b,a,c), (b,g,f), (a,e,d), (c,d,f)
- order `b g f a e d c` : E: forces unlisted AP (g,e,c)
- order `b g a e f d c` : E: forces unlisted AP (b,e,d)
- (12 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.20** `mid(b,c)=a; mid(a,d)=e; mid(b,f)=g; mid(c,d)=f`
- order `b a c g e f d` : R  realization b=0, a=2, c=4, g=7, e=13, f=14, d=24
- (20 orders in total; first realizable shown)

**9.21** `mid(a,b)=c; mid(d,e)=a; mid(f,g)=b; mid(d,f)=c`
- order `d a e c f b g` : O: no increasing point; minimal order-infeasible sub-pattern (d,c,f), (a,c,b)
- order `d a e c g b f` : E: forces unlisted AP (e,c,g)
- order `d a c e g b f` : O: no increasing point; minimal order-infeasible sub-pattern (d,a,c), (d,g,f), (a,g,b), (e,b,f)
- (23 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.22** `mid(a,b)=c; mid(d,e)=a; mid(b,g)=f; mid(d,f)=c`
- order `b f g c d a e` : D: forces x_f-x_b = x_a-x_d
- order `b f g c e a d` : O: no increasing point; minimal order-infeasible sub-pattern (b,c,a), (f,c,d)
- order `b f c g e a d` : O: no increasing point; minimal order-infeasible sub-pattern (b,e,a), (f,e,d)
- (23 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.23** `mid(a,b)=c; mid(d,e)=a; mid(b,f)=g; mid(d,f)=c`
- order `d a e c f g b` : O: no increasing point; minimal order-infeasible sub-pattern (d,c,f), (a,c,b)
- order `f g b c d a e` : O: no increasing point; minimal order-infeasible sub-pattern (f,c,d), (b,c,a)
- order `b g f c d a e` : D: forces x_f-x_b = x_a-x_d
- (33 orders in total; first realizable shown, none realizable: first 3 orders shown)

**9.24** `mid(a,b)=c; mid(a,d)=e; mid(b,f)=g; mid(d,f)=c`
- order `a e d c b g f` : O: no increasing point; minimal order-infeasible sub-pattern (a,c,b), (d,c,f)
- order `a e d c f g b` : E: forces unlisted AP (e,c,g)
- order `a e f c d g b` : E: forces unlisted AP (e,c,g)
- (14 orders in total; first realizable shown, none realizable: first 3 orders shown)
