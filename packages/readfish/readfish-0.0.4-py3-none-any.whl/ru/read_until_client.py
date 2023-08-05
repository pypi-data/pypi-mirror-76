import logging

from read_until import ReadUntilClient


class Client(ReadUntilClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set our extension here
        # TODO: unblock logger
        # TODO: message port?
        # TODO: wait for acquisition
        # Don't bother writing to data dir
        #

    def unblock_read(self, read_channel, read_number, duration=0.1):
        super().unblock_read(
            read_channel=read_channel, read_number=read_number, duration=duration,
        )
        # Log read id of unblocked read
