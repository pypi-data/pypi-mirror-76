import time

from channels.db import database_sync_to_async
from pydantic import HttpUrl
from pydantic.dataclasses import dataclass


class PydanticConfig:
    arbitrary_types_allowed = True


def Service(cls):
    if hasattr(cls, "result"):
        raise TypeError("service must not have result as a field")

    # def __post_init_post_parse__(self) -> None:
    #     """Overwrite self.accuracy with a mapping as defined below."""
    #     if hasattr(self, 'process'):
    #         time_start = time.time()
    #         self.result = self.process()
    #         self.runtime = time.time() - time_start
    #     if hasattr(self, 'post_process'):
    #         self.process()

    def process(self):
        raise NotImplementedError

    def post_process(self):
        raise NotImplementedError

    @classmethod
    def execute(cls, **inputs):
        """
        Function to be called from the outside to kick off the Service
        functionality.
        :param dictionary inputs: data parameters for Service, checked
            against the fields defined on the Service class.
        :param dictionary files: usually request's FILES dictionary or
            None.
        :param dictionary **kwargs: any additional parameters Service may
            need, can be an empty dictionary
        """
        instance = cls(**inputs)
        if hasattr(instance, "process"):
            time_start = time.time()
            result = instance.process()
            instance.runtime = time.time() - time_start
            return result
        if hasattr(instance, "post_process"):
            instance.post_process()

    @classmethod
    async def execute_threaded(cls, **inputs):
        instance = cls(**inputs)
        if hasattr(instance, "process"):
            time_start = time.time()
            result = await database_sync_to_async(instance.process)()
            instance.runtime = time.time() - time_start
            return result
        if hasattr(instance, "post_process"):
            database_sync_to_async(instance.post_process)()

    # setattr(cls, '__post_init_post_parse__', __post_init_post_parse__)
    setattr(cls, "execute", execute)
    setattr(cls, "execute_threaded", execute_threaded)

    if not hasattr(cls, "process"):
        setattr(cls, "process", process)
    # setattr(cls, 'post_process', post_process)
    return dataclass(config=PydanticConfig)(cls)


# async
# threaded
# cached(?)
# on error - TypeError, ValidationError
