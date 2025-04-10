from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Marks, student
from django.db import models


@receiver(post_save, sender=Marks)
def update_student_average_scores(sender, instance, **kwargs):
    student_obj = instance.student

    # Get all marks for this student
    marks = Marks.objects.filter(student=student_obj)

    # Calculate new averages
    avg_sat = marks.aggregate(models.Avg('sat_score'))['sat_score__avg'] or 0
    avg_pat = marks.aggregate(models.Avg('pat_score'))['pat_score__avg'] or 0

    # Update student object
    student_obj.avg_sat_score = avg_sat
    student_obj.avg_pat_score = avg_pat
    student_obj.save()
 