# -*- coding: utf-8 -*-
from peerplaysbase.account import PublicKey
from .account import Account
from .instance import BlockchainInstance

from graphenecommon.message import Message as GrapheneMessage, InvalidMessageSignature


@BlockchainInstance.inject
class Message(GrapheneMessage):
    MESSAGE_SPLIT = (
        "-----BEGIN PEERPLAYS SIGNED MESSAGE-----",
        "-----BEGIN META-----",
        "-----BEGIN SIGNATURE-----",
        "-----END PEERPLAYS SIGNED MESSAGE-----",
    )

    def define_classes(self):
        self.account_class = Account
        self.publickey_class = PublicKey
