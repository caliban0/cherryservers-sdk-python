"""Cherry Servers API client tests."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, cast
from unittest import mock

import pytest
import requests
from pydantic import Field

from cherryservers_sdk_python import _base, _client

if TYPE_CHECKING:
    from collections.abc import Generator


class RequestSchema(_base.RequestSchema):
    """Cherry Servers request schema for testing.."""

    data: str = Field(description="Test data.", default="my-test")


class TestCherryClient:
    """Test Cherry Servers API client."""

    @pytest.fixture
    def response(self) -> requests.Response:
        """Initialize default response."""
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps({"result": "test"}).encode("utf-8")
        return response

    @pytest.fixture
    def client(self) -> Generator[_client.CherryApiClient]:
        """Initialize default Cherry API client."""
        client = _client.CherryApiClient("test_token", user_agent_prefix="test")
        patcher = mock.patch.object(client, "_requests_session")
        patcher.start()
        yield client
        patcher.stop()

    def test_get(
        self, client: _client.CherryApiClient, response: requests.Response
    ) -> None:
        """Test GET request."""
        cast(mock.Mock, client._requests_session.get).return_value = response
        resp = client.get(path="test_url", params=None)
        cast(mock.Mock, client._requests_session.get).assert_called_with(
            "https://api.cherryservers.com/v1/test_url",
            params=None,
            timeout=120,
            allow_redirects=False,
        )
        assert resp == response

    def test_delete(
        self, client: _client.CherryApiClient, response: requests.Response
    ) -> None:
        """Test DELETE request."""
        cast(mock.Mock, client._requests_session.delete).return_value = response
        resp = client.delete(path="test_url", params=None)
        cast(mock.Mock, client._requests_session.delete).assert_called_with(
            "https://api.cherryservers.com/v1/test_url",
            params=None,
            timeout=120,
        )
        assert resp == response

    def test_post(
        self, client: _client.CherryApiClient, response: requests.Response
    ) -> None:
        """Test POST request."""
        response.status_code = 201
        cast(mock.Mock, client._requests_session.post).return_value = response
        req = RequestSchema()
        resp = client.post(path="test_url", data=req)
        cast(mock.Mock, client._requests_session.post).assert_called_with(
            "https://api.cherryservers.com/v1/test_url",
            params=None,
            timeout=120,
            data=req.model_dump_json(),
        )
        assert resp == response

    def test_put(
        self, client: _client.CherryApiClient, response: requests.Response
    ) -> None:
        """Test PUT request."""
        response.status_code = 201
        cast(mock.Mock, client._requests_session.put).return_value = response
        req = RequestSchema()
        resp = client.put(path="test_url", data=req)
        cast(mock.Mock, client._requests_session.put).assert_called_with(
            "https://api.cherryservers.com/v1/test_url",
            params=None,
            timeout=120,
            data=req.model_dump_json(),
        )
        assert resp == response

    def test_patch(
        self, client: _client.CherryApiClient, response: requests.Response
    ) -> None:
        """Test PATCH request."""
        response.status_code = 201
        cast(mock.Mock, client._requests_session.patch).return_value = response
        req = RequestSchema()
        resp = client.patch(path="test_url", data=req)
        cast(mock.Mock, client._requests_session.patch).assert_called_with(
            "https://api.cherryservers.com/v1/test_url",
            params=None,
            timeout=120,
            data=req.model_dump_json(),
        )
        assert resp == response
