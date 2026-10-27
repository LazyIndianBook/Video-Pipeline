import pytest
from pydantic import ValidationError
from examleaf.interfaces import AssetManifest,ProviderJob,ShortSpec,PendingAdapter

def test_generated_asset_needs_provenance():
    with pytest.raises(ValidationError):AssetManifest(id='test',content_sha256='a'*64,local_path='x.mp4',kind='video',origin='generated',licence='pending')
def test_unknown_external_job_must_be_rejoinable():
    with pytest.raises(ValidationError):ProviderJob(idempotency_key='12345678',provider='vendor',model='v1',state='unknown',estimated_cents=30,input_sha256='a'*64)
def test_short_must_reflow():
    with pytest.raises(ValidationError):ShortSpec(id='x',source_lesson_id='y',source_claim_ids=['c1'],target_seconds=30,hook='question',complete_payoff='answer',retained_conditions=[],destination_resource_id='free-1',access_tier='free',layout_strategy='crop')
def test_pending_adapter_not_success():
    with pytest.raises(NotImplementedError):PendingAdapter('higgsfield').submit({},'12345678')
