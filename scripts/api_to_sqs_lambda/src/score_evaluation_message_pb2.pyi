from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScoreEvaluationMessage(_message.Message):
    __slots__ = ["branch_name", "drop_interval", "game_level", "machine_learning_mode", "predict_weight_path", "repository_url"]
    class GameLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class MachineLearningMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT: ScoreEvaluationMessage.MachineLearningMode
    DROP_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    EASY: ScoreEvaluationMessage.GameLevel
    GAME_LEVEL_FIELD_NUMBER: _ClassVar[int]
    HARD: ScoreEvaluationMessage.GameLevel
    MACHINE_LEARNING_MODE_FIELD_NUMBER: _ClassVar[int]
    MIDIUM: ScoreEvaluationMessage.GameLevel
    PREDICT: ScoreEvaluationMessage.MachineLearningMode
    PREDICT_SAMPLE: ScoreEvaluationMessage.MachineLearningMode
    PREDICT_SAMPLE2: ScoreEvaluationMessage.MachineLearningMode
    PREDICT_WEIGHT_PATH_FIELD_NUMBER: _ClassVar[int]
    REPOSITORY_URL_FIELD_NUMBER: _ClassVar[int]
    branch_name: str
    drop_interval: int
    game_level: ScoreEvaluationMessage.GameLevel
    machine_learning_mode: ScoreEvaluationMessage.MachineLearningMode
    predict_weight_path: str
    repository_url: str
    def __init__(self, repository_url: _Optional[str] = ..., game_level: _Optional[_Union[ScoreEvaluationMessage.GameLevel, str]] = ..., branch_name: _Optional[str] = ..., drop_interval: _Optional[int] = ..., machine_learning_mode: _Optional[_Union[ScoreEvaluationMessage.MachineLearningMode, str]] = ..., predict_weight_path: _Optional[str] = ...) -> None: ...
