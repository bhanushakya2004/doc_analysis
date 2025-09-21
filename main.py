from fastapi import FastAPI, HTTPException
from datetime import datetime
import json

from src.models import (
    DocAnalysisRequest,
    DocAnalysisResponse,
    AnalysisSummary,
    KeyTerm,
    HiddenClause,
    Risk,
    FinancialImplication,
    Recommendation,
)
from src.agents import analysis_team
from src.parser import parse_ai_response
from src.config import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Document Analysis API", version="1.0.0")

@app.post("/docanalyser", response_model=DocAnalysisResponse)
async def doc_analyser(request: DocAnalysisRequest):
    """
    Analyze document for hidden clauses, risks, and key terms using AI agents
    """
    start_time = datetime.utcnow()
    print(f"🚀 Starting analysis for docid: {request.docid}")
    print(f"📧 User email: {request.email}")
    print(f"📄 Document text length: {len(request.text)} characters")
    
    try:
        # Enhanced prompt with structured output request
        analysis_prompt = f"""
        URGENT: Analyze this document directly and return ONLY valid JSON. Do not delegate or explain the process.

        DOCUMENT TEXT:
        {request.text}

        REQUIRED: Return ONLY this JSON structure with actual analysis data (no other text):

        {{
            "analysis_summary": {{
                "document_type": "[identify: insurance/rental/contract/etc]",
                "document_title": "[extract title or null]",
                "parties_involved": "["[list all parties mentioned]"]",
                "effective_date": "[YYYY-MM-DD format or null]",
                "expiration_date": "[YYYY-MM-DD format or null]", 
                "overall_risk_level": "[CRITICAL/HIGH/MEDIUM/LOW based on analysis]",
                "complexity_score": [rate 1-10 based on document complexity],
                "summary": "[2-3 sentence executive summary of key findings]",
                "total_clauses_analyzed": [count of clauses found]
            }},
            "key_terms": [
                {{
                    "term": "[important term]",
                    "definition": "[what it means]",
                    "location": "[where found in document]", 
                    "importance": "[HIGH/MEDIUM/LOW]"
                }}
            ],
            "hidden_clauses": [
                {{
                    "clause_text": "[actual text of hidden/concerning clause]",
                    "location": "[section where found]",
                    "hidden_reason": "[why this might be missed]",
                    "potential_impact": "[impact on user]",
                    "severity": "[CRITICAL/HIGH/MEDIUM/LOW]"
                }}
            ],
            "risks_identified": [
                {{
                    "risk_type": "[financial/legal/operational]",
                    "description": "[detailed risk description]",
                    "likelihood": "[HIGH/MEDIUM/LOW]",
                    "severity": "[CRITICAL/HIGH/MEDIUM/LOW]",
                    "mitigation": "[how to address this risk]"
                }}
            ],
            "financial_implications": [
                {{
                    "item": "[cost/fee/penalty item]",
                    "amount": "[specific amount if mentioned]",
                    "frequency": "[when this applies]", 
                    "impact_type": "[COST/SAVING/LIABILITY]",
                    "description": "[detailed explanation]"
                }}
            ],
            "recommendations": [
                {{
                    "action": "[specific action to take]",
                    "priority": "[HIGH/MEDIUM/LOW]",
                    "reasoning": "[why this is important]",
                    "timeline": "[when to act]"
                }}
            ],
            "confidence_score": [0.0-1.0 confidence in analysis]
        }}

        CRITICAL: Respond with ONLY the JSON above filled with actual analysis data. No other text before or after.
        """
        
        print(f"🤖 Sending analysis request to AI team...")
        
        # Run analysis
        response = analysis_team.run(analysis_prompt)
        
        print(f"✅ Received AI team response")
        
        # Parse the structured response
        parsed_data = parse_ai_response(response)
        
        # Calculate processing time
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        
        print(f"⏱️ Processing time: {processing_time:.2f} seconds")
        print(f"🔍 Parsed data keys: {list(parsed_data.keys())}")
        
        # Build final response with safe defaults and error handling
        try:
            analysis_summary_data = parsed_data.get("analysis_summary", {})
            print(f"📊 Analysis summary data: {analysis_summary_data}")
            
            result = DocAnalysisResponse(
                docid=request.docid,
                email=request.email,
                analysis_summary=AnalysisSummary(
                    document_type=analysis_summary_data.get("document_type", "Unknown"),
                    document_title=analysis_summary_data.get("document_title"),
                    parties_involved=analysis_summary_data.get("parties_involved", []),
                    effective_date=analysis_summary_data.get("effective_date"),
                    expiration_date=analysis_summary_data.get("expiration_date"),
                    overall_risk_level=analysis_summary_data.get("overall_risk_level", "MEDIUM"),
                    complexity_score=analysis_summary_data.get("complexity_score", 5),
                    summary=analysis_summary_data.get("summary", "Analysis completed"),
                    total_clauses_analyzed=analysis_summary_data.get("total_clauses_analyzed", 0)
                ),
                key_terms=[KeyTerm(**term) for term in parsed_data.get("key_terms", [])],
                hidden_clauses=[HiddenClause(**clause) for clause in parsed_data.get("hidden_clauses", [])],
                risks_identified=[Risk(**risk) for risk in parsed_data.get("risks_identified", [])],
                financial_implications=[FinancialImplication(**impl) for impl in parsed_data.get("financial_implications", [])],
                recommendations=[Recommendation(**rec) for rec in parsed_data.get("recommendations", [])],
                confidence_score=parsed_data.get("confidence_score", 0.8),
                analysis_timestamp=end_time.isoformat() + "Z",
                processing_time_seconds=processing_time
            )
            
            print(f"✅ Successfully created response object")
            return result
            
        except Exception as model_error:
            print(f"❌ Error creating response models: {model_error}")
            print(f"📋 Available parsed_data: {json.dumps(parsed_data, indent=2)}")
            raise HTTPException(status_code=500, detail=f"Response model creation failed: {str(model_error)}")
        
    except Exception as e:
        print(f"❌ Analysis failed with error: {str(e)}")
        print(f"🔍 Error type: {type(e)}")
        import traceback
        print(f"📋 Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat() + "Z"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
