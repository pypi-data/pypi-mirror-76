# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains the behaviour of a generic seller AEA."""

import json
from typing import Dict, cast

from aea.mail.base import EnvelopeContext
from aea.skills.behaviours import TickerBehaviour

from packages.fetchai.connections.http_client.connection import (
    PUBLIC_ID as HTTP_CLIENT_CONNECTION_PUBLIC_ID,
)
from packages.fetchai.protocols.http.message import HttpMessage
from packages.fetchai.protocols.oef_search.message import OefSearchMessage
from packages.fetchai.skills.aries_alice.dialogues import (
    HttpDialogues,
    OefSearchDialogues,
)
from packages.fetchai.skills.aries_alice.strategy import (
    AliceStrategy,
    HTTP_COUNTERPARTY,
)

DEFAULT_SERVICES_INTERVAL = 60.0


class AliceBehaviour(TickerBehaviour):
    """This class implements a behaviour."""

    def __init__(self, **kwargs):
        """Initialise the behaviour."""

        services_interval = kwargs.pop(
            "services_interval", DEFAULT_SERVICES_INTERVAL
        )  # type: int
        super().__init__(tick_interval=services_interval, **kwargs)

    def send_http_request_message(
        self, method: str, url: str, content: Dict = None
    ) -> None:
        """
        Send an http request message.

        :param method: the http request method (i.e. 'GET' or 'POST').
        :param url: the url to send the message to.
        :param content: the payload.

        :return: None
        """
        # context
        http_dialogues = cast(HttpDialogues, self.context.http_dialogues)

        # http request message
        request_http_message = HttpMessage(
            dialogue_reference=http_dialogues.new_self_initiated_dialogue_reference(),
            performative=HttpMessage.Performative.REQUEST,
            method=method,
            url=url,
            headers="",
            version="",
            bodyy=b"" if content is None else json.dumps(content).encode("utf-8"),
        )
        request_http_message.counterparty = HTTP_COUNTERPARTY

        # http dialogue
        http_dialogue = http_dialogues.update(request_http_message)
        assert (
            http_dialogue is not None
        ), "alice -> behaviour -> send_http_request_message(): something went wrong when sending a HTTP message."

        # send
        self.context.outbox.put_message(
            message=request_http_message,
            context=EnvelopeContext(connection_id=HTTP_CLIENT_CONNECTION_PUBLIC_ID),
        )

    def setup(self) -> None:
        """
        Implement the setup.

        :return: None
        """
        self.context.logger.info("My address is: " + self.context.agent_address)
        self._register_agent()
        self._register_service()

    def act(self) -> None:
        """
        Implement the act.

        :return: None
        """

    def teardown(self) -> None:
        """
        Implement the task teardown.

        :return: None
        """
        self._unregister_service()
        self._unregister_agent()

    def _register_agent(self) -> None:
        """
        Register the agent's location.

        :return: None
        """
        strategy = cast(AliceStrategy, self.context.strategy)
        description = strategy.get_location_description()
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg = OefSearchMessage(
            performative=OefSearchMessage.Performative.REGISTER_SERVICE,
            dialogue_reference=oef_search_dialogues.new_self_initiated_dialogue_reference(),
            service_description=description,
        )
        oef_search_msg.counterparty = self.context.search_service_address
        oef_dialogue = oef_search_dialogues.update(oef_search_msg)
        assert (
            oef_dialogue is not None
        ), "alice -> behaviour -> _register_agent(): something went wrong when registering Alice on SOEF."
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("registering Alice on SOEF.")

    def _register_service(self) -> None:
        """
        Register the agent's service.

        :return: None
        """
        strategy = cast(AliceStrategy, self.context.strategy)
        description = strategy.get_register_service_description()
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg = OefSearchMessage(
            performative=OefSearchMessage.Performative.REGISTER_SERVICE,
            dialogue_reference=oef_search_dialogues.new_self_initiated_dialogue_reference(),
            service_description=description,
        )
        oef_search_msg.counterparty = self.context.search_service_address
        oef_dialogue = oef_search_dialogues.update(oef_search_msg)
        assert (
            oef_dialogue is not None
        ), "alice -> behaviour -> _register_service(): something went wrong when registering Alice service on SOEF."
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("registering Alice service on SOEF.")

    def _unregister_service(self) -> None:
        """
        Unregister service from the SOEF.

        :return: None
        """
        strategy = cast(AliceStrategy, self.context.strategy)
        description = strategy.get_unregister_service_description()
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg = OefSearchMessage(
            performative=OefSearchMessage.Performative.UNREGISTER_SERVICE,
            dialogue_reference=oef_search_dialogues.new_self_initiated_dialogue_reference(),
            service_description=description,
        )
        oef_search_msg.counterparty = self.context.search_service_address
        oef_dialogue = oef_search_dialogues.update(oef_search_msg)
        assert (
            oef_dialogue is not None
        ), "alice -> behaviour -> _unregister_service(): something went wrong when unregistering Alice service on SOEF."
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("unregistering service from SOEF.")

    def _unregister_agent(self) -> None:
        """
        Unregister agent from the SOEF.

        :return: None
        """
        strategy = cast(AliceStrategy, self.context.strategy)
        description = strategy.get_location_description()
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg = OefSearchMessage(
            performative=OefSearchMessage.Performative.UNREGISTER_SERVICE,
            dialogue_reference=oef_search_dialogues.new_self_initiated_dialogue_reference(),
            service_description=description,
        )
        oef_search_msg.counterparty = self.context.search_service_address
        oef_dialogue = oef_search_dialogues.update(oef_search_msg)
        assert (
            oef_dialogue is not None
        ), "alice -> behaviour -> _unregister_agent(): something went wrong when unregistering Alice on SOEF."
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("unregistering agent from SOEF.")
