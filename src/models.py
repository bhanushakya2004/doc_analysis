from pydantic import BaseModel, Field
from typing import List, Optional

# ---- Enhanced Data Models ----
class KeyTerm(BaseModel):
    term: str = Field(..., description="The key term or concept")
    definition: str = Field(..., description="Clear explanation of the term")
    location: str = Field(..., description="Where in document this appears")
    importance: str = Field(..., description="HIGH, MEDIUM, or LOW")

class HiddenClause(BaseModel):
    clause_text: str = Field(..., description="The actual text of the clause")
    location: str = Field(..., description="Section/page where found")
    hidden_reason: str = Field(..., description="Why this might be overlooked")
    potential_impact: str = Field(..., description="What this could mean for the user")
    severity: str = Field(..., description="CRITICAL, HIGH, MEDIUM, or LOW")

class Risk(BaseModel):
    risk_type: str = Field(..., description="Type of risk (financial, legal, operational)")
    description: str = Field(..., description="Detailed risk description")
    likelihood: str = Field(..., description="HIGH, MEDIUM, or LOW")
    severity: str = Field(..., description="CRITICAL, HIGH, MEDIUM, or LOW")
    mitigation: str = Field(..., description="Suggested action to address risk")

class FinancialImplication(BaseModel):
    item: str = Field(..., description="Financial item or cost")
    amount: Optional[str] = Field(None, description="Specific amount if mentioned")
    frequency: Optional[str] = Field(None, description="When this cost applies")
    impact_type: str = Field(..., description="COST, SAVING, or LIABILITY")
    description: str = Field(..., description="Detailed explanation")

class Recommendation(BaseModel):
    action: str = Field(..., description="Specific recommended action")
    priority: str = Field(..., description="HIGH, MEDIUM, or LOW")
    reasoning: str = Field(..., description="Why this recommendation is important")
    timeline: str = Field(..., description="When to take action")

class AnalysisSummary(BaseModel):
    document_type: str
    document_title: Optional[str]
    parties_involved: List[str]
    effective_date: Optional[str]
    expiration_date: Optional[str]
    overall_risk_level: str = Field(..., description="CRITICAL, HIGH, MEDIUM, or LOW")
    complexity_score: int = Field(..., ge=1, le=10, description="Document complexity 1-10")
    summary: str = Field(..., description="Executive summary of key findings")
    total_clauses_analyzed: int

class DocAnalysisRequest(BaseModel):
    docid: str = Field(..., description="Unique document identifier")
    email: str = Field(..., description="User email for tracking")
    text: str = Field(..., description="Document text to analyze")

class DocAnalysisResponse(BaseModel):
    docid: str
    email: str
    analysis_summary: AnalysisSummary
    key_terms: List[KeyTerm]
    hidden_clauses: List[HiddenClause]
    risks_identified: List[Risk]
    financial_implications: List[FinancialImplication]
    recommendations: List[Recommendation]
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Analysis confidence 0.0-1.0")
    analysis_timestamp: str
    processing_time_seconds: float
