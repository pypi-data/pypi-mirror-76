# -*- coding: utf-8 -*-
import _pytest.python as pythtest
from dict_tools import data
import mock
import os
import pathlib
import pop.hub
import pop.mods.pop.testing as testing
import pytest
import sys
import logging
from typing import Any, Dict, List

log = logging.getLogger("pytest_pop.plugin")


def pytest_sessionstart(session: pytest.Session):
    root = pathlib.Path(session.config.rootdir)
    CODE_DIR = str(root)
    if CODE_DIR in sys.path:
        sys.path.remove(CODE_DIR)
    sys.path.insert(0, CODE_DIR)


@pytest.fixture(autouse=True, scope="session")
def hub():
    """
    Create a base hub that is scoped for session, you should redefine it in your own conftest.py
    to be scoped for modules or functions
    """
    hub = pop.hub.Hub()

    # Set up the rudimentary logger
    hub.pop.sub.add(dyne_name="log")

    # This will create the loop used for pytest-asyncio
    hub.pop.loop.create()

    yield hub

    # Hub cleanup
    hub.pop.Loop.close()


@pytest.fixture(scope="session")
def event_loop():
    hub = pop.hub.Hub()
    hub.pop.loop.create()
    yield hub.pop.Loop
    hub.pop.Loop.close()


@pytest.fixture(autouse=True, scope="session")
def setup_session():
    pass


@pytest.fixture(autouse=True, scope="session")
def teardown_session():
    pass


@pytest.fixture(autouse=True, scope="module")
def setup_module():
    pass


@pytest.fixture(autouse=True, scope="module")
def teardown_module():
    pass


@pytest.fixture(autouse=True, scope="function")
def setup_function():
    pass


@pytest.fixture(autouse=True, scope="function")
def teardown_function():
    pass


@pytest.fixture(scope="function")
def mock_hub(hub):
    yield hub.pop.testing.mock_hub()


@pytest.fixture(scope="function")
def contract_hub(hub):
    yield testing.ContractHub(hub)


@pytest.fixture(scope="function")
def lazy_hub(hub):
    yield testing._LazyPop(hub)


@pytest.fixture(scope="function")
def mock_attr_hub(hub):
    yield hub.pop.testing.mock_attr_hub()


@pytest.fixture(scope="function")
def fn_hub(hub):
    yield hub.pop.testing.fn_hub()


@pytest.fixture(scope="session")
def acct_subs() -> List[str]:
    log.error("Override the 'acct_subs' fixture in your own conftest.py")
    return []


@pytest.fixture(scope="session")
def acct_profile() -> str:
    log.error("Override the 'acct_profile' fixture in your own conftest.py")
    return ""


@pytest.fixture(scope="module")
@pytest.mark.asyncio
async def ctx(hub, acct_subs: List[str], acct_profile: str) -> Dict[str, Any]:
    """
    Set up the context for idem-cloud executions
    :param acct_subs: The output of an overridden fixture of the same name
    :param acct_profile: The output of an overridden fixture of the same name
    """
    ctx = data.NamespaceDict(
        {"run_name": "test", "test": False, "acct": data.NamespaceDict(),}
    )

    old_opts = hub.OPT

    if acct_subs and acct_profile:
        if not (
            hasattr(hub, "acct") and (hasattr(hub, "states") or hasattr(hub, "exec"))
        ):
            log.debug("Creating a temporary hub to generate ctx")
            # Use a fresh hub, they didn't supply a unique one
            hub = pop.hub.Hub()
            # Add the bare minimum for acct
            for dyne in ("acct", "exec"):
                hub.pop.sub.add(dyne_name=dyne)

        if not (
            hub.OPT.get("acct")
            and hub.OPT.acct.get("acct_file")
            and hub.OPT.acct.get("acct_key")
        ):
            # Get the account information from environment variables
            log.debug("Loading temporary config from idem and acct")
            with mock.patch("sys.argv", ["pytest_pop"]):
                hub.pop.config.load(["idem", "acct"], "idem", parse_cli=False)

        # Add the profile to the account
        hub.acct.init.unlock(hub.OPT.acct.acct_file, hub.OPT.acct.acct_key)
        ctx["acct"] = await hub.acct.init.gather(acct_subs, acct_profile)

    hub.OPT = old_opts

    yield ctx


def pytest_runtest_protocol(item: pythtest.Function, nextitem: pythtest.Function):
    """
    implements the runtest_setup/call/teardown protocol for
    the given test item, including capturing exceptions and calling
    reporting hooks.
    """
    log.debug(f">>>>> START >>>>> {item.name}")


def pytest_runtest_teardown(item: pythtest.Function):
    """
    called after ``pytest_runtest_call``
    """
    log.debug(f"<<<<< END <<<<<<< {item.name}")


@pytest.fixture(scope="session", autouse=True)
def os_sleep_secs():
    if "CI_RUN" in os.environ:
        return 1.75
    return 0.5
