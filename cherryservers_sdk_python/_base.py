from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from cherryservers_sdk_python import _client


class ResourceModel(BaseModel, abc.ABC):
    model_config = ConfigDict(frozen=True)


class ResourceClient(abc.ABC):  # noqa: B024
    """Cherry Servers resource client base.."""

    def __init__(self, api_client: _client.CherryApiClient) -> None:
        """Initialize a Cherry Servers resource client."""
        self._api_client = api_client


class Resource[C: ResourceClient, T: ResourceModel](abc.ABC):  # noqa: B024
    def __init__(self, client: C, model: T) -> None:
        """Initialize a Cherry Servers resource."""
        self._model = model
        self._client = client

    def get_model(self) -> T:
        """Get resource model.

        This model is frozen, since it represents actual resource state.
        """
        return self._model


class RequestSchema(BaseModel, abc.ABC):
    """Cherry Servers base API request schema."""