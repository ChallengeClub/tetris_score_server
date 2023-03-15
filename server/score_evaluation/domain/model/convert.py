from .score_evaluation_message_pb2 import ScoreEvaluationMessage
from .entity import Evaluation

def protobuf_message_to_django_model(msg: ScoreEvaluationMessage)-> Evaluation:
    eval = Evaluation()
    eval.id = msg.id
    eval.created_at = msg.created_at
    eval.name = msg.name
    eval.repository_url = msg.repository_url
    eval.branch = msg.branch
    eval.game_mode = msg.game_mode
    eval.game_time = msg.game_time
    eval.drop_interval = msg.drop_interval
    eval.level = msg.level
    eval.trial_num = msg.trial_num
    eval.random_seeds["values"] = msg.random_seeds
    eval.value_predict_weight = msg.predict_weight_path

    return eval