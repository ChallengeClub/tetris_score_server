from django.db import models
import json
from uuid import uuid4
from datetime import datetime

class Evaluation(models.Model):
    id = models.UUIDField(primary_key=True, default=str(uuid4), editable=False) # Object of type UUID is not JSON serializable
    created_at = models.DateTimeField(default=str(datetime.now())) # Object of type datetime is not JSON serializable
    ended_at = models.DateTimeField()
    repository_url = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    game_time = models.IntegerField(default=180)

    class EvaluationStatus(models.TextChoices):
        WAIT = 'W', ('waiting in queue')
        EVALUATING = 'EV', ('evaluating')
        SUCCESS = 'S', ('evaluation successfully ended')
        ERROR = 'ER', ('evaluation ended with error')
    error_message = models.TextField(default="")
    status = models.CharField(max_length=2, choices=EvaluationStatus.choices, default=EvaluationStatus.WAIT)
    drop_interval = models.IntegerField(default=1000)
    value_mode = models.CharField(max_length=10, default="default")
    value_predict_weight = models.CharField(max_length=100, default="")
    trial_num = models.IntegerField(default=1)
    score_mean = models.FloatField(default=0)
    score_stdev = models.FloatField(default=0)
    score_max = models.FloatField(default=0)
    score_min = models.FloatField(default=0)

    def to_json(self):
        data = {
            "id": self.id, 
            "created_at": self.created_at,
            "ended_at": self.ended_at,
            "repository_url": self.repository_url,
            "branch": self.branch,
            "game_time": self.game_time,
            "level": self.level,
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
        return self.repository_url+ " | " + self.branch
