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

"""This module contains the tests of the ethereum module."""
import logging
import time
from unittest import mock
from unittest.mock import MagicMock

import pytest

from aea.crypto.cosmos import CosmosApi, CosmosCrypto, CosmosFaucetApi

from tests.conftest import (
    COSMOS_PRIVATE_KEY_PATH,
    COSMOS_TESTNET_CONFIG,
    MAX_FLAKY_RERUNS,
)


def test_creation():
    """Test the creation of the crypto_objects."""
    assert CosmosCrypto(), "Did not manage to initialise the crypto module"
    assert CosmosCrypto(
        COSMOS_PRIVATE_KEY_PATH
    ), "Did not manage to load the cosmos private key"


def test_initialization():
    """Test the initialisation of the variables."""
    account = CosmosCrypto()
    assert account.entity is not None, "The property must return the account."
    assert (
        account.address is not None
    ), "After creation the display address must not be None"
    assert (
        account.public_key is not None
    ), "After creation the public key must no be None"


def test_sign_and_recover_message():
    """Test the signing and the recovery of a message."""
    account = CosmosCrypto(COSMOS_PRIVATE_KEY_PATH)
    sign_bytes = account.sign_message(message=b"hello")
    assert len(sign_bytes) > 0, "The len(signature) must not be 0"
    recovered_addresses = CosmosApi.recover_message(
        message=b"hello", signature=sign_bytes
    )
    assert (
        account.address in recovered_addresses
    ), "Failed to recover the correct address."


def test_get_hash():
    """Test the get hash functionality."""
    expected_hash = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    hash_ = CosmosApi.get_hash(message=b"hello")
    assert expected_hash == hash_


def test_dump_positive():
    """Test dump."""
    account = CosmosCrypto(COSMOS_PRIVATE_KEY_PATH)
    account.dump(MagicMock())


def test_api_creation():
    """Test api instantiation."""
    assert CosmosApi(**COSMOS_TESTNET_CONFIG), "Failed to initialise the api"


def test_api_none():
    """Test the "api" of the cryptoApi is none."""
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)
    assert cosmos_api.api is None, "The api property is not None."


def test_generate_nonce():
    """Test generate nonce."""
    nonce = CosmosApi.generate_tx_nonce(
        seller="some_seller_addr", client="some_buyer_addr"
    )
    assert len(nonce) > 0 and int(
        nonce, 16
    ), "The len(nonce) must not be 0 and must be hex"


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_construct_sign_and_submit_transfer_transaction():
    """Test the construction, signing and submitting of a transfer transaction."""
    account = CosmosCrypto()
    balance = get_wealth(account.address)
    assert balance > 0, "Failed to fund account."
    cc2 = CosmosCrypto()
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)

    amount = 10000
    assert amount < balance, "Not enough funds."
    transfer_transaction = cosmos_api.get_transfer_transaction(
        sender_address=account.address,
        destination_address=cc2.address,
        amount=amount,
        tx_fee=1000,
        tx_nonce="something",
    )
    assert (
        isinstance(transfer_transaction, dict) and len(transfer_transaction) == 6
    ), "Incorrect transfer_transaction constructed."

    signed_transaction = account.sign_transaction(transfer_transaction)
    assert (
        isinstance(signed_transaction, dict)
        and len(signed_transaction["tx"]) == 4
        and isinstance(signed_transaction["tx"]["signatures"], list)
    ), "Incorrect signed_transaction constructed."

    transaction_digest = cosmos_api.send_signed_transaction(signed_transaction)
    assert transaction_digest is not None, "Failed to submit transfer transaction!"

    not_settled = True
    elapsed_time = 0
    while not_settled and elapsed_time < 20:
        elapsed_time += 1
        time.sleep(2)
        transaction_receipt = cosmos_api.get_transaction_receipt(transaction_digest)
        if transaction_receipt is None:
            continue
        is_settled = cosmos_api.is_transaction_settled(transaction_receipt)
        not_settled = not is_settled
    assert transaction_receipt is not None, "Failed to retrieve transaction receipt."
    assert is_settled, "Failed to verify tx!"

    tx = cosmos_api.get_transaction(transaction_digest)
    is_valid = cosmos_api.is_transaction_valid(
        tx, cc2.address, account.address, "", amount
    )
    assert is_valid, "Failed to settle tx correctly!"
    assert tx == transaction_receipt, "Should be same!"


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_get_balance():
    """Test the balance is zero for a new account."""
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)
    cc = CosmosCrypto()
    balance = cosmos_api.get_balance(cc.address)
    assert balance == 0, "New account has a positive balance."
    balance = get_wealth(cc.address)
    assert balance > 0, "Existing account has no balance."


def get_wealth(address: str):
    """Get wealth for test."""
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)
    CosmosFaucetApi().get_wealth(address)
    balance = 0
    timeout = 0
    while timeout < 40 and balance == 0:
        time.sleep(1)
        timeout += 1
        _balance = cosmos_api.get_balance(address)
        balance = _balance if _balance is not None else 0
    return balance


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_get_wealth_positive(caplog):
    """Test the balance is zero for a new account."""
    with caplog.at_level(logging.DEBUG, logger="aea.crypto.cosmos"):
        cosmos_faucet_api = CosmosFaucetApi()
        cc = CosmosCrypto()
        cosmos_faucet_api.get_wealth(cc.address)
        assert "Wealth generated" in caplog.text


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_format_default():
    """Test if default CosmosSDK transaction is correctly formated."""
    account = CosmosCrypto()
    cc2 = CosmosCrypto()
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)

    amount = 10000

    transfer_transaction = cosmos_api.get_transfer_transaction(
        sender_address=account.address,
        destination_address=cc2.address,
        amount=amount,
        tx_fee=1000,
        tx_nonce="something",
    )

    signed_transaction = cc2.sign_transaction(transfer_transaction)

    assert "tx" in signed_transaction
    assert "signatures" in signed_transaction["tx"]
    assert len(signed_transaction["tx"]["signatures"]) == 1

    assert "pub_key" in signed_transaction["tx"]["signatures"][0]
    assert "value" in signed_transaction["tx"]["signatures"][0]["pub_key"]
    base64_pbk = signed_transaction["tx"]["signatures"][0]["pub_key"]["value"]

    assert "signature" in signed_transaction["tx"]["signatures"][0]
    signature = signed_transaction["tx"]["signatures"][0]["signature"]

    default_formated_transaction = cc2.format_default_transaction(
        transfer_transaction, signature, base64_pbk
    )

    # Compare default formatted transaction with signed transaction
    assert signed_transaction == default_formated_transaction


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_format_cosmwasm():
    """Test if CosmWasm transaction is correctly formated."""
    cc2 = CosmosCrypto()

    # Dummy CosmWasm transaction
    wasm_transaction = {
        "account_number": "8",
        "chain_id": "agent-land",
        "fee": {"amount": [], "gas": "200000"},
        "memo": "",
        "msgs": [
            {
                "type": "wasm/execute",
                "value": {
                    "sender": "cosmos14xjnl2mwwfz6pztpwzj6s89npxr0e3lhxl52nv",
                    "contract": "cosmos1xzlgeyuuyqje79ma6vllregprkmgwgav5zshcm",
                    "msg": {
                        "create_single": {
                            "item_owner": "cosmos1fz0dcvvqv5at6dl39804jy92lnndf3d5saalx6",
                            "id": "1234",
                            "path": "SOME_URI",
                        }
                    },
                    "sent_funds": [],
                },
            }
        ],
        "sequence": "25",
    }

    signed_transaction = cc2.sign_transaction(wasm_transaction)

    assert "value" in signed_transaction
    assert "signatures" in signed_transaction["value"]
    assert len(signed_transaction["value"]["signatures"]) == 1

    assert "pub_key" in signed_transaction["value"]["signatures"][0]
    assert "value" in signed_transaction["value"]["signatures"][0]["pub_key"]
    base64_pbk = signed_transaction["value"]["signatures"][0]["pub_key"]["value"]

    assert "signature" in signed_transaction["value"]["signatures"][0]
    signature = signed_transaction["value"]["signatures"][0]["signature"]

    wasm_formated_transaction = cc2.format_wasm_transaction(
        wasm_transaction, signature, base64_pbk
    )

    # Compare Wasm formatted transaction with signed transaction
    assert signed_transaction == wasm_formated_transaction


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_get_deploy_transaction_cosmwasm():
    """Test the get deploy transaction method."""
    cc2 = CosmosCrypto()
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)

    contract_interface = {"wasm_byte_code": b""}
    deployer_address = cc2.address
    deploy_transaction = cosmos_api.get_deploy_transaction(
        contract_interface, deployer_address
    )

    assert type(deploy_transaction) == dict and len(deploy_transaction) == 6
    assert "account_number" in deploy_transaction
    assert "chain_id" in deploy_transaction
    assert "fee" in deploy_transaction and deploy_transaction["fee"] == {
        "amount": [{"amount": "0", "denom": "atestfet"}],
        "gas": "80000",
    }
    assert "memo" in deploy_transaction
    assert "msgs" in deploy_transaction and len(deploy_transaction["msgs"]) == 1
    msg = deploy_transaction["msgs"][0]
    assert "type" in msg and msg["type"] == "wasm/store-code"
    assert (
        "value" in msg
        and msg["value"]["sender"] == deployer_address
        and msg["value"]["wasm_byte_code"] == contract_interface["wasm_byte_code"]
    )
    assert "sequence" in deploy_transaction


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_get_init_transaction_cosmwasm():
    """Test the get deploy transaction method."""
    cc2 = CosmosCrypto()
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)
    init_msg = "init_msg"
    code_id = 1
    deployer_address = cc2.address
    tx_fee = 1
    amount = 10
    deploy_transaction = cosmos_api.get_init_transaction(
        deployer_address, code_id, init_msg, amount, tx_fee
    )

    assert type(deploy_transaction) == dict and len(deploy_transaction) == 6
    assert "account_number" in deploy_transaction
    assert "chain_id" in deploy_transaction
    assert "fee" in deploy_transaction and deploy_transaction["fee"] == {
        "amount": [{"denom": "atestfet", "amount": "{}".format(tx_fee)}],
        "gas": "80000",
    }
    assert "memo" in deploy_transaction
    assert "msgs" in deploy_transaction and len(deploy_transaction["msgs"]) == 1
    msg = deploy_transaction["msgs"][0]
    assert "type" in msg and msg["type"] == "wasm/instantiate"
    assert (
        "value" in msg
        and msg["value"]["sender"] == deployer_address
        and msg["value"]["code_id"] == str(code_id)
        and msg["value"]["label"] == ""
        and msg["value"]["init_msg"] == init_msg
        and msg["value"]["init_funds"] == [{"denom": "atestfet", "amount": str(amount)}]
    )
    assert "sequence" in deploy_transaction


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_get_handle_transaction_cosmwasm():
    """Test the get deploy transaction method."""
    cc2 = CosmosCrypto()
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)
    handle_msg = "handle_msg"
    sender_address = cc2.address
    contract_address = "contract_address"
    tx_fee = 1
    amount = 10
    handle_transaction = cosmos_api.get_handle_transaction(
        sender_address, contract_address, handle_msg, amount, tx_fee
    )

    assert type(handle_transaction) == dict and len(handle_transaction) == 6
    assert "account_number" in handle_transaction
    assert "chain_id" in handle_transaction
    assert "fee" in handle_transaction and handle_transaction["fee"] == {
        "amount": [{"denom": "atestfet", "amount": "{}".format(tx_fee)}],
        "gas": "80000",
    }
    assert "memo" in handle_transaction
    assert "msgs" in handle_transaction and len(handle_transaction["msgs"]) == 1
    msg = handle_transaction["msgs"][0]
    assert "type" in msg and msg["type"] == "wasm/execute"
    assert (
        "value" in msg
        and msg["value"]["sender"] == sender_address
        and msg["value"]["contract"] == contract_address
        and msg["value"]["msg"] == handle_msg
        and msg["value"]["sent_funds"] == [{"denom": "atestfet", "amount": str(amount)}]
    )
    assert "sequence" in handle_transaction


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_try_execute_wasm_query():
    """Test the execute wasm query method."""
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)
    process_mock = mock.Mock()
    output = "output".encode("ascii")
    attrs = {"communicate.return_value": (output, "error")}
    process_mock.configure_mock(**attrs)
    with mock.patch("subprocess.Popen", return_value=process_mock):
        result = cosmos_api.try_execute_wasm_query(
            contract_address="contract_address", query_msg={}
        )
    assert result == output.decode("ascii")


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_try_execute_wasm_transaction():
    """Test the execute wasm query method."""
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)
    process_mock = mock.Mock()
    output = "output".encode("ascii")
    attrs = {"communicate.return_value": (output, "error")}
    process_mock.configure_mock(**attrs)
    with mock.patch("subprocess.Popen", return_value=process_mock):
        result = cosmos_api.try_execute_wasm_transaction(tx_signed="signed_transaction")
    assert result == output.decode("ascii")


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_send_signed_transaction_wasm_transaction():
    """Test the send_signed_transaction method for a wasm transaction."""
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)
    tx_signed = {"value": {"msg": [{"type": "wasm/store-code"}]}}
    with mock.patch.object(
        cosmos_api, "try_execute_wasm_transaction", return_value="digest"
    ):
        result = cosmos_api.send_signed_transaction(tx_signed=tx_signed)
    assert result == "digest"


@pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)
@pytest.mark.integration
@pytest.mark.ledger
def test_get_contract_instance():
    """Test the get contract instance method."""
    cosmos_api = CosmosApi(**COSMOS_TESTNET_CONFIG)
    assert cosmos_api.get_contract_instance("interface") is None
