#!/usr/bin/env python3
import sys

import connexion
import pika

from swagger_server import encoder
from swagger_server import config
from swagger_server import pika_dispatcher

from kazoo.client import KazooClient


def main():
    # Generate personal id
    config.Config.generate_frontend_id()

    config.Config.initialize_parameters()
    pika_dispatcher.start_pika_dispatcher()
    
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Scooter API'})
    app.run(port=8080)


if __name__ == '__main__':
    main()
