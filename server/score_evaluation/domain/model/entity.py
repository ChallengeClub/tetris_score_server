from django.db import models
import json
from uuid import uuid4
from time import time
from datetime import datetime

class Evaluation(models.Model):
    id = models.UUIDField(primary_key=True, default=str(uuid4()), editable=False) # Object of type UUID is not JSON serializable
    receipt_handle = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=int(time()))
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
        WAIT = 'W', ('waiting in queue')
        EVALUATING = 'EV', ('evaluating')
        SUCCESS = 'S', ('evaluation successfully ended')
        ERROR = 'ER', ('evaluation ended with error')
    status = models.CharField(max_length=2, choices=EvaluationStatus.choices, default=EvaluationStatus.WAIT)
    trial_num = models.IntegerField(default=1)
    score_mean = models.FloatField(default=0)
    score_stdev = models.FloatField(default=0)
    score_max = models.FloatField(default=0)
    score_min = models.FloatField(default=0)
    

    def to_json(self):
        data = self.to_dict()
        return json.dumps(data)
    
    def to_dict(self):
        data = {
            "Id": self.id, 
            "CreatedAt": self.created_at,
            "EndedAt": self.ended_at,
            "RepositoryURL": self.repository_url,
            "Branch": self.branch,
            "GameTime": self.game_time,
            "Level": self.level,
            "ErrorMessage": self.error_message,
            "Status": self.status,
            "DropInterval": self.drop_interval,
            "GameMode": self.game_mode,
            "ValuePredictWeight": self.value_predict_weight,
            "TrialNum": self.trial_num,
            "MeanScore": int(self.score_mean),
            "StdDevScore": int(self.score_stdev),
            "MaxScore": self.score_max,
            "MinScore": self.score_min
        }
        return data
    
    
    def __str__(self):
        return self.repository_url+ " | " + self.branch
