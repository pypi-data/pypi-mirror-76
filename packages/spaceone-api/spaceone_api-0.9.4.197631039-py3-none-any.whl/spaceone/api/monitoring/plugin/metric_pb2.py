# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/monitoring/plugin/metric.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from spaceone.api.core.v1 import plugin_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_plugin__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/monitoring/plugin/metric.proto',
  package='spaceone.api.monitoring.plugin',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+spaceone/api/monitoring/plugin/metric.proto\x12\x1espaceone.api.monitoring.plugin\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a!spaceone/api/core/v1/plugin.proto\"\x91\x01\n\rMetricRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12(\n\x08resource\x18\x03 \x01(\x0b\x32\x16.google.protobuf.Value\"\x97\x02\n\x11MetricDataRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12(\n\x08resource\x18\x03 \x01(\x0b\x32\x16.google.protobuf.Value\x12\x0e\n\x06metric\x18\x04 \x01(\t\x12)\n\x05start\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\'\n\x03\x65nd\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06period\x18\x07 \x01(\x05\x12\x0c\n\x04stat\x18\x08 \x01(\t\"\x92\x01\n\nMetricInfo\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04unit\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x12\n\nchart_type\x18\x04 \x01(\t\x12.\n\rchart_options\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\"J\n\x0bMetricsInfo\x12;\n\x07metrics\x18\x01 \x03(\x0b\x32*.spaceone.api.monitoring.plugin.MetricInfo\"h\n\x0eMetricDataInfo\x12*\n\x06labels\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12*\n\x06values\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.ListValue\"\xa0\x01\n\x15PluginMetricsResponse\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12\x33\n\x07\x61\x63tions\x18\x02 \x03(\x0b\x32\".spaceone.api.core.v1.PluginAction\x12;\n\x06result\x18\x03 \x01(\x0b\x32+.spaceone.api.monitoring.plugin.MetricsInfo\"\xa6\x01\n\x18PluginMetricDataResponse\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12\x33\n\x07\x61\x63tions\x18\x02 \x03(\x0b\x32\".spaceone.api.core.v1.PluginAction\x12>\n\x06result\x18\x03 \x01(\x0b\x32..spaceone.api.monitoring.plugin.MetricDataInfo2\xf7\x01\n\x06Metric\x12p\n\x04list\x12-.spaceone.api.monitoring.plugin.MetricRequest\x1a\x35.spaceone.api.monitoring.plugin.PluginMetricsResponse\"\x00\x30\x01\x12{\n\x08get_data\x12\x31.spaceone.api.monitoring.plugin.MetricDataRequest\x1a\x38.spaceone.api.monitoring.plugin.PluginMetricDataResponse\"\x00\x30\x01\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,spaceone_dot_api_dot_core_dot_v1_dot_plugin__pb2.DESCRIPTOR,])




_METRICREQUEST = _descriptor.Descriptor(
  name='MetricRequest',
  full_name='spaceone.api.monitoring.plugin.MetricRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.monitoring.plugin.MetricRequest.options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secret_data', full_name='spaceone.api.monitoring.plugin.MetricRequest.secret_data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resource', full_name='spaceone.api.monitoring.plugin.MetricRequest.resource', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=178,
  serialized_end=323,
)


_METRICDATAREQUEST = _descriptor.Descriptor(
  name='MetricDataRequest',
  full_name='spaceone.api.monitoring.plugin.MetricDataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.monitoring.plugin.MetricDataRequest.options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secret_data', full_name='spaceone.api.monitoring.plugin.MetricDataRequest.secret_data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='resource', full_name='spaceone.api.monitoring.plugin.MetricDataRequest.resource', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='metric', full_name='spaceone.api.monitoring.plugin.MetricDataRequest.metric', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start', full_name='spaceone.api.monitoring.plugin.MetricDataRequest.start', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end', full_name='spaceone.api.monitoring.plugin.MetricDataRequest.end', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='period', full_name='spaceone.api.monitoring.plugin.MetricDataRequest.period', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stat', full_name='spaceone.api.monitoring.plugin.MetricDataRequest.stat', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=326,
  serialized_end=605,
)


_METRICINFO = _descriptor.Descriptor(
  name='MetricInfo',
  full_name='spaceone.api.monitoring.plugin.MetricInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='spaceone.api.monitoring.plugin.MetricInfo.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.monitoring.plugin.MetricInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='unit', full_name='spaceone.api.monitoring.plugin.MetricInfo.unit', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chart_type', full_name='spaceone.api.monitoring.plugin.MetricInfo.chart_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chart_options', full_name='spaceone.api.monitoring.plugin.MetricInfo.chart_options', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=608,
  serialized_end=754,
)


_METRICSINFO = _descriptor.Descriptor(
  name='MetricsInfo',
  full_name='spaceone.api.monitoring.plugin.MetricsInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='metrics', full_name='spaceone.api.monitoring.plugin.MetricsInfo.metrics', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=756,
  serialized_end=830,
)


_METRICDATAINFO = _descriptor.Descriptor(
  name='MetricDataInfo',
  full_name='spaceone.api.monitoring.plugin.MetricDataInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='labels', full_name='spaceone.api.monitoring.plugin.MetricDataInfo.labels', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='values', full_name='spaceone.api.monitoring.plugin.MetricDataInfo.values', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=832,
  serialized_end=936,
)


_PLUGINMETRICSRESPONSE = _descriptor.Descriptor(
  name='PluginMetricsResponse',
  full_name='spaceone.api.monitoring.plugin.PluginMetricsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_type', full_name='spaceone.api.monitoring.plugin.PluginMetricsResponse.resource_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='actions', full_name='spaceone.api.monitoring.plugin.PluginMetricsResponse.actions', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result', full_name='spaceone.api.monitoring.plugin.PluginMetricsResponse.result', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=939,
  serialized_end=1099,
)


_PLUGINMETRICDATARESPONSE = _descriptor.Descriptor(
  name='PluginMetricDataResponse',
  full_name='spaceone.api.monitoring.plugin.PluginMetricDataResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_type', full_name='spaceone.api.monitoring.plugin.PluginMetricDataResponse.resource_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='actions', full_name='spaceone.api.monitoring.plugin.PluginMetricDataResponse.actions', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result', full_name='spaceone.api.monitoring.plugin.PluginMetricDataResponse.result', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1102,
  serialized_end=1268,
)

_METRICREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_METRICREQUEST.fields_by_name['secret_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_METRICREQUEST.fields_by_name['resource'].message_type = google_dot_protobuf_dot_struct__pb2._VALUE
_METRICDATAREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_METRICDATAREQUEST.fields_by_name['secret_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_METRICDATAREQUEST.fields_by_name['resource'].message_type = google_dot_protobuf_dot_struct__pb2._VALUE
_METRICDATAREQUEST.fields_by_name['start'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_METRICDATAREQUEST.fields_by_name['end'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_METRICINFO.fields_by_name['unit'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_METRICINFO.fields_by_name['chart_options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_METRICSINFO.fields_by_name['metrics'].message_type = _METRICINFO
_METRICDATAINFO.fields_by_name['labels'].message_type = google_dot_protobuf_dot_struct__pb2._LISTVALUE
_METRICDATAINFO.fields_by_name['values'].message_type = google_dot_protobuf_dot_struct__pb2._LISTVALUE
_PLUGINMETRICSRESPONSE.fields_by_name['actions'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_plugin__pb2._PLUGINACTION
_PLUGINMETRICSRESPONSE.fields_by_name['result'].message_type = _METRICSINFO
_PLUGINMETRICDATARESPONSE.fields_by_name['actions'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_plugin__pb2._PLUGINACTION
_PLUGINMETRICDATARESPONSE.fields_by_name['result'].message_type = _METRICDATAINFO
DESCRIPTOR.message_types_by_name['MetricRequest'] = _METRICREQUEST
DESCRIPTOR.message_types_by_name['MetricDataRequest'] = _METRICDATAREQUEST
DESCRIPTOR.message_types_by_name['MetricInfo'] = _METRICINFO
DESCRIPTOR.message_types_by_name['MetricsInfo'] = _METRICSINFO
DESCRIPTOR.message_types_by_name['MetricDataInfo'] = _METRICDATAINFO
DESCRIPTOR.message_types_by_name['PluginMetricsResponse'] = _PLUGINMETRICSRESPONSE
DESCRIPTOR.message_types_by_name['PluginMetricDataResponse'] = _PLUGINMETRICDATARESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MetricRequest = _reflection.GeneratedProtocolMessageType('MetricRequest', (_message.Message,), {
  'DESCRIPTOR' : _METRICREQUEST,
  '__module__' : 'spaceone.api.monitoring.plugin.metric_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.plugin.MetricRequest)
  })
_sym_db.RegisterMessage(MetricRequest)

MetricDataRequest = _reflection.GeneratedProtocolMessageType('MetricDataRequest', (_message.Message,), {
  'DESCRIPTOR' : _METRICDATAREQUEST,
  '__module__' : 'spaceone.api.monitoring.plugin.metric_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.plugin.MetricDataRequest)
  })
_sym_db.RegisterMessage(MetricDataRequest)

MetricInfo = _reflection.GeneratedProtocolMessageType('MetricInfo', (_message.Message,), {
  'DESCRIPTOR' : _METRICINFO,
  '__module__' : 'spaceone.api.monitoring.plugin.metric_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.plugin.MetricInfo)
  })
_sym_db.RegisterMessage(MetricInfo)

MetricsInfo = _reflection.GeneratedProtocolMessageType('MetricsInfo', (_message.Message,), {
  'DESCRIPTOR' : _METRICSINFO,
  '__module__' : 'spaceone.api.monitoring.plugin.metric_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.plugin.MetricsInfo)
  })
_sym_db.RegisterMessage(MetricsInfo)

MetricDataInfo = _reflection.GeneratedProtocolMessageType('MetricDataInfo', (_message.Message,), {
  'DESCRIPTOR' : _METRICDATAINFO,
  '__module__' : 'spaceone.api.monitoring.plugin.metric_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.plugin.MetricDataInfo)
  })
_sym_db.RegisterMessage(MetricDataInfo)

PluginMetricsResponse = _reflection.GeneratedProtocolMessageType('PluginMetricsResponse', (_message.Message,), {
  'DESCRIPTOR' : _PLUGINMETRICSRESPONSE,
  '__module__' : 'spaceone.api.monitoring.plugin.metric_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.plugin.PluginMetricsResponse)
  })
_sym_db.RegisterMessage(PluginMetricsResponse)

PluginMetricDataResponse = _reflection.GeneratedProtocolMessageType('PluginMetricDataResponse', (_message.Message,), {
  'DESCRIPTOR' : _PLUGINMETRICDATARESPONSE,
  '__module__' : 'spaceone.api.monitoring.plugin.metric_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.plugin.PluginMetricDataResponse)
  })
_sym_db.RegisterMessage(PluginMetricDataResponse)



_METRIC = _descriptor.ServiceDescriptor(
  name='Metric',
  full_name='spaceone.api.monitoring.plugin.Metric',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1271,
  serialized_end=1518,
  methods=[
  _descriptor.MethodDescriptor(
    name='list',
    full_name='spaceone.api.monitoring.plugin.Metric.list',
    index=0,
    containing_service=None,
    input_type=_METRICREQUEST,
    output_type=_PLUGINMETRICSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_data',
    full_name='spaceone.api.monitoring.plugin.Metric.get_data',
    index=1,
    containing_service=None,
    input_type=_METRICDATAREQUEST,
    output_type=_PLUGINMETRICDATARESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_METRIC)

DESCRIPTOR.services_by_name['Metric'] = _METRIC

# @@protoc_insertion_point(module_scope)
