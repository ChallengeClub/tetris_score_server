# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: score_evaluation_message.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1escore_evaluation_message.proto\x12\x08tutorial\"\xbd\x03\n\x16ScoreEvaluationMessage\x12\x11\n\x04name\x18\x0c \x01(\tH\x00\x88\x01\x01\x12\x0f\n\x02id\x18\n \x01(\tH\x01\x88\x01\x01\x12\x17\n\ncreated_at\x18\x0b \x01(\x05H\x02\x88\x01\x01\x12\x16\n\x0erepository_url\x18\x01 \x01(\t\x12\x0e\n\x06\x62ranch\x18\x02 \x01(\t\x12\x15\n\rdrop_interval\x18\x03 \x01(\x05\x12\x39\n\x05level\x18\x04 \x01(\x0e\x32*.tutorial.ScoreEvaluationMessage.GameLevel\x12\x11\n\tgame_mode\x18\x05 \x01(\t\x12\x11\n\tgame_time\x18\x06 \x01(\x05\x12\x0f\n\x07timeout\x18\x07 \x01(\x05\x12\x1b\n\x13predict_weight_path\x18\x08 \x01(\t\x12\x11\n\ttrial_num\x18\t \x01(\x05\x12\x18\n\x0brandom_seed\x18\r \x01(\x04H\x03\x88\x01\x01\"<\n\tGameLevel\x12\x08\n\x04ZERO\x10\x00\x12\x07\n\x03ONE\x10\x01\x12\x07\n\x03TWO\x10\x02\x12\t\n\x05THREE\x10\x03\x12\x08\n\x04\x46OUR\x10\x04\x42\x07\n\x05_nameB\x05\n\x03_idB\r\n\x0b_created_atB\x0e\n\x0c_random_seedb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'score_evaluation_message_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SCOREEVALUATIONMESSAGE._serialized_start=45
  _SCOREEVALUATIONMESSAGE._serialized_end=490
  _SCOREEVALUATIONMESSAGE_GAMELEVEL._serialized_start=383
  _SCOREEVALUATIONMESSAGE_GAMELEVEL._serialized_end=443
# @@protoc_insertion_point(module_scope)
