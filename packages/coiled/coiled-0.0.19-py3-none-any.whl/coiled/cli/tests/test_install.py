from click.testing import CliRunner
import pytest
import shutil

import coiled
from coiled.cli.install import install, remote_name_to_local_name, DEFAULT_PIP_PACKAGES
from coiled.cli.utils import parse_conda_command, conda_command


if shutil.which("conda") is None:
    pytest.skip(
        "Conda is needed to create local software environments", allow_module_level=True
    )


def test_install_raises(sample_user):
    bad_name = "not-a-software-environment"
    runner = CliRunner()
    result = runner.invoke(install, [bad_name])

    assert result.exit_code != 0
    err_msg = str(result.exception).lower()
    assert "could not find" in err_msg
    assert bad_name in err_msg


@pytest.mark.slow
def test_install_conda(sample_user):
    name = "my-env"
    coiled.create_software_environment(name=name, conda=["toolz"])
    runner = CliRunner()
    result = runner.invoke(install, [name])

    assert result.exit_code == 0
    output = result.output.lower()
    assert "conda activate" in output
    assert name in output


@pytest.mark.slow
def test_install_pip(sample_user):
    name = "my-env"
    coiled.create_software_environment(name=name, pip=["toolz"])
    runner = CliRunner()
    result = runner.invoke(install, [name])

    assert result.exit_code == 0

    local_name = remote_name_to_local_name(account=sample_user.user.username, name=name)
    cmd = [conda_command(), "run", "-n", local_name, "pip", "list", "--format=json"]
    output = parse_conda_command(cmd)
    assert any(i["name"] == "toolz" for i in output)


@pytest.mark.slow
def test_install_post_build(sample_user):
    name = "my-env"
    coiled.create_software_environment(
        name=name, conda=["toolz"], post_build=["export FOO=BARBAZ", "echo $FOO"]
    )
    runner = CliRunner()
    result = runner.invoke(install, [name])

    assert result.exit_code == 0
    assert "BARBAZ" in result.output


@pytest.mark.slow
def test_install_defaults(sample_user):
    # Ensure default packages (e.g. ipython, coiled) are installed
    name = "my-env"
    coiled.create_software_environment(name=name)
    runner = CliRunner()
    result = runner.invoke(install, [name])

    assert result.exit_code == 0

    local_name = remote_name_to_local_name(account=sample_user.user.username, name=name)
    cmd = [conda_command(), "run", "-n", local_name, "pip", "list", "--format=json"]
    output = parse_conda_command(cmd)
    for package in DEFAULT_PIP_PACKAGES:
        assert any(i["name"] == package for i in output)


@pytest.mark.slow
def test_install_multiple(sample_user):
    name = "my-env"
    coiled.create_software_environment(
        name=name,
        conda=["toolz"],
        pip=["ipython"],
        post_build=["export FOO=BARBAZ", "echo $FOO"],
    )
    runner = CliRunner()
    result = runner.invoke(install, [name])

    assert result.exit_code == 0
    assert "BARBAZ" in result.output
