# -*- coding: utf-8 -*-
import os

import pytest


@pytest.fixture(autouse=True)
def pass_schema(responses):
    schema_url = os.environ.get("ARKINDEX_API_SCHEMA_URL")
    responses.add_passthru(schema_url)
