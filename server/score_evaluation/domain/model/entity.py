from django.db import models
import json
from uuid import uuid4

class Evaluation(models.Model):
    id = models.UUIDField(primary_key=True, default=str(uuid4()), editable=False) # Object of type UUID is not JSON serializable
    name = models.CharField(max_length=50)
    receipt_handle = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    repository_url = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    drop_interval = models.IntegerField(default=1000)
    level = models.IntegerField(default=1)    
    game_mode = models.CharField(max_length=50, default="default")
    game_time = models.IntegerField(default=180)
    timeout = models.IntegerField(default=200)
    value_predict_weight = models.CharField(max_length=100, default="")
    error_message = models.TextField(default="")
    class EvaluationStatus(models.TextChoices):
        WAIT = 'waiting', ('waiting in queue')
        EVALUATING = 'evaluating', ('evaluating')
        SUCCESS = 'succeeded', ('evaluation successfully ended')
        ERROR = 'error', ('evaluation ended with error')
    status = models.CharField(max_length=15, choices=EvaluationStatus.choices, default=EvaluationStatus.WAIT)
    trial_num = models.IntegerField(default=1)
    score_mean = models.FloatField(default=0)
    score_stdev = models.FloatField(default=0)
    score_max = models.FloatField(default=0)
    score_min = models.FloatField(default=0)
    random_seed = models.BigIntegerField(default=0)
    
    def to_json(self):
        data = self.to_dict()
        return json.dumps(data)
    
    def to_dict(self):
        data = {
            "id": self.id, 
            "name": self.name,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "repository_url": self.repository_url,
            "branch": self.branch,
            "game_time": self.game_time,
            "level": self.level,
            "error_message": self.error_message,
            "status": self.status,
            "drop_interval": self.drop_interval,
            "game_mode": self.game_mode,
            "predict_weight_path": self.value_predict_weight,
            "trial_num": self.trial_num,
            "mean_score": int(self.score_mean),
            "std_dev_score": int(self.score_stdev),
            "max_score": self.score_max,
            "min_score": self.score_min,
            "random_seed": self.random_seed
        }
        return data
    
    
    def __str__(self):
        return self.name + " | " + self.repository_url+ " | " + self.branch + " | level" + str(self.level)
