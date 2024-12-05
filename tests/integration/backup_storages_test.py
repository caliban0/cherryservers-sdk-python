"""Test cherry backup_storages functionality."""

from __future__ import annotations

import pytest
import requests

import cherry


class TestBackupStorage:
    """Test backup storage functionality."""

    @pytest.fixture(scope="class")
    def project_id(self, vps: cherry.servers.Server) -> int:
        """VPS project ID."""
        vps_server_model = vps.get_model()
        assert vps_server_model.project is not None

        return vps_server_model.project.id

    @pytest.fixture(scope="class")
    def storage(
        self, facade: cherry.facade.CherryApiFacade, vps: cherry.servers.Server
    ) -> cherry.backup_storages.BackupStorage:
        """Initialize a BackupStorage instance."""
        creation_req = cherry.backup_storages.CreationRequest(
            region="eu_nord_1", slug="backup_50"
        )

        return facade.backup_storages.create(creation_req, vps.get_model().id)

    def test_get_by_id(
        self,
        storage: cherry.backup_storages.BackupStorage,
        facade: cherry.facade.CherryApiFacade,
    ) -> None:
        """Test getting a single backup storage by ID."""
        storage_model = storage.get_model()
        retrieved_storage = facade.backup_storages.get_by_id(storage_model.id)

        retrieved_model = retrieved_storage.get_model()

        assert storage_model.id == retrieved_model.id
        assert storage_model.attached_to == retrieved_model.attached_to

    def test_list_by_project(
        self,
        project_id: int,
        facade: cherry.facade.CherryApiFacade,
        storage: cherry.backup_storages.BackupStorage,
    ) -> None:
        """Test listing backup storages by project."""
        storages = facade.backup_storages.list_by_project(project_id)

        retrieved_storage_models = [storage.get_model() for storage in storages]
        fixture_storage_model = storage.get_model()

        assert any(
            storage_model.id == fixture_storage_model.id
            for storage_model in retrieved_storage_models
        )

    def test_list_backup_plans(self, facade: cherry.facade.CherryApiFacade) -> None:
        """Test listing backup storage plans."""
        plans = facade.backup_storages.list_backup_plans()

        assert any(plan.slug == "backup_50" for plan in plans)

    def test_update(
        self,
        storage: cherry.backup_storages.BackupStorage,
        sshkey: cherry.sshkeys.SSHKey,
    ) -> None:
        """Test updating a backup storage."""
        storage.update(
            cherry.backup_storages.UpdateRequest(
                slug="backup_100",
                ssh_key=sshkey.get_model().key,
            )
        )

        updated_model_copy = storage.get_model()

        assert updated_model_copy.plan is not None
        assert updated_model_copy.plan.slug == "backup_100"

    def test_update_access_method(
        self,
        storage: cherry.backup_storages.BackupStorage,
    ) -> None:
        """Test updating a backup storage access method."""
        storage.update_access_method(
            cherry.backup_storages.UpdateAccessMethodsRequest(enabled=False),
            method_name="ftp",
        )

        updated_model_copy = storage.get_model()

        assert updated_model_copy.methods is not None

        assert any(
            access_method.enabled is False and access_method.name == "ftp"
            for access_method in updated_model_copy.methods
        )

    def test_delete(
        self,
        storage: cherry.backup_storages.BackupStorage,
        facade: cherry.facade.CherryApiFacade,
    ) -> None:
        """Test deleting a backup storage."""
        storage.delete()

        with pytest.raises(requests.exceptions.HTTPError):
            facade.backup_storages.get_by_id(storage.get_model().id)
