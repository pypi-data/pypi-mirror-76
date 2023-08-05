# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from chirpstack_api.as_pb.external.api import deviceQueue_pb2 as chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class DeviceQueueServiceStub(object):
    """DeviceQueueService is the service managing the downlink data queue.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Enqueue = channel.unary_unary(
                '/api.DeviceQueueService/Enqueue',
                request_serializer=chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.EnqueueDeviceQueueItemRequest.SerializeToString,
                response_deserializer=chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.EnqueueDeviceQueueItemResponse.FromString,
                )
        self.Flush = channel.unary_unary(
                '/api.DeviceQueueService/Flush',
                request_serializer=chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.FlushDeviceQueueRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.List = channel.unary_unary(
                '/api.DeviceQueueService/List',
                request_serializer=chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.ListDeviceQueueItemsRequest.SerializeToString,
                response_deserializer=chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.ListDeviceQueueItemsResponse.FromString,
                )


class DeviceQueueServiceServicer(object):
    """DeviceQueueService is the service managing the downlink data queue.
    """

    def Enqueue(self, request, context):
        """Enqueue adds the given item to the device-queue.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Flush(self, request, context):
        """Flush flushes the downlink device-queue.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """List lists the items in the device-queue.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DeviceQueueServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Enqueue': grpc.unary_unary_rpc_method_handler(
                    servicer.Enqueue,
                    request_deserializer=chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.EnqueueDeviceQueueItemRequest.FromString,
                    response_serializer=chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.EnqueueDeviceQueueItemResponse.SerializeToString,
            ),
            'Flush': grpc.unary_unary_rpc_method_handler(
                    servicer.Flush,
                    request_deserializer=chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.FlushDeviceQueueRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.ListDeviceQueueItemsRequest.FromString,
                    response_serializer=chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.ListDeviceQueueItemsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'api.DeviceQueueService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DeviceQueueService(object):
    """DeviceQueueService is the service managing the downlink data queue.
    """

    @staticmethod
    def Enqueue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.DeviceQueueService/Enqueue',
            chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.EnqueueDeviceQueueItemRequest.SerializeToString,
            chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.EnqueueDeviceQueueItemResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Flush(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.DeviceQueueService/Flush',
            chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.FlushDeviceQueueRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/api.DeviceQueueService/List',
            chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.ListDeviceQueueItemsRequest.SerializeToString,
            chirpstack__api_dot_as__pb_dot_external_dot_api_dot_deviceQueue__pb2.ListDeviceQueueItemsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
