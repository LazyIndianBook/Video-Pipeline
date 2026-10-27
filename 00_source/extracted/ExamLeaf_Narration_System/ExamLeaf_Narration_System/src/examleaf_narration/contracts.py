from __future__ import annotations
import re
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator

class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

class VoiceIdentity(Strict):
    identity_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    brief: str = Field(min_length=1)
    locale: Literal["en-IN", "hi-IN", "as-IN"]
    rights_status: Literal["audition-only", "licensed-stock", "consented-custom", "unverified"]
    rights_record: str = Field(min_length=1)
    reference_audio_sha256: str | None = None

class Direction(Strict):
    mode: Literal["curious", "steady", "deliberate", "light", "reassuring", "focused"] = "steady"
    target_wpm: int = Field(default=140, ge=80, le=185)
    emphasis: list[str] = Field(default_factory=list)
    notes: str = ""

class Cue(Strict):
    cue_id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    phrase: str = Field(min_length=1)
    occurrence: int = Field(default=1, ge=1)
    edge: Literal["start", "end"] = "start"
    action: Literal["show", "highlight", "transform", "hide", "reveal-answer"]
    element_id: str = Field(min_length=1)

class Pause(Strict):
    kind: Literal["none", "beat", "think", "pause-video"] = "none"
    seconds: float = Field(default=0.0, ge=0, le=30)
    prompt: str = ""
    @model_validator(mode="after")
    def check(self):
        if self.kind == "none" and self.seconds != 0:
            raise ValueError("A none pause cannot contain time")
        if self.kind in {"think", "pause-video"} and not self.prompt:
            raise ValueError("Student pauses require a specific task prompt")
        return self

class Segment(Strict):
    segment_id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    objective_id: str = Field(min_length=1)
    claim_ids: list[str] = Field(min_length=1)
    text_template: str = Field(min_length=1, max_length=6000)
    direction: Direction = Field(default_factory=Direction)
    pause_after: Pause = Field(default_factory=Pause)
    cues: list[Cue] = Field(default_factory=list)
    expected_visuals: list[str] = Field(default_factory=list)
    critical_phrases: list[str] = Field(default_factory=list)
    answers_after: str | None = None
    @field_validator("text_template")
    @classmethod
    def no_stage_tags(cls, text):
        if re.search(r"\[[^\]]+\]|<[^>]+>", text):
            raise ValueError("Provider/stage tags belong to direction, not canonical spoken text")
        return text

class NarrationPlan(Strict):
    schema_version: Literal["1.0"] = "1.0"
    lesson_id: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    academic_edition: str
    source_claim_manifest: str
    voice: VoiceIdentity
    lexicon_version: str
    segments: list[Segment] = Field(min_length=1)
    @model_validator(mode="after")
    def dependencies(self):
        ids=[s.segment_id for s in self.segments]
        if len(ids)!=len(set(ids)): raise ValueError("Duplicate segment ids")
        cues=[c.cue_id for s in self.segments for c in s.cues]
        if len(cues)!=len(set(cues)): raise ValueError("Duplicate cue ids")
        index={sid:i for i,sid in enumerate(ids)}
        for i,seg in enumerate(self.segments):
            if seg.answers_after:
                j=index.get(seg.answers_after,-1)
                if not 0<=j<i: raise ValueError("An answer must reference an earlier question")
                q=self.segments[j]
                if q.pause_after.kind not in {"think","pause-video"} or q.pause_after.seconds<=0:
                    raise ValueError("Question needs an explicit protected response window")
        return self

class ProviderProfile(Strict):
    provider: Literal["elevenlabs", "cartesia", "gemini", "openai"]
    model: str
    voice_id: str
    api_version: str | None = None
    live_contract_verified: bool = False

class AlignedWord(Strict):
    text: str = Field(min_length=1)
    start: float = Field(ge=0)
    end: float = Field(gt=0)
    @model_validator(mode="after")
    def interval(self):
        if self.end<=self.start: raise ValueError("Non-positive word interval")
        return self

class Alignment(Strict):
    segment_id: str
    audio_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    transcript_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    method: Literal["provider-timestamps", "forced-aligner", "human", "synthetic-fixture"]
    engine_version: str
    words: list[AlignedWord]
    @model_validator(mode="after")
    def ordered(self):
        for left,right in zip(self.words,self.words[1:]):
            if right.start<left.end-.001: raise ValueError("Overlapping/out-of-order single-speaker words")
        return self
