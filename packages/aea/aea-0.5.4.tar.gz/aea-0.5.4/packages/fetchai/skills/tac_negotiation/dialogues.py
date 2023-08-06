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

"""
This module contains the classes required for dialogue management.

- Dialogues: The dialogues class keeps track of all dialogues.
"""

from typing import Optional, cast

from aea.helpers.dialogue.base import Dialogue, DialogueLabel
from aea.mail.base import Address
from aea.protocols.base import Message
from aea.protocols.default.dialogues import DefaultDialogue as BaseDefaultDialogue
from aea.protocols.default.dialogues import DefaultDialogues as BaseDefaultDialogues
from aea.protocols.signing.dialogues import SigningDialogue as BaseSigningDialogue
from aea.protocols.signing.dialogues import SigningDialogues as BaseSigningDialogues
from aea.skills.base import Model

from packages.fetchai.protocols.fipa.dialogues import FipaDialogue as BaseFipaDialogue
from packages.fetchai.protocols.fipa.dialogues import FipaDialogues as BaseFipaDialogues
from packages.fetchai.protocols.fipa.message import FipaMessage
from packages.fetchai.protocols.oef_search.dialogues import (
    OefSearchDialogue as BaseOefSearchDialogue,
)
from packages.fetchai.protocols.oef_search.dialogues import (
    OefSearchDialogues as BaseOefSearchDialogues,
)
from packages.fetchai.skills.tac_negotiation.helpers import (
    DEMAND_DATAMODEL_NAME,
    SUPPLY_DATAMODEL_NAME,
)


DefaultDialogue = BaseDefaultDialogue


class DefaultDialogues(Model, BaseDefaultDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs) -> None:
        """
        Initialize dialogues.

        :return: None
        """
        Model.__init__(self, **kwargs)
        BaseDefaultDialogues.__init__(self, self.context.agent_address)

    @staticmethod
    def role_from_first_message(message: Message) -> Dialogue.Role:
        """Infer the role of the agent from an incoming/outgoing first message

        :param message: an incoming/outgoing first message
        :return: The role of the agent
        """
        return DefaultDialogue.Role.AGENT

    def create_dialogue(
        self, dialogue_label: DialogueLabel, role: Dialogue.Role,
    ) -> DefaultDialogue:
        """
        Create an instance of fipa dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param role: the role of the agent this dialogue is maintained for

        :return: the created dialogue
        """
        dialogue = DefaultDialogue(
            dialogue_label=dialogue_label, agent_address=self.agent_address, role=role
        )
        return dialogue


FipaDialogue = BaseFipaDialogue


class FipaDialogues(Model, BaseFipaDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs) -> None:
        """
        Initialize dialogues.

        :return: None
        """
        Model.__init__(self, **kwargs)
        BaseFipaDialogues.__init__(self, self.context.agent_address)

    @staticmethod
    def role_from_first_message(message: Message) -> Dialogue.Role:
        """
        Infer the role of the agent from an incoming or outgoing first message

        :param message: an incoming/outgoing first message
        :return: the agent's role
        """
        fipa_message = cast(FipaMessage, message)
        if fipa_message.performative != FipaMessage.Performative.CFP:
            raise ValueError("First message must be a CFP!")
        query = fipa_message.query
        if query.model is None:
            raise ValueError("Query must have a data model!")
        if query.model.name not in [
            SUPPLY_DATAMODEL_NAME,
            DEMAND_DATAMODEL_NAME,
        ]:
            raise ValueError(
                "Query data model name must be in [{},{}]".format(
                    SUPPLY_DATAMODEL_NAME, DEMAND_DATAMODEL_NAME
                )
            )
        if message.is_incoming:
            is_seller = (
                query.model.name == SUPPLY_DATAMODEL_NAME
            )  # the counterparty is querying for supply/sellers (this agent is receiving their CFP so is the seller)
        else:
            is_seller = (
                query.model.name == DEMAND_DATAMODEL_NAME
            )  # the agent is querying for demand/buyers (this agent is sending the CFP so it is the seller)
        role = FipaDialogue.Role.SELLER if is_seller else FipaDialogue.Role.BUYER
        return role


class OefSearchDialogue(BaseOefSearchDialogue):
    """The dialogue class maintains state of a dialogue and manages it."""

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        agent_address: Address,
        role: Dialogue.Role,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param agent_address: the address of the agent for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for

        :return: None
        """
        BaseOefSearchDialogue.__init__(
            self, dialogue_label=dialogue_label, agent_address=agent_address, role=role
        )
        self._is_seller_search = None  # type: Optional[bool]

    @property
    def is_seller_search(self) -> bool:
        """Get if it is a seller search."""
        assert self._is_seller_search is not None, "is_seller_search not set!"
        return self._is_seller_search

    @is_seller_search.setter
    def is_seller_search(self, is_seller_search: bool) -> None:
        """Set is_seller_search."""
        assert self._is_seller_search is None, "is_seller_search already set!"
        self._is_seller_search = is_seller_search


class OefSearchDialogues(Model, BaseOefSearchDialogues):
    """This class keeps track of all oef_search dialogues."""

    def __init__(self, **kwargs) -> None:
        """
        Initialize dialogues.

        :param agent_address: the address of the agent for whom dialogues are maintained
        :return: None
        """
        Model.__init__(self, **kwargs)
        BaseOefSearchDialogues.__init__(
            self, self.context.agent_address + "_" + str(self.context.skill_id)
        )

    @staticmethod
    def role_from_first_message(message: Message) -> Dialogue.Role:
        """Infer the role of the agent from an incoming/outgoing first message

        :param message: an incoming/outgoing first message
        :return: The role of the agent
        """
        return BaseOefSearchDialogue.Role.AGENT

    def create_dialogue(
        self, dialogue_label: DialogueLabel, role: Dialogue.Role,
    ) -> OefSearchDialogue:
        """
        Create an instance of fipa dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param role: the role of the agent this dialogue is maintained for

        :return: the created dialogue
        """
        dialogue = OefSearchDialogue(
            dialogue_label=dialogue_label, agent_address=self.agent_address, role=role
        )
        return dialogue


SigningDialogue = BaseSigningDialogue


class SigningDialogues(Model, BaseSigningDialogues):
    """This class keeps track of all oef_search dialogues."""

    def __init__(self, **kwargs) -> None:
        """
        Initialize dialogues.

        :param agent_address: the address of the agent for whom dialogues are maintained
        :return: None
        """
        Model.__init__(self, **kwargs)
        BaseSigningDialogues.__init__(
            self, self.context.agent_address + "_" + str(self.context.skill_id)
        )

    @staticmethod
    def role_from_first_message(message: Message) -> Dialogue.Role:
        """Infer the role of the agent from an incoming/outgoing first message

        :param message: an incoming/outgoing first message
        :return: The role of the agent
        """
        return BaseSigningDialogue.Role.SKILL

    def create_dialogue(
        self, dialogue_label: DialogueLabel, role: Dialogue.Role,
    ) -> SigningDialogue:
        """
        Create an instance of fipa dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param role: the role of the agent this dialogue is maintained for

        :return: the created dialogue
        """
        dialogue = SigningDialogue(
            dialogue_label=dialogue_label, agent_address=self.agent_address, role=role
        )
        return dialogue
