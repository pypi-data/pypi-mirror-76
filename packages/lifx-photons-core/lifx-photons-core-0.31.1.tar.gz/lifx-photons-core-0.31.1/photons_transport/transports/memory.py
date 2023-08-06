from photons_transport.transports.base import Transport

import logging

log = logging.getLogger("photons_transport.transports.memory")


class Memory(Transport):
    """Knows how to send and receive messages with an in memory Fake device"""

    def setup(self, writer):
        self.writer = writer

    def clone_for(self, session):
        return self.__class__(session, self.writer)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.writer is self.writer

    async def is_transport_active(self, packet, transport):
        return True

    async def close_transport(self, transport):
        pass

    async def spawn_transport(self, timeout):
        return self.writer

    async def write(self, transport, bts, original_message):
        await self.writer(self.session.received_data, bts)
