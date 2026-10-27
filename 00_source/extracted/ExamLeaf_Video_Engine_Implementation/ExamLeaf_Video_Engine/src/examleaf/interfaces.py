"""Production-boundary contracts. Remote adapters are explicitly unimplemented.
These data types are locally validated; they are not claims of provider integration.
"""
from pathlib import Path
from typing import Literal,Protocol
from pydantic import Field,model_validator
from .contracts import StrictModel,SourceRef,Claim,Subject

class LessonPlan(StrictModel):
    schema_version: Literal['1.0']='1.0'
    id: str
    board: str
    academic_year: str
    subject: Subject
    class_level: int=Field(ge=10,le=12)
    language: str
    objective: str
    prerequisites: list[str]
    sources: list[SourceRef]=Field(min_length=1)
    claims: list[Claim]=Field(min_length=1)
    target_seconds: int=Field(default=600,gt=0,le=1200)
    source_review_status: Literal['pending','approved']='pending'
    syllabus_review_status: Literal['pending','approved']='pending'
    actual_audio_seconds: float|None=None
    @model_validator(mode='after')
    def known_sources(self):
        ids={s.id for s in self.sources}
        if any(not set(c.source_ids)<=ids for c in self.claims):raise ValueError('unresolved source claim')
        return self

class AssetManifest(StrictModel):
    id: str
    content_sha256: str=Field(pattern=r'^[a-f0-9]{64}$')
    local_path: str
    kind: Literal['svg','video','audio','mesh','data']
    origin: Literal['deterministic','licensed','generated']
    licence: str
    attribution: str=''
    provider: str|None=None
    model: str|None=None
    provider_job_id: str|None=None
    science_review_status: Literal['pending','approved','not_applicable']='pending'
    @model_validator(mode='after')
    def generated_trace(self):
        if self.origin=='generated' and not (self.provider and self.model and self.provider_job_id):
            raise ValueError('generated asset requires provider/model/job provenance')
        return self

class ProviderJob(StrictModel):
    idempotency_key: str=Field(min_length=8)
    provider: str
    model: str
    provider_job_id: str|None=None
    state: Literal['planned','reserved','submitted','running','succeeded','failed','unknown']='planned'
    estimated_cents: int=Field(ge=0)
    actual_cents: int|None=Field(default=None,ge=0)
    input_sha256: str=Field(pattern=r'^[a-f0-9]{64}$')
    @model_validator(mode='after')
    def require_job_id(self):
        if self.state in ('submitted','running','succeeded','unknown') and not self.provider_job_id:
            raise ValueError('persist provider job ID; do not resubmit an unknown job')
        return self

class ShortSpec(StrictModel):
    id: str
    source_lesson_id: str
    source_claim_ids: list[str]=Field(min_length=1)
    target_seconds: int=Field(ge=20,le=60)
    hook: str
    complete_payoff: str
    retained_conditions: list[str]
    destination_resource_id: str
    access_tier: Literal['free','book_entitlement','preview']
    layout_strategy: Literal['reflow']='reflow'
    approval_status: Literal['pending','approved']='pending'

class GeneratorAdapter(Protocol):
    def estimate(self,request:dict)->int:...
    def submit(self,request:dict,idempotency_key:str)->str:...
    def poll(self,job_id:str)->dict:...
    def fetch(self,job_id:str,directory:Path)->AssetManifest:...

class PendingAdapter:
    """Fail closed rather than pretend an SDK or MCP endpoint has been tested."""
    def __init__(self,name:str):self.name=name
    def estimate(self,request:dict)->int:raise NotImplementedError(f'{self.name}: authenticated estimate adapter not implemented')
    def submit(self,request:dict,idempotency_key:str)->str:raise NotImplementedError(f'{self.name}: live integration not validated')
    def poll(self,job_id:str)->dict:raise NotImplementedError(f'{self.name}: polling integration not validated')
    def fetch(self,job_id:str,directory:Path)->AssetManifest:raise NotImplementedError(f'{self.name}: artifact retrieval not validated')
