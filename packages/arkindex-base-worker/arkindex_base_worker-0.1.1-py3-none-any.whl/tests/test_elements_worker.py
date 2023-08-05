# -*- coding: utf-8 -*-
import json
import os
import sys
import tempfile
from argparse import Namespace
from uuid import UUID

import pytest
from apistar.exceptions import ErrorResponse

from arkindex_worker.models import Element
from arkindex_worker.worker import ElementsWorker


def test_cli_default(monkeypatch):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump(
            [
                {"id": "volumeid", "type": "volume"},
                {"id": "pageid", "type": "page"},
                {"id": "actid", "type": "act"},
                {"id": "surfaceid", "type": "surface"},
            ],
            f,
        )

    monkeypatch.setenv("TASK_ELEMENTS", path)
    worker = ElementsWorker()
    worker.configure()

    assert worker.args.elements_list.name == path
    assert not worker.args.element
    os.unlink(path)


def test_cli_arg_elements_list_given(mocker):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump(
            [
                {"id": "volumeid", "type": "volume"},
                {"id": "pageid", "type": "page"},
                {"id": "actid", "type": "act"},
                {"id": "surfaceid", "type": "surface"},
            ],
            f,
        )

    mocker.patch.object(sys, "argv", ["worker", "--elements-list", path])
    worker = ElementsWorker()
    worker.configure()

    assert worker.args.elements_list.name == path
    assert not worker.args.element
    os.unlink(path)


def test_cli_arg_element_one_given_not_uuid(mocker):
    mocker.patch.object(sys, "argv", ["worker", "--element", "1234"])
    worker = ElementsWorker()
    with pytest.raises(SystemExit):
        worker.configure()


def test_cli_arg_element_one_given(mocker):
    mocker.patch.object(
        sys, "argv", ["worker", "--element", "12341234-1234-1234-1234-123412341234"]
    )
    worker = ElementsWorker()
    worker.configure()

    assert worker.args.element == [UUID("12341234-1234-1234-1234-123412341234")]
    # elements_list is None because TASK_ELEMENTS environment variable isn't set
    assert not worker.args.elements_list


def test_cli_arg_element_many_given(mocker):
    mocker.patch.object(
        sys,
        "argv",
        [
            "worker",
            "--element",
            "12341234-1234-1234-1234-123412341234",
            "43214321-4321-4321-4321-432143214321",
        ],
    )
    worker = ElementsWorker()
    worker.configure()

    assert worker.args.element == [
        UUID("12341234-1234-1234-1234-123412341234"),
        UUID("43214321-4321-4321-4321-432143214321"),
    ]
    # elements_list is None because TASK_ELEMENTS environment variable isn't set
    assert not worker.args.elements_list


def test_list_elements_elements_list_arg_wrong_type(monkeypatch):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump({}, f)

    monkeypatch.setenv("TASK_ELEMENTS", path)
    worker = ElementsWorker()
    worker.configure()
    os.unlink(path)

    with pytest.raises(AssertionError) as e:
        worker.list_elements()
    assert str(e.value) == "Elements list must be a list"


def test_list_elements_elements_list_arg_empty_list(monkeypatch):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump([], f)

    monkeypatch.setenv("TASK_ELEMENTS", path)
    worker = ElementsWorker()
    worker.configure()
    os.unlink(path)

    with pytest.raises(AssertionError) as e:
        worker.list_elements()
    assert str(e.value) == "No elements in elements list"


def test_list_elements_elements_list_arg_missing_id(monkeypatch):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump([{"type": "volume"}], f)

    monkeypatch.setenv("TASK_ELEMENTS", path)
    worker = ElementsWorker()
    worker.configure()
    os.unlink(path)

    elt_list = worker.list_elements()

    assert elt_list == []


def test_list_elements_elements_list_arg(monkeypatch):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump(
            [
                {"id": "volumeid", "type": "volume"},
                {"id": "pageid", "type": "page"},
                {"id": "actid", "type": "act"},
                {"id": "surfaceid", "type": "surface"},
            ],
            f,
        )

    monkeypatch.setenv("TASK_ELEMENTS", path)
    worker = ElementsWorker()
    worker.configure()
    os.unlink(path)

    elt_list = worker.list_elements()

    assert elt_list == ["volumeid", "pageid", "actid", "surfaceid"]


def test_list_elements_element_arg(mocker):
    mocker.patch(
        "arkindex_worker.worker.argparse.ArgumentParser.parse_args",
        return_value=Namespace(
            element=["volumeid", "pageid"], verbose=False, elements_list=None
        ),
    )

    worker = ElementsWorker()
    worker.configure()

    elt_list = worker.list_elements()

    assert elt_list == ["volumeid", "pageid"]


def test_list_elements_both_args_error(mocker):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump(
            [
                {"id": "volumeid", "type": "volume"},
                {"id": "pageid", "type": "page"},
                {"id": "actid", "type": "act"},
                {"id": "surfaceid", "type": "surface"},
            ],
            f,
        )
    mocker.patch(
        "arkindex_worker.worker.argparse.ArgumentParser.parse_args",
        return_value=Namespace(
            element=["anotherid", "againanotherid"],
            verbose=False,
            elements_list=open(path),
        ),
    )

    worker = ElementsWorker()
    worker.configure()
    os.unlink(path)

    with pytest.raises(AssertionError) as e:
        worker.list_elements()
    assert str(e.value) == "elements-list and element CLI args shouldn't be both set"


def test_create_sub_element_wrong_element():
    worker = ElementsWorker()
    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=None,
            type="something",
            name="0",
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element="not element type",
            type="something",
            name="0",
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"


def test_create_sub_element_wrong_type():
    worker = ElementsWorker()
    elt = Element({"zone": None})

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=elt, type=None, name="0", polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "type shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=elt, type=1234, name="0", polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "type shouldn't be null and should be of type str"


def test_create_sub_element_wrong_name():
    worker = ElementsWorker()
    elt = Element({"zone": None})

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=elt,
            type="something",
            name=None,
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "name shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=elt,
            type="something",
            name=1234,
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "name shouldn't be null and should be of type str"


def test_create_sub_element_wrong_polygon():
    worker = ElementsWorker()
    elt = Element({"zone": None})

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=elt, type="something", name="0", polygon=None,
        )
    assert str(e.value) == "polygon shouldn't be null and should be of type list"

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=elt, type="something", name="O", polygon="not a polygon",
        )
    assert str(e.value) == "polygon shouldn't be null and should be of type list"

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=elt, type="something", name="O", polygon=[[1, 1], [2, 2]],
        )
    assert str(e.value) == "polygon should have at least three points"

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=elt,
            type="something",
            name="O",
            polygon=[[1, 1, 1], [2, 2, 1], [2, 1, 1], [1, 2, 1]],
        )
    assert str(e.value) == "polygon points should be lists of two items"

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=elt, type="something", name="O", polygon=[[1], [2], [2], [1]],
        )
    assert str(e.value) == "polygon points should be lists of two items"

    with pytest.raises(AssertionError) as e:
        worker.create_sub_element(
            element=elt,
            type="something",
            name="O",
            polygon=[["not a coord", 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "polygon points should be lists of two numbers"


def test_create_sub_element_api_error(responses):
    worker = ElementsWorker()
    worker.configure()
    elt = Element(
        {
            "id": "12341234-1234-1234-1234-123412341234",
            "corpus": {"id": "11111111-1111-1111-1111-111111111111"},
            "zone": {"image": {"id": "22222222-2222-2222-2222-222222222222"}},
        }
    )
    responses.add(
        responses.POST,
        "https://arkindex.teklia.com/api/v1/elements/create/",
        status=500,
    )

    with pytest.raises(ErrorResponse):
        worker.create_sub_element(
            element=elt,
            type="something",
            name="0",
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )

    assert len(responses.calls) == 1
    assert (
        responses.calls[0].request.url
        == "https://arkindex.teklia.com/api/v1/elements/create/"
    )


def test_create_sub_element(responses):
    worker = ElementsWorker()
    worker.configure()
    elt = Element(
        {
            "id": "12341234-1234-1234-1234-123412341234",
            "corpus": {"id": "11111111-1111-1111-1111-111111111111"},
            "zone": {"image": {"id": "22222222-2222-2222-2222-222222222222"}},
        }
    )
    responses.add(
        responses.POST,
        "https://arkindex.teklia.com/api/v1/elements/create/",
        status=200,
    )

    worker.create_sub_element(
        element=elt,
        type="something",
        name="0",
        polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
    )

    assert len(responses.calls) == 1
    assert (
        responses.calls[0].request.url
        == "https://arkindex.teklia.com/api/v1/elements/create/"
    )
