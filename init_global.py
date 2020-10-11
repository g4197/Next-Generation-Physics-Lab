from PhysicsLab.models import GlobalVariable
for i in range(1, 17):
    v = GlobalVariable()
    v.is_drawn = False
    v.week = i
    v.save()