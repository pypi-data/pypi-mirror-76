import re
import json
import click
from pprint import pprint
from prettytable import PrettyTable
from peerplays.block import Block
from peerplays.amount import Amount
from peerplays.blockchain import Blockchain
from peerplays.account import Account
from peerplays.asset import Asset
from .decorators import onlineChain, unlockWallet
from .main import main


@main.command()
@click.pass_context
@onlineChain
@click.argument("objects", type=str, nargs=-1)
def info(ctx, objects):
    """ Obtain all kinds of information
    """
    if not objects:
        t = PrettyTable(["Key", "Value"])
        t.align = "l"
        info = ctx.peerplays.rpc.get_dynamic_global_properties()
        for key in info:
            t.add_row([key, info[key]])
        click.echo(t.get_string(sortby="Key"))

    for obj in objects:
        # Block
        if re.match("^[0-9]*$", obj):
            block = Block(obj, peerplays_instance=ctx.peerplays)
            if block:
                t = PrettyTable(["Key", "Value"])
                t.align = "l"
                for key in sorted(block):
                    value = block[key]
                    if key == "transactions":
                        value = json.dumps(value, indent=4)
                    t.add_row([key, value])
                click.echo(t)
            else:
                click.echo("Block number %s unknown" % obj)
        # Object Id
        elif len(obj.split(".")) == 3:
            data = ctx.peerplays.rpc.get_object(obj)
            if data:
                t = PrettyTable(["Key", "Value"])
                t.align = "l"
                for key in sorted(data):
                    value = data[key]
                    if isinstance(value, dict) or isinstance(value, list):
                        value = json.dumps(value, indent=4)
                    t.add_row([key, value])
                click.echo(t)
            else:
                click.echo("Object %s unknown" % obj)

        # Asset
        elif obj.upper() == obj:
            data = Asset(obj)
            t = PrettyTable(["Key", "Value"])
            t.align = "l"
            for key in sorted(data):
                value = data[key]
                if isinstance(value, dict):
                    value = json.dumps(value, indent=4)
                t.add_row([key, value])
            click.echo(t)

        # Public Key
        elif re.match("^PPY.{48,55}$", obj):
            account = ctx.peerplays.wallet.getAccountFromPublicKey(obj)
            if account:
                t = PrettyTable(["Account"])
                t.align = "l"
                t.add_row([account])
                click.echo(t)
            else:
                click.echo("Public Key not known" % obj)

        # Account name
        elif re.match("^[a-zA-Z0-9\-\._]{2,64}$", obj):
            account = Account(obj, full=True)
            if account:
                t = PrettyTable(["Key", "Value"])
                t.align = "l"
                for key in sorted(account):
                    value = account[key]
                    if isinstance(value, dict) or isinstance(value, list):
                        value = json.dumps(value, indent=4)
                    t.add_row([key, value])
                click.echo(t)
            else:
                click.echo("Account %s unknown" % obj)
        else:
            click.echo("Couldn't identify object to read")


@main.command()
@click.pass_context
@onlineChain
def fees(ctx):
    """ List fees
    """
    from peerplaysbase.operationids import getOperationNameForId

    chain = Blockchain(peerplays_instance=ctx.peerplays)
    feesObj = chain.chainParameters().get("current_fees")
    fees = feesObj["parameters"]

    t = PrettyTable(["Operation", "Type", "Fee"])
    t.align = "l"
    t.align["Fee"] = "r"

    for fee in fees:
        for f in fee[1]:
            t.add_row(
                [
                    getOperationNameForId(fee[0]),
                    f,
                    str(Amount({"amount": fee[1].get(f, 0), "asset_id": "1.3.0"})),
                ]
            )
    click.echo(t)
