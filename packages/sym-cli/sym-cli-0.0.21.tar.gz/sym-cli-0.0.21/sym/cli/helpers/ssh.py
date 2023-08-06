import re
from datetime import datetime, timedelta
from subprocess import CalledProcessError
from textwrap import dedent
from typing import Sequence

from ..decorators import intercept_errors, run_subprocess
from ..errors import AccessDenied, TargetNotConnected, WrappedSubprocessError
from ..helpers.boto import send_ssh_key
from ..helpers.config import Config, SymConfigFile
from ..helpers.params import get_ssh_user

MissingPublicKeyPattern = re.compile(r"Permission denied \(.*publickey.*\)")
TargetNotConnectedPattern = re.compile("TargetNotConnected")
AccessDeniedPattern = re.compile("AccessDeniedException")

SSHConfig = SymConfigFile("ssh/config")
SSHKey = SymConfigFile("ssh/key")


@intercept_errors()
@run_subprocess
def gen_ssh_key(dest: SymConfigFile):
    dest.path.parent.mkdir(parents=True, exist_ok=True)
    dest.path.unlink(missing_ok=True)
    yield "ssh-keygen", {"t": "rsa", "f": str(dest), "N": ""}


def ssh_args(client, instance, port) -> tuple:
    return (
        "ssh",
        instance,
        {"p": str(port), "F": str(SSHConfig), "l": get_ssh_user(), "v": client.debug},
    )


@run_subprocess
def _start_background_ssh_session(
    client: "SAMLClient", instance: str, port: int, *command
):
    yield (
        *ssh_args(client, instance, port),
        {"f": True},
        "-o BatchMode=yes",
        *command,
    )


@run_subprocess
def _start_ssh_session(client: "SAMLClient", instance: str, port: int, *command: str):
    yield (*ssh_args(client, instance, port), *command)


def start_ssh_session(
    client: "SAMLClient", instance: str, port: int, command: Sequence[str] = []
):
    ensure_ssh_key(client, instance, port)
    try:
        _start_ssh_session(client, instance, port, *command)
    except CalledProcessError as err:
        if MissingPublicKeyPattern.search(err.stderr):
            Config.touch_instance(instance, error=True)
            raise WrappedSubprocessError(
                err, f"Does the user ({get_ssh_user()}) exist on the instance?"
            ) from err
        # If the ssh key path is cached then this doesn't get intercepted in ensure_ssh_key
        elif TargetNotConnectedPattern.search(err.stderr):
            raise TargetNotConnected() from err
        elif AccessDeniedPattern.search(err.stderr):
            raise AccessDenied() from err
        else:
            raise WrappedSubprocessError(
                err, f"Contact your Sym administrator.", report=True
            ) from err
    else:
        Config.touch_instance(instance)


@intercept_errors({TargetNotConnectedPattern: TargetNotConnected}, suppress=True)
def ensure_ssh_key(client, instance: str, port: int):
    # Write the SSH Config first, we need to do this regardles of whether the
    # SSH Key is present on the box.

    # fmt: off
    SSHConfig.put(dedent(
        f"""
        Host {instance}
            IdentityFile {str(SSHKey)}
            PreferredAuthentications publickey
            PubkeyAuthentication yes
            StrictHostKeyChecking no
            PasswordAuthentication no
            ChallengeResponseAuthentication no
            GSSAPIAuthentication no
            ProxyCommand sh -c "sym ssh-session {client.resource} --instance %h --port %p"
        """
    ))
    # fmt: on

    instance_config = Config.get_instance(instance)

    if SSHKey.path.exists():
        last_connect = instance_config.get("last_connection")
        if last_connect and datetime.now() - last_connect < timedelta(days=1):
            client.dprint(f"Skipping remote SSH key check for {instance}")
            return
    else:
        gen_ssh_key(SSHKey, capture_output_=True)

    try:
        _start_background_ssh_session(
            client, instance, port, "exit", capture_output_=True
        )
    except CalledProcessError as err:
        if not MissingPublicKeyPattern.search(err.stderr):
            raise
        send_ssh_key(client, instance, SSHKey)
    else:
        return


def start_tunnel(client, instance: str, port: int):
    client.exec(
        "aws",
        "ssm",
        "start-session",
        target=instance,
        document_name="AWS-StartSSHSession",
        parameters=f"portNumber={port}",
    )
