# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.identity.v1 import api_key_pb2 as spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2


class APIKeyStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.identity.v1.APIKey/create',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.CreateAPIKeyRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
                )
        self.enable = channel.unary_unary(
                '/spaceone.api.identity.v1.APIKey/enable',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
                )
        self.disable = channel.unary_unary(
                '/spaceone.api.identity.v1.APIKey/disable',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
                )
        self.update_role = channel.unary_unary(
                '/spaceone.api.identity.v1.APIKey/update_role',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.UpdateAPIKeyRoleRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
                )
        self.update_allowed_hosts = channel.unary_unary(
                '/spaceone.api.identity.v1.APIKey/update_allowed_hosts',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.UpdateAPIKeyHostsRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.identity.v1.APIKey/delete',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.identity.v1.APIKey/get',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.GetAPIKeyRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.identity.v1.APIKey/list',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeysInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.identity.v1.APIKey/stat',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class APIKeyServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_role(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_allowed_hosts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_APIKeyServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.CreateAPIKeyRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.SerializeToString,
            ),
            'enable': grpc.unary_unary_rpc_method_handler(
                    servicer.enable,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.SerializeToString,
            ),
            'disable': grpc.unary_unary_rpc_method_handler(
                    servicer.disable,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.SerializeToString,
            ),
            'update_role': grpc.unary_unary_rpc_method_handler(
                    servicer.update_role,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.UpdateAPIKeyRoleRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.SerializeToString,
            ),
            'update_allowed_hosts': grpc.unary_unary_rpc_method_handler(
                    servicer.update_allowed_hosts,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.UpdateAPIKeyHostsRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.GetAPIKeyRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeysInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.identity.v1.APIKey', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class APIKey(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.APIKey/create',
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.CreateAPIKeyRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def enable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.APIKey/enable',
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def disable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.APIKey/disable',
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_role(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.APIKey/update_role',
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.UpdateAPIKeyRoleRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_allowed_hosts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.APIKey/update_allowed_hosts',
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.UpdateAPIKeyHostsRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.APIKey/delete',
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.APIKey/get',
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.GetAPIKeyRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.APIKey/list',
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyQuery.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeysInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.APIKey/stat',
            spaceone_dot_api_dot_identity_dot_v1_dot_api__key__pb2.APIKeyStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
