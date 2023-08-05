# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.identity.v1 import user_pb2 as spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2


class UserStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.identity.v1.User/create',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.CreateUserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.identity.v1.User/update',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UpdateUserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
                )
        self.enable = channel.unary_unary(
                '/spaceone.api.identity.v1.User/enable',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
                )
        self.disable = channel.unary_unary(
                '/spaceone.api.identity.v1.User/disable',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
                )
        self.update_role = channel.unary_unary(
                '/spaceone.api.identity.v1.User/update_role',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UpdateUserRoleRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.identity.v1.User/delete',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.identity.v1.User/get',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.GetUserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.identity.v1.User/list',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UsersInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.identity.v1.User/stat',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )
        self.find = channel.unary_unary(
                '/spaceone.api.identity.v1.User/find',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.FindUserQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.FindUsersInfo.FromString,
                )
        self.sync = channel.unary_unary(
                '/spaceone.api.identity.v1.User/sync',
                request_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
                )


class UserServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """
        desc: Update user info by given user_id
        note:
        request_example: >-
        {
        "user_id": "dkang@mz.co.kr",
        "tags": {
        "user1": "Reuters",
        "user2": "Bloomberg"
        },
        "domain_id": "{{DOMAIN_ID}}"
        }
        response_example: >-
        {
        "roles": [],
        "user_id": "dkang@mz.co.kr",
        "name": "Dong Yoo kang",
        "state": "ENABLED",
        "email": "dkang@mz.co.kr",
        "mobile": "",
        "group": "",
        "language": "en",
        "timezone": "UTC",
        "tags": {
        "user1": "Reuters",
        "user2": "Bloomberg"
        },
        "last_accessed_at": {
        "seconds": "1593161630",
        "nanos": 79000000
        },
        "created_at": {
        "seconds": "1593161630",
        "nanos": 79000000
        },
        "domain_id": "domain-fd6e23a5ae36"
        }
        """
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

    def find(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sync(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.CreateUserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UpdateUserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'enable': grpc.unary_unary_rpc_method_handler(
                    servicer.enable,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'disable': grpc.unary_unary_rpc_method_handler(
                    servicer.disable,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'update_role': grpc.unary_unary_rpc_method_handler(
                    servicer.update_role,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UpdateUserRoleRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.GetUserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UsersInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
            'find': grpc.unary_unary_rpc_method_handler(
                    servicer.find,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.FindUserQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.FindUsersInfo.SerializeToString,
            ),
            'sync': grpc.unary_unary_rpc_method_handler(
                    servicer.sync,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.identity.v1.User', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class User(object):
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/create',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.CreateUserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/update',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UpdateUserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/enable',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/disable',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/update_role',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UpdateUserRoleRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/delete',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.SerializeToString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/get',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.GetUserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/list',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserQuery.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UsersInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/stat',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def find(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/find',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.FindUserQuery.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.FindUsersInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def sync(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v1.User/sync',
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v1_dot_user__pb2.UserInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
