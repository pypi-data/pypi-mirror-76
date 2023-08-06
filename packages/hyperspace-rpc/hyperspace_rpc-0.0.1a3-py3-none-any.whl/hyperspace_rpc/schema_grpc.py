from . import hrpc_pb2 as hrpc__pb2
import purerpc

from . import schema_pb2 as schema__pb2


class HyperspaceServicer(purerpc.Servicer):
    async def Status(self, input_message):
        raise NotImplementedError()

    @property
    def service(self) -> purerpc.Service:
        service_obj = purerpc.Service("hyperspace.Hyperspace")
        service_obj.add_method(
            "Status",
            self.Status,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                hrpc__pb2.Void,
                schema__pb2.HyperspaceStatusResponse,
            ),
        )
        return service_obj


class HyperspaceStub:
    def __init__(self, channel):
        self._client = purerpc.Client("hyperspace.Hyperspace", channel)
        self.Status = self._client.get_method_stub(
            "Status",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                hrpc__pb2.Void,
                schema__pb2.HyperspaceStatusResponse,
            ),
        )


class CorestoreServicer(purerpc.Servicer):
    async def Open(self, input_message):
        raise NotImplementedError()

    async def OnFeed(self, input_message):
        raise NotImplementedError()

    @property
    def service(self) -> purerpc.Service:
        service_obj = purerpc.Service("hyperspace.Corestore")
        service_obj.add_method(
            "Open",
            self.Open,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.OpenRequest,
                schema__pb2.OpenResponse,
            ),
        )
        service_obj.add_method(
            "OnFeed",
            self.OnFeed,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.FeedEvent,
                hrpc__pb2.Void,
            ),
        )
        return service_obj


class CorestoreStub:
    def __init__(self, channel):
        self._client = purerpc.Client("hyperspace.Corestore", channel)
        self.Open = self._client.get_method_stub(
            "Open",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.OpenRequest,
                schema__pb2.OpenResponse,
            ),
        )
        self.OnFeed = self._client.get_method_stub(
            "OnFeed",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.FeedEvent,
                hrpc__pb2.Void,
            ),
        )


class HypercoreServicer(purerpc.Servicer):
    async def Get(self, input_message):
        raise NotImplementedError()

    async def Append(self, input_message):
        raise NotImplementedError()

    async def Update(self, input_message):
        raise NotImplementedError()

    async def Seek(self, input_message):
        raise NotImplementedError()

    async def Has(self, input_message):
        raise NotImplementedError()

    async def Cancel(self, input_message):
        raise NotImplementedError()

    async def Download(self, input_message):
        raise NotImplementedError()

    async def Downloaded(self, input_message):
        raise NotImplementedError()

    async def Undownload(self, input_message):
        raise NotImplementedError()

    async def Close(self, input_message):
        raise NotImplementedError()

    async def RegisterExtension(self, input_message):
        raise NotImplementedError()

    async def UnregisterExtension(self, input_message):
        raise NotImplementedError()

    async def SendExtension(self, input_message):
        raise NotImplementedError()

    async def AcquireLock(self, input_message):
        raise NotImplementedError()

    async def ReleaseLock(self, input_message):
        raise NotImplementedError()

    async def OnAppend(self, input_message):
        raise NotImplementedError()

    async def OnClose(self, input_message):
        raise NotImplementedError()

    async def OnPeerOpen(self, input_message):
        raise NotImplementedError()

    async def OnPeerRemove(self, input_message):
        raise NotImplementedError()

    async def OnExtension(self, input_message):
        raise NotImplementedError()

    async def OnWait(self, input_message):
        raise NotImplementedError()

    @property
    def service(self) -> purerpc.Service:
        service_obj = purerpc.Service("hyperspace.Hypercore")
        service_obj.add_method(
            "Get",
            self.Get,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.GetRequest,
                schema__pb2.GetResponse,
            ),
        )
        service_obj.add_method(
            "Append",
            self.Append,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.AppendRequest,
                schema__pb2.AppendResponse,
            ),
        )
        service_obj.add_method(
            "Update",
            self.Update,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.UpdateRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "Seek",
            self.Seek,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.SeekRequest,
                schema__pb2.SeekResponse,
            ),
        )
        service_obj.add_method(
            "Has",
            self.Has,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.HasRequest,
                schema__pb2.HasResponse,
            ),
        )
        service_obj.add_method(
            "Cancel",
            self.Cancel,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.CancelRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "Download",
            self.Download,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.DownloadRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "Downloaded",
            self.Downloaded,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.DownloadedRequest,
                schema__pb2.DownloadedResponse,
            ),
        )
        service_obj.add_method(
            "Undownload",
            self.Undownload,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.UndownloadRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "Close",
            self.Close,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.CloseRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "RegisterExtension",
            self.RegisterExtension,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.RegisterExtensionRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "UnregisterExtension",
            self.UnregisterExtension,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.UnregisterExtensionRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "SendExtension",
            self.SendExtension,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.ExtensionMessage,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "AcquireLock",
            self.AcquireLock,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.LockRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "ReleaseLock",
            self.ReleaseLock,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.LockRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "OnAppend",
            self.OnAppend,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.AppendEvent,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "OnClose",
            self.OnClose,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.CloseEvent,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "OnPeerOpen",
            self.OnPeerOpen,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.PeerEvent,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "OnPeerRemove",
            self.OnPeerRemove,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.PeerEvent,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "OnExtension",
            self.OnExtension,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.ExtensionMessage,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "OnWait",
            self.OnWait,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.WaitEvent,
                hrpc__pb2.Void,
            ),
        )
        return service_obj


class HypercoreStub:
    def __init__(self, channel):
        self._client = purerpc.Client("hyperspace.Hypercore", channel)
        self.Get = self._client.get_method_stub(
            "Get",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.GetRequest,
                schema__pb2.GetResponse,
            ),
        )
        self.Append = self._client.get_method_stub(
            "Append",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.AppendRequest,
                schema__pb2.AppendResponse,
            ),
        )
        self.Update = self._client.get_method_stub(
            "Update",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.UpdateRequest,
                hrpc__pb2.Void,
            ),
        )
        self.Seek = self._client.get_method_stub(
            "Seek",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.SeekRequest,
                schema__pb2.SeekResponse,
            ),
        )
        self.Has = self._client.get_method_stub(
            "Has",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.HasRequest,
                schema__pb2.HasResponse,
            ),
        )
        self.Cancel = self._client.get_method_stub(
            "Cancel",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.CancelRequest,
                hrpc__pb2.Void,
            ),
        )
        self.Download = self._client.get_method_stub(
            "Download",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.DownloadRequest,
                hrpc__pb2.Void,
            ),
        )
        self.Downloaded = self._client.get_method_stub(
            "Downloaded",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.DownloadedRequest,
                schema__pb2.DownloadedResponse,
            ),
        )
        self.Undownload = self._client.get_method_stub(
            "Undownload",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.UndownloadRequest,
                hrpc__pb2.Void,
            ),
        )
        self.Close = self._client.get_method_stub(
            "Close",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.CloseRequest,
                hrpc__pb2.Void,
            ),
        )
        self.RegisterExtension = self._client.get_method_stub(
            "RegisterExtension",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.RegisterExtensionRequest,
                hrpc__pb2.Void,
            ),
        )
        self.UnregisterExtension = self._client.get_method_stub(
            "UnregisterExtension",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.UnregisterExtensionRequest,
                hrpc__pb2.Void,
            ),
        )
        self.SendExtension = self._client.get_method_stub(
            "SendExtension",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.ExtensionMessage,
                hrpc__pb2.Void,
            ),
        )
        self.AcquireLock = self._client.get_method_stub(
            "AcquireLock",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.LockRequest,
                hrpc__pb2.Void,
            ),
        )
        self.ReleaseLock = self._client.get_method_stub(
            "ReleaseLock",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.LockRequest,
                hrpc__pb2.Void,
            ),
        )
        self.OnAppend = self._client.get_method_stub(
            "OnAppend",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.AppendEvent,
                hrpc__pb2.Void,
            ),
        )
        self.OnClose = self._client.get_method_stub(
            "OnClose",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.CloseEvent,
                hrpc__pb2.Void,
            ),
        )
        self.OnPeerOpen = self._client.get_method_stub(
            "OnPeerOpen",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.PeerEvent,
                hrpc__pb2.Void,
            ),
        )
        self.OnPeerRemove = self._client.get_method_stub(
            "OnPeerRemove",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.PeerEvent,
                hrpc__pb2.Void,
            ),
        )
        self.OnExtension = self._client.get_method_stub(
            "OnExtension",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.ExtensionMessage,
                hrpc__pb2.Void,
            ),
        )
        self.OnWait = self._client.get_method_stub(
            "OnWait",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.WaitEvent,
                hrpc__pb2.Void,
            ),
        )


class NetworkServicer(purerpc.Servicer):
    async def Open(self, input_message):
        raise NotImplementedError()

    async def Configure(self, input_message):
        raise NotImplementedError()

    async def Status(self, input_message):
        raise NotImplementedError()

    async def AllStatuses(self, input_message):
        raise NotImplementedError()

    async def RegisterExtension(self, input_message):
        raise NotImplementedError()

    async def UnregisterExtension(self, input_message):
        raise NotImplementedError()

    async def SendExtension(self, input_message):
        raise NotImplementedError()

    async def OnPeerAdd(self, input_message):
        raise NotImplementedError()

    async def OnPeerRemove(self, input_message):
        raise NotImplementedError()

    async def OnExtension(self, input_message):
        raise NotImplementedError()

    @property
    def service(self) -> purerpc.Service:
        service_obj = purerpc.Service("hyperspace.Network")
        service_obj.add_method(
            "Open",
            self.Open,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                hrpc__pb2.Void,
                schema__pb2.OpenNetworkResponse,
            ),
        )
        service_obj.add_method(
            "Configure",
            self.Configure,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.ConfigureNetworkRequest,
                schema__pb2.NetworkStatusResponse,
            ),
        )
        service_obj.add_method(
            "Status",
            self.Status,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.NetworkStatusRequest,
                schema__pb2.NetworkStatusResponse,
            ),
        )
        service_obj.add_method(
            "AllStatuses",
            self.AllStatuses,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                hrpc__pb2.Void,
                schema__pb2.AllNetworkStatusesResponse,
            ),
        )
        service_obj.add_method(
            "RegisterExtension",
            self.RegisterExtension,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.RegisterExtensionRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "UnregisterExtension",
            self.UnregisterExtension,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.UnregisterExtensionRequest,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "SendExtension",
            self.SendExtension,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.ExtensionMessage,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "OnPeerAdd",
            self.OnPeerAdd,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.PeerEvent,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "OnPeerRemove",
            self.OnPeerRemove,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.PeerEvent,
                hrpc__pb2.Void,
            ),
        )
        service_obj.add_method(
            "OnExtension",
            self.OnExtension,
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.ExtensionMessage,
                hrpc__pb2.Void,
            ),
        )
        return service_obj


class NetworkStub:
    def __init__(self, channel):
        self._client = purerpc.Client("hyperspace.Network", channel)
        self.Open = self._client.get_method_stub(
            "Open",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                hrpc__pb2.Void,
                schema__pb2.OpenNetworkResponse,
            ),
        )
        self.Configure = self._client.get_method_stub(
            "Configure",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.ConfigureNetworkRequest,
                schema__pb2.NetworkStatusResponse,
            ),
        )
        self.Status = self._client.get_method_stub(
            "Status",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.NetworkStatusRequest,
                schema__pb2.NetworkStatusResponse,
            ),
        )
        self.AllStatuses = self._client.get_method_stub(
            "AllStatuses",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                hrpc__pb2.Void,
                schema__pb2.AllNetworkStatusesResponse,
            ),
        )
        self.RegisterExtension = self._client.get_method_stub(
            "RegisterExtension",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.RegisterExtensionRequest,
                hrpc__pb2.Void,
            ),
        )
        self.UnregisterExtension = self._client.get_method_stub(
            "UnregisterExtension",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.UnregisterExtensionRequest,
                hrpc__pb2.Void,
            ),
        )
        self.SendExtension = self._client.get_method_stub(
            "SendExtension",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.ExtensionMessage,
                hrpc__pb2.Void,
            ),
        )
        self.OnPeerAdd = self._client.get_method_stub(
            "OnPeerAdd",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.PeerEvent,
                hrpc__pb2.Void,
            ),
        )
        self.OnPeerRemove = self._client.get_method_stub(
            "OnPeerRemove",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.PeerEvent,
                hrpc__pb2.Void,
            ),
        )
        self.OnExtension = self._client.get_method_stub(
            "OnExtension",
            purerpc.RPCSignature(
                purerpc.Cardinality.UNARY_UNARY,
                schema__pb2.ExtensionMessage,
                hrpc__pb2.Void,
            ),
        )
