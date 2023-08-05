#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

""" the global configuration """

import os
from ast import literal_eval

# pylint: disable=invalid-name
DEFAULT_KAFKA_BOOTSTRAP_SERVER = "10.14.0.23:9092"
DEFAULT_KAFKA_LOG_TOPIC = "titan.logs"
DEFAULT_GRIDMANAGER_ADDRESS = "http://localhost:8080/gridmanager"
DEFAULT_FLOWMANAGER_ADDRESS = "http://localhost:9002/flowmanager"
DEFAULT_PACKAGEMANAGER_ADDRESS = "http://localhost:8087/packagemanager"
DEFAULT_REPOSERVICE_ADDRESS = "http://localhost:8085/object"


# pylint: disable=too-few-public-methods
class Configuration:
    """Current Configuration"""
    kafka_bootstrap_servers = DEFAULT_KAFKA_BOOTSTRAP_SERVER
    kafka_log_topic = DEFAULT_KAFKA_LOG_TOPIC

    no_kafka_today = literal_eval(
        os.getenv("TITAN_METRICS_DISABLED") or os.getenv("TITANFE_WITHOUT_KAFKA") or "False"
    )

    gridmanager_address = DEFAULT_GRIDMANAGER_ADDRESS
    flowmanager_address = DEFAULT_FLOWMANAGER_ADDRESS
    packagemanager_address = DEFAULT_PACKAGEMANAGER_ADDRESS
    reposervice_address = DEFAULT_REPOSERVICE_ADDRESS
    IP = None
    controlpeer_address = None

    @classmethod
    def update(cls, config: dict):
        """update config from dict"""
        config_keys = {
            "GridManager": "gridmanager_address",
            "FlowManager": "flowmanager_address",
            "PackageManager": "packagemanager_address",
            "RepositoryService": "reposervice_address",
            "ControlPeer": "controlpeer_address",
            "IP": "IP",
            "Kafka": "kafka_bootstrap_servers",
            "KafkaLogTopic": "kafka_log_topic"
        }

        for key, target in config_keys.items():
            if key in config:
                setattr(cls, target, config[key])


configuration = Configuration()
