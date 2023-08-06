#!/usr/bin/env python

"""Tests for `tasks3.tasks3` module."""
from typing import List
from tasks3 import tasks3, db

from pathlib import Path
from sqlalchemy import create_engine
import pytest


@pytest.fixture(params=["sqlite"])
def db_backend(request) -> str:
    return request.param


@pytest.fixture(params=["Title"])
def title(request) -> str:
    return request.param


@pytest.fixture(params=[0, 4], ids=["Not Urgent", "Very Urgent"])
def urgency(request) -> int:
    return request.param


@pytest.fixture(params=[0, 4], ids=["Not Important", "Very Important"])
def importance(request) -> int:
    return request.param


@pytest.fixture(params=[["pytest"]])
def tags(request) -> List[str]:
    return request.param


@pytest.fixture(params=[".", None])
def anchor_path(request) -> List[str]:
    return request.param


@pytest.fixture(params=["Testing tasks3 interface."])
def description(request) -> List[str]:
    return request.param


def get_db_engine(tmp_path: Path, backend: str) -> str:
    tasks3_path = tmp_path.joinpath("tasks3")
    tasks3_path.mkdir()
    tasks3_path.joinpath("task.db").absolute()
    db_path = tasks3_path.joinpath("task.db").absolute()
    engine = create_engine(f"{backend}:///{db_path}")
    db.init(engine)
    return engine


def test_task_add(
    tmp_path: Path,
    title,
    urgency,
    importance,
    tags,
    anchor_path,
    description,
    db_backend: str,
):
    db_engine = get_db_engine(tmp_path, db_backend)
    id = tasks3.add(
        title=title,
        urgency=urgency,
        importance=importance,
        tags=tags,
        anchor_folder=anchor_path,
        description=description,
        db_engine=db_engine,
    )
    with db.session_scope(db_engine) as session:
        task: db.Task = session.query(db.Task).filter_by(id=id).one()
        assert task.title == title
        assert task.urgency == urgency
        assert task.importance == importance
        assert task.tags == tags
        assert task.folder == anchor_path
        assert task.description == description


def test_task_edit(tmp_path: Path, db_backend: str):
    db_engine = get_db_engine(tmp_path, db_backend)
    title, urgency, importance, tags, anchor_path, description = (
        "New Title",
        4,
        4,
        ["new-tags"],
        "/tmp",
        "New description.",
    )
    id = tasks3.add(
        title="Old title",
        urgency=2,
        importance=2,
        tags=["old-tags"],
        anchor_folder=".",
        description="Old description",
        db_engine=db_engine,
    )
    tasks3.edit(
        id=id,
        db_engine=db_engine,
        title=title,
        urgency=urgency,
        importance=importance,
        tags=tags,
        anchor_folder=anchor_path,
        description=description,
    )
    with db.session_scope(db_engine) as session:
        task: db.Task = session.query(db.Task).filter_by(id=id).one()
        assert task.title == title
        assert task.urgency == urgency
        assert task.importance == importance
        assert task.tags == tags
        assert task.folder == anchor_path
        assert task.description == description


def test_task_remove(
    tmp_path: Path,
    title,
    urgency,
    importance,
    tags,
    anchor_path,
    description,
    db_backend: str,
):
    db_engine = get_db_engine(tmp_path, db_backend)
    id = tasks3.add(
        title=title,
        urgency=urgency,
        importance=importance,
        tags=tags,
        anchor_folder=anchor_path,
        description=description,
        db_engine=db_engine,
    )
    with db.session_scope(db_engine) as session:
        task: db.Task = session.query(db.Task).filter_by(id=id).one()
        assert task is not None
    task = tasks3.remove(id, db_engine)
    assert task.title == title
    assert task.urgency == urgency
    assert task.importance == importance
    assert task.tags == tags
    assert task.folder == anchor_path
    assert task.description == description
    with db.session_scope(db_engine) as session:
        task: db.Task = session.query(db.Task).filter_by(id=id).first()
        assert task is None
