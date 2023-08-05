# -*- coding: utf-8 -*-
#
# Copyright 2020 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Service logger."""
import logging.config

import yaml

from renku.service.config import LOGGER_CONFIG_FILE

config = yaml.safe_load(LOGGER_CONFIG_FILE.read_text())
logging.config.dictConfig(config)

service_log = logging.getLogger("renku.service")
worker_log = logging.getLogger("renku.worker")
scheduler_log = logging.getLogger("renku.scheduler")

__all__ = [
    "service_log",
    "worker_log",
    "scheduler_log",
]
