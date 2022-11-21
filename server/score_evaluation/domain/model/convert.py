from uuid import uuid4
from .score_evaluation_message_pb2 import ScoreEvaluationMessage
from .entity import Evaluation

def protobuf_message_to_django_model(msg: ScoreEvaluationMessage)-> Evaluation:
    eval = Evaluation(str(uuid4())) # generate new uuid 
    eval.repository_url = msg.repository_url
    eval.branch = msg.branch
    eval.game_mode = msg.game_mode
    eval.game_time = msg.game_time
    eval.drop_interval = msg.drop_interval
    eval.level = msg.level
    eval.trial_num = msg.trial_num

    return eval