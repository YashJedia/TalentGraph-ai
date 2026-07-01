from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base class for backend AI agents."""

    @abstractmethod
    async def run(self, *args, **kwargs):
        raise NotImplementedError
