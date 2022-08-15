from django.db import models
import json

class EvaluationResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now=True)
    repository_url = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    score = models.IntegerField(default=0)

    class EvaluationStatus(models.TextChoices):
        WAIT = 'W', ('waiting in queue')
        EVALUATING = 'EV', ('evaluating')
        SUCCESS = 'S', ('evaluation successfully ended')
        ERROR = 'ER', ('evaluation ended with error')
    error_message = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=2, choices=EvaluationStatus.choices, default=EvaluationStatus.WAIT)
    drop_interval = models.IntegerField()
    value_mode = models.CharField(max_length=10)
    value_predict_weight = models.CharField(max_length=100, default="")
    trial_num = models.IntegerField()
    score_mean = models.FloatField(default=0)
    score_stdev = models.FloatField(default=0)
    score_max = models.FloatField(default=0)
    score_min = models.FloatField(default=0)

    def to_json(self):
        data = {
            "id": self.id,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "repository_url": self.repository_url,
            "branch": self.branch,
            "error_message": self.error_message,
            "status": self.status,
            "drop_interval": self.drop_interval,
            "value_mode": self.value_mode,
            "value_predict_weight": self.value_predict_weight,
            "trial_num": self.trial_num,
            "score_mean": self.score_mean,
            "score_stdev": self.score_stdev,
            "score_max": self.score_max,
            "score_min": self.score_min
        }
        return json.dumps(data)
    
    def __str__(self):
        return self.repository_url + self.branch
