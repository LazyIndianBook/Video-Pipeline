"""Small, versioned intermediate representation; no executable code in content."""
from __future__ import annotations
import math
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

Subject = Literal['physics', 'chemistry', 'mathematics', 'biology']
Kind = Literal['rc_charge', 'atom_balance', 'chain_rule', 'mendel_cross']

class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)

class SourceRef(StrictModel):
    id: str = Field(min_length=3)
    uri: str
    locator: str
    rights_status: Literal['owned', 'permission', 'open_reference', 'unconfirmed']
    claim_scope: str
    retrieved_at: str

class Claim(StrictModel):
    id: str
    statement: str
    source_ids: list[str] = Field(min_length=1)
    assumptions: list[str] = Field(default_factory=list)
    status: Literal['draft', 'machine_checked', 'expert_approved'] = 'draft'

class Cue(StrictModel):
    start_s: float = Field(ge=0)
    end_s: float = Field(gt=0)
    text: str
    role: Literal['explain','question','feedback','recap'] = 'explain'
    voice: Literal['steady','curious','deliberate','light','reassuring'] = 'steady'
    answer_visible: bool = False
    @model_validator(mode='after')
    def ordered(self):
        if self.end_s <= self.start_s:
            raise ValueError('cue end must exceed start')
        if self.role == 'question' and self.answer_visible:
            raise ValueError('answer cannot be visible during a question')
        return self

class SceneSpec(StrictModel):
    schema_version: Literal['1.0'] = '1.0'
    id: str = Field(pattern=r'^[a-z][a-z0-9_-]{2,70}$')
    subject: Subject
    kind: Kind
    title: str
    objective: str
    class_context: str
    duration_s: float = Field(gt=0, le=600)
    fps: int = Field(default=24, ge=1, le=60)
    parameters: dict[str, float | int | str | list[int]]
    assumptions: list[str] = Field(min_length=1)
    sources: list[SourceRef] = Field(min_length=1)
    claims: list[Claim] = Field(min_length=1)
    cues: list[Cue] = Field(min_length=1)
    status: Literal['technical_preview','review_pending','approved'] = 'technical_preview'
    @model_validator(mode='after')
    def consistent(self):
        expected = {'physics':'rc_charge','chemistry':'atom_balance','mathematics':'chain_rule','biology':'mendel_cross'}
        if expected[self.subject] != self.kind:
            raise ValueError('subject/renderer mismatch')
        ids={s.id for s in self.sources}
        for c in self.claims:
            if not set(c.source_ids) <= ids:
                raise ValueError(f'unknown source on claim {c.id}')
        last=0.0
        for c in self.cues:
            if abs(c.start_s-last)>1e-6:
                raise ValueError('cues must provide contiguous ordered coverage')
            last=c.end_s
        if abs(last-self.duration_s)>1e-6:
            raise ValueError('cue duration does not match scene')
        if not math.isclose(self.duration_s*self.fps, round(self.duration_s*self.fps), abs_tol=1e-8):
            raise ValueError('duration must map to a whole number of frames')
        return self

class Check(StrictModel):
    name: str
    passed: bool
    detail: str

class ScienceReport(StrictModel):
    scene_id: str
    checks: list[Check]
    boundary: str = 'Checks cover the specified model only; they do not establish curriculum fit or expert approval.'
    @property
    def passed(self):
        return bool(self.checks) and all(c.passed for c in self.checks)

class Approval(StrictModel):
    role: Literal['academic','production']
    reviewer_id: str = Field(min_length=3)
    artifact_sha256: str = Field(pattern=r'^[a-f0-9]{64}$')
    approved: bool
    reviewed_at: str
    full_video_watched: bool = False
