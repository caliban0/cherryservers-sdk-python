"""Cherry Servers image resource management module."""

from __future__ import annotations

from pydantic import Field

from cherry import _base


class ImageModel(_base.ResourceModel):
    """Cherry Servers image model.

    This model is frozen by default,
    since it represents an actual Cherry Servers image resource state.

    Attributes:
        id(int): ID of the image.
        name(str): Full name of the image.
        slug(str): Slug of the image name.

    """

    id: int = Field(description="ID of the image.")
    name: str = Field(description="Full name of the image.")
    slug: str = Field(description="Slug of the image name.")


class ImageClient(_base.ResourceClient):
    """Cherry Servers image client.

    Manage Cherry Servers image resources. This class should typically be initialized by
    :class:`cherry.facade.CherryApiFacade`.

    Example:
        .. code-block:: python

            facade = cherry.facade.CherryApiFacade(token="my-token")

            # Retrieve a list of available OSes for a server plan.
            images = facade.images.get_by_plan("cloud_vps_1")

    """

    def get_by_plan(self, plan_slug: str) -> list[Image]:
        """Retrieve a list of available OSes for a server plan."""
        response = self._api_client.get(f"plans/{plan_slug}/images", None, 5)
        images: list[Image] = []
        for value in response.json():
            image_model = ImageModel.model_validate(value)
            images.append(Image(self, image_model))

        return images


class Image(_base.Resource[ImageClient, ImageModel]):
    """Cherry Servers image resource.

    This class represents an existing Cherry Servers resource
    and should only be initialized by :class:`ImageClient`.
    """
