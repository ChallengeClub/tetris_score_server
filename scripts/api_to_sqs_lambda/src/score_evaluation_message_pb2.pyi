from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScoreEvaluationMessage(_message.Message):
    __slots__ = ["branch", "created_at", "drop_interval", "game_mode", "game_time", "id", "level", "predict_weight_path", "repository_url", "timeout", "trial_num"]
    class GameLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DROP_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    FOUR: ScoreEvaluationMessage.GameLevel
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    GAME_TIME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    ONE: ScoreEvaluationMessage.GameLevel
    PREDICT_WEIGHT_PATH_FIELD_NUMBER: _ClassVar[int]
    REPOSITORY_URL_FIELD_NUMBER: _ClassVar[int]
    THREE: ScoreEvaluationMessage.GameLevel
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    TRIAL_NUM_FIELD_NUMBER: _ClassVar[int]
    TWO: ScoreEvaluationMessage.GameLevel
    ZERO: ScoreEvaluationMessage.GameLevel
    branch: str
    created_at: int
    drop_interval: int
    game_mode: str
    game_time: int
    id: str
    level: ScoreEvaluationMessage.GameLevel
    predict_weight_path: str
    repository_url: str
    timeout: int
    trial_num: int
    def __init__(self, id: _Optional[str] = ..., created_at: _Optional[int] = ..., repository_url: _Optional[str] = ..., branch: _Optional[str] = ..., drop_interval: _Optional[int] = ..., level: _Optional[_Union[ScoreEvaluationMessage.GameLevel, str]] = ..., game_mode: _Optional[str] = ..., game_time: _Optional[int] = ..., timeout: _Optional[int] = ..., predict_weight_path: _Optional[str] = ..., trial_num: _Optional[int] = ...) -> None: ...
