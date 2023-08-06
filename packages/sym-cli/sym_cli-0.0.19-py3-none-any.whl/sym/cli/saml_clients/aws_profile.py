from typing import Final, Iterator, Tuple

from ..decorators import intercept_errors, require_bins, run_subprocess
from ..helpers.contexts import push_env
from ..helpers.keywords_to_options import Argument
from . import SAMLClient


class AwsProfile(SAMLClient):
    resource: str
    debug: bool
    binary: Final[str] = 'aws'

    def __init__(self, resource: str, *, debug: bool) -> None:
        self.resource = resource
        self.debug = debug

    @intercept_errors()
    @run_subprocess
    @require_bins(binary)
    def exec(self, *args: str, **opts: str) -> Iterator[Tuple[Argument, ...]]:
        self.log_subprocess_event(args)
        with push_env("AWS_PROFILE", self.resource):
            yield *args, opts
