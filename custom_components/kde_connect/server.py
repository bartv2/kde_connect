from logging import DEBUG, INFO, WARNING, basicConfig, getLogger, info
from os import makedirs
from os.path import expanduser, expandvars, join
from uuid import uuid4

from OpenSSL.crypto import Error
from twisted.internet import reactor
from twisted.web.server import Site

from konnect import __version__
from konnect.api import API
from konnect.certificate import Certificate
from konnect.database import Database
from konnect.factories import KonnectFactory
from konnect.protocols import Discovery
from homeassistant.core import HomeAssistant


def start(hass: HomeAssistant, args):
    level = DEBUG if args.debug else INFO

    format_ = "%(levelname)s %(message)s"

    if args.timestamps:
        format_ = "%(asctime)s " + format_

        basicConfig(format=format_, level=level)

        getLogger("PIL").setLevel(WARNING)

        args.config_dir = expanduser(expandvars(args.config_dir))
        makedirs(args.config_dir, exist_ok=True)
        database = Database(join(args.config_dir, "konnect.db"))

        try:
            options = Certificate.load_options(args.config_dir)
            identifier = Certificate.extract_identifier(options)
        except (FileNotFoundError, Error):
            identifier = str(uuid4()).replace("-", "")
            Certificate.generate(identifier, args.config_dir)
            options = Certificate.load_options(args.config_dir)

        konnect = KonnectFactory(database, identifier, args.name, options)
        discovery = Discovery(identifier, args.name, args.service_port)

        info(f"Starting Konnectd {__version__} as {args.name}")

        reactor.listenTCP(args.service_port, konnect, interface="0.0.0.0")
        reactor.listenUDP(args.discovery_port, discovery, interface="0.0.0.0")
        site = Site(API(konnect, discovery, database, args.debug))

        if args.admin_port.isdigit():
            reactor.listenTCP(int(args.admin_port), site, interface="127.0.0.1")
        else:
            reactor.listenUNIX(expanduser(expandvars(args.admin_port)), site)
        return konnect
