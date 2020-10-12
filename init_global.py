from PhysicsLab.models import WeekStatus
for i in range(1, 17):
    v = WeekStatus()
    v.is_drawn = False
    v.week = i
    v.save()