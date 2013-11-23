"""
Initialize and teardown fake HTTP services for use in acceptance tests.
"""

from lettuce import before, after, world
from django.conf import settings
from terrain.stubs.youtube import StubYouTubeService
from terrain.stubs.xqueue import StubXQueueService


USAGE = "USAGE: python -m fakes.start SERVICE_NAME PORT_NUM"

# Map service names to classes
SERVICES = {
    "youtube": {"port": settings.YOUTUBE_PORT, "class": StubYouTubeService},
    "xqueue": {"port": settings.XQUEUE_PORT, "class": StubXQueueService},
}


@before.all
def start_fakes():
    """
    Start each fake service running on a local port.
    """
    for name, service in SERVICES.iteritems():
        fake_server = service['class'](port_num=service['port'])
        setattr(world, name, fake_server)


@after.all
def stop_fakes(_):
    """
    Shut down each fake service.
    """
    for name in SERVICES.keys():
        fake_server = getattr(world, name, None)
        if fake_server is not None:
            fake_server.shutdown()
