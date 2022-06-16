import pytest
from rossum_ng.models.queue import Queue
from rossum_ng.elis_api_client import ElisAPIClient
from rossum_ng.api_client import APIClient


@pytest.fixture
def dummy_queue():
    return {
        "id": 8198,
        "name": "Received invoices",
        "url": "https://elis.rossum.ai/api/v1/queues/8198",
        "workspace": "https://elis.rossum.ai/api/v1/workspaces/7540",
        "connector": None,
        "webhooks": [],
        "hooks": [],
        "schema": "https://elis.rossum.ai/api/v1/schemas/31336",
        "inbox": "https://elis.rossum.ai/api/v1/inboxes/1229",
        "users": ["https://elis.rossum.ai/api/v1/users/10775"],
        "session_timeout": "01:00:00",
        "rir_url": "https://all.rir.rossum.ai",
        "rir_params": None,
        "dedicated_engine": None,
        "generic_engine": None,
        "counts": {
            "importing": 0,
            "split": 0,
            "failed_import": 0,
            "to_review": 2,
            "reviewing": 0,
            "confirmed": 0,
            "exporting": 0,
            "postponed": 0,
            "failed_export": 0,
            "exported": 0,
            "deleted": 0,
            "purged": 0,
            "rejected": 0,
        },
        "default_score_threshold": 0.8,
        "automation_enabled": False,
        "automation_level": "never",
        "locale": "en_US",
        "metadata": {},
        "use_confirmed_state": False,
        "document_lifetime": "01:00:00",
        "settings": {
            "columns": [{"schema_id": "tags"}],
            "hide_export_button": True,
            "automation": {"automate_duplicates": True, "automate_suggested_edit": False},
            "rejection_config": {"enabled": True},
            "email_notifications": {
                "recipient": {"email": "john.doe@company.com", "name": "John Doe"},
                "unprocessable_attachments": False,
                "email_with_no_attachments": True,
                "postponed_annotations": False,
                "deleted_annotations": False,
            },
        },
    }


@pytest.mark.asyncio
class TestQueues:
    async def test_get_queues(self, http_client: APIClient, dummy_queue, mock_generator):
        http_client.fetch_all.return_value = mock_generator(dummy_queue)

        client = ElisAPIClient(http_client=http_client)
        queues = client.get_queues()

        async for q in queues:
            assert q == Queue(**dummy_queue)

        http_client.fetch_all.assert_called()
        http_client.fetch_all.assert_called_with("queues")

    async def test_get_queue(self, http_client: APIClient, dummy_queue):
        http_client.fetch_one.return_value = dummy_queue

        client = ElisAPIClient(http_client=http_client)
        qid = dummy_queue["id"]
        queue = await client.get_queue(qid)

        assert queue == Queue(**dummy_queue)

        http_client.fetch_one.assert_called()
        http_client.fetch_one.assert_called_with("queues", qid)