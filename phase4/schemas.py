from pydantic import BaseModel
from typing import List


class Evidence(BaseModel):
    claim: str
    source_page: str


class ResearchReport(BaseModel):
    executive_summary: str
    background: str
    key_findings: List[str]
    benefits: List[str]
    challenges: List[str]
    evidence: List[Evidence]
    conclusion: str
    limitations: List[str]