from abc import ABC, abstractmethod
from typing import Any


class StreamConnection(ABC):

    @abstractmethod
    def identity(self) -> str:
        """
        The connection identity
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def inbound_stream(self) -> Any:
        """
        TODO: generify
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def outbound_stream(self) -> Any:
        """
        TODO: generify
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def closed_count(self) -> int:
        """
        :return: the amount of closed underlying streams (at max 2)
        """
        raise NotImplementedError()

    @abstractmethod
    def close_inbound(self):
        """
        Closes the inbound side of the stream
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def close_outbound(self):
        """
        Closes the outbound side of the stream
        :return:
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return "StreamConnection(identity={}, closed_count={}" \
            .format(self.identity(), self.closed_count())
