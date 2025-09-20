from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
import os

# ---- Enhanced Agents with Better Prompts ----
document_analyzer = Agent(
    name="Document Analyzer",
    role="Expert document content extractor and clause identifier",
    model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
    instructions=[
        "You are a meticulous document analysis expert specializing in contracts, policies, and agreements.",
        "ALWAYS respond with properly formatted JSON as requested.",
        "Extract ALL key information including: terms, conditions, obligations, rights, limitations, and exclusions.",
        "Identify document type, parties involved, effective dates, and renewal terms.",
        "Pay special attention to fine print, asterisks, footnotes, and conditional clauses.",
        "Look for: coverage limits, deductibles, exclusions, cancellation terms, liability caps, and renewal conditions.",
        "Flag any ambiguous language or terms that could be interpreted differently.",
        "Structure your findings clearly with specific clause references where possible.",
        "IMPORTANT: Provide concrete analysis results, not delegation messages."
    ]
)

risk_assessor = Agent(
    name="Risk Assessor",
    role="Financial and legal risk evaluation specialist",
    model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
    instructions=[
        "You are a risk assessment expert focused on identifying financial, legal, and operational risks.",
        "Evaluate each clause for potential negative impacts on the user/policyholder/tenant.",
        "Assess: financial exposure, liability risks, compliance requirements, and exit costs.",
        "Rate risk levels as: CRITICAL (immediate action needed), HIGH (significant concern), MEDIUM (monitor closely), LOW (minimal impact).",
        "Calculate potential financial impacts with specific dollar amounts where possible.",
        "Identify red flags: unusual terms, one-sided clauses, automatic renewals, penalty fees.",
        "Consider both immediate and long-term implications of each identified risk."
    ]
)

analysis_team = Team(
    name="Document Analysis Team",
    members=[document_analyzer, risk_assessor],
    model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
    instructions=[
        "You are the final coordinator ensuring comprehensive document analysis.",
        "DO NOT delegate - provide direct analysis results in the requested JSON format.",
        "Combine insights from document extraction and risk assessment.",
        "Extract specific details: document type, parties, dates, terms, risks, and recommendations.",
        "Focus on actionable findings and concrete analysis results.",
        "ALWAYS respond with valid JSON structure as requested in the prompt."
    ],
    show_members_responses=False,  # Changed to False to get final result
    markdown=False  # Changed to False for cleaner JSON output
)
