import click
from click_option_group import MutuallyExclusiveOptionGroup

from .config import Config
from .params import get_resource_env_var
from .validations import validate_resource


def config_option(name: str, help: str):
    def decorator(f):
        option_decorator = click.option(
            f"--{name}",
            help=help,
            prompt=True,
            default=lambda: Config.instance().get(name),
        )
        return option_decorator(f)

    return decorator


def _resource_callback(ctx, resource: str):
    if resource is None:
        return None
    if not validate_resource(resource):
        raise click.BadParameter(f"Invalid resource: {resource}")
    return resource


def resource_option(f):
    option_decorator = click.option(
        "--resource",
        help="the Sym resource to use",
        envvar="SYM_RESOURCE",
        callback=_resource_callback,
        default=get_resource_env_var,
    )
    return option_decorator(f)


def aws_profile_options(f):
    group = MutuallyExclusiveOptionGroup("Ansible Roles")
    ansible_aws_profile = group.option(
        "--ansible-aws-profile",
        help="the local AWS Profile to use for Ansible commands",
        envvar="AWS_PROFILE",
    )
    ansible_sym_resource = group.option(
        "--ansible-sym-resource",
        help="the Sym resource to use for Ansible commands",
        envvar="SYM_ANSIBLE_RESOURCE",
        callback=_resource_callback,
    )
    return ansible_aws_profile(ansible_sym_resource(f))
