# -*- coding: utf-8 -*-
import logging
import os
import sys
from pathlib import Path

from arkindex_worker import logger
from arkindex_worker.worker import BaseWorker


def test_init_default_local_share():
    worker = BaseWorker()

    assert worker.work_dir == os.path.expanduser("~/.local/share/arkindex")


def test_init_default_xdg_data_home(monkeypatch):
    path = str(Path(__file__).absolute().parent)
    monkeypatch.setenv("XDG_DATA_HOME", path)
    worker = BaseWorker()

    assert worker.work_dir == f"{path}/arkindex"


def test_init_var_ponos_data_given(monkeypatch):
    path = str(Path(__file__).absolute().parent)
    monkeypatch.setenv("PONOS_DATA", path)
    worker = BaseWorker()

    assert worker.work_dir == f"{path}/current"


def test_cli_default(mocker):
    worker = BaseWorker()
    spy = mocker.spy(worker, "add_arguments")
    assert not spy.called
    assert logger.level == logging.NOTSET
    assert not hasattr(worker, "api_client")
    worker.configure()

    assert spy.called
    assert spy.call_count == 1
    assert not worker.args.verbose
    assert logger.level == logging.NOTSET
    assert worker.api_client

    logger.setLevel(logging.NOTSET)


def test_cli_arg_verbose_given(mocker):
    worker = BaseWorker()
    spy = mocker.spy(worker, "add_arguments")
    assert not spy.called
    assert logger.level == logging.NOTSET
    assert not hasattr(worker, "api_client")

    mocker.patch.object(sys, "argv", ["worker", "-v"])
    worker.configure()

    assert spy.called
    assert spy.call_count == 1
    assert worker.args.verbose
    assert logger.level == logging.DEBUG
    assert worker.api_client

    logger.setLevel(logging.NOTSET)
