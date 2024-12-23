"""Test cherryservers_sdk_python projects module functionality."""

from __future__ import annotations

import pytest
import requests

import cherryservers_sdk_python


class TestProject:
    """Test Project functionality."""

    @pytest.fixture(scope="class")
    def project(
        self, facade: cherryservers_sdk_python.facade.CherryApiFacade, team_id: int
    ) -> cherryservers_sdk_python.projects.Project:
        """Initialize a Cherry Servers Project."""
        creation_req = cherryservers_sdk_python.projects.CreationRequest(
            name="cherryservers-python-sdk-project-test"
        )
        project = facade.projects.create(creation_req, team_id=team_id)

        project_model = project.get_model()

        assert project_model.name == creation_req.name

        return project

    def test_get_by_id(
        self,
        project: cherryservers_sdk_python.projects.Project,
        facade: cherryservers_sdk_python.facade.CherryApiFacade,
    ) -> None:
        """Test getting a single project by ID."""
        project_model = project.get_model()
        retrieved_project = facade.projects.get_by_id(project_model.id)
        retrieved_project_model = retrieved_project.get_model()

        assert retrieved_project_model.name == project_model.name

    def test_get_by_team(
        self,
        project: cherryservers_sdk_python.projects.Project,
        facade: cherryservers_sdk_python.facade.CherryApiFacade,
        team_id: int,
    ) -> None:
        """Test getting all projects that belong to a team."""
        retrieved_projects = facade.projects.list_by_team(team_id)
        retrieved_project_models = [model.get_model() for model in retrieved_projects]
        project_model = project.get_model()

        assert any(
            project_model.name == retrieved_project_model.name
            for retrieved_project_model in retrieved_project_models
        )

    def test_update(self, project: cherryservers_sdk_python.projects.Project) -> None:
        """Test updating a project."""
        update_req = cherryservers_sdk_python.projects.UpdateRequest(
            name="cherryservers-python-sdk-project-test-updated", bgp=True
        )
        project.update(update_req)

        updated_model = project.get_model()

        assert updated_model.name == update_req.name

    def test_delete(
        self,
        project: cherryservers_sdk_python.projects.Project,
        facade: cherryservers_sdk_python.facade.CherryApiFacade,
    ) -> None:
        """Test deleting a project."""
        project.delete()
        project_model = project.get_model()

        with pytest.raises(requests.exceptions.HTTPError):
            facade.projects.get_by_id(project_model.id)
