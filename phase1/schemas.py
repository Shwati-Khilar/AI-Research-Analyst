from pydantic import BaseModel, Field
from typing import List


class ResearchAnalysis(BaseModel):
    definition: str
    how_it_works: str
    examples: List[str] = Field(min_length=3, max_length=3)
    limitations: List[str] = Field(min_length=2)
    key_takeaway: str