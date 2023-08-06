#!/usr/bin/env python

"""Tests for `tasks3` package."""

import pytest

from click.testing import CliRunner

import tasks3 as package_tasks3
from tasks3 import tasks3, cli


@pytest.fixture
def cli_runner():
    return CliRunner()


def test_command_line_interface_main(cli_runner):
    """Test the CLI (tasks3)"""
    main_result = cli_runner.invoke(cli.main)
    assert main_result.exit_code == 0
    assert package_tasks3.__doc__ in main_result.output


def test_command_line_interface_version(cli_runner):
    """Test the CLI (tasks3 --version)"""
    version_result = cli_runner.invoke(cli.main, ["--version"])
    assert version_result.exit_code == 0
    assert package_tasks3.__version__ in version_result.output


def test_command_line_interface_main_help(cli_runner):
    """Test the CLI (tasks3 --help)"""
    help_result = cli_runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help     Show this message and exit." in help_result.output


def test_command_line_interface_task(cli_runner):
    """Test the CLI (tasks3 task)"""
    task_result = cli_runner.invoke(cli.main, ["task"])
    assert task_result.exit_code == 0
    assert cli.task.__doc__ in task_result.output
    for command in cli.task.commands:
        assert command in task_result.output


def test_command_line_interface_task_help(cli_runner):
    """Test the CLI (tasks3 task --help)"""
    task_help_result = cli_runner.invoke(cli.main, ["task", "--help"])
    assert task_help_result.exit_code == 0
    assert cli.task.__doc__ in task_help_result.output
    for command in cli.task.commands:
        assert command in task_help_result.output
