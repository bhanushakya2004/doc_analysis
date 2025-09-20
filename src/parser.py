import json
import re

def parse_ai_response(ai_response) -> dict:
    """Parse AI response into structured format"""
    print(f"📥 Raw AI Response Type: {type(ai_response)}")
    
    # Handle TeamRunOutput object - try different attributes
    response_text = ""
    if hasattr(ai_response, 'content'):
        response_text = str(ai_response.content)
        print(f"📄 Extracted from .content: {response_text[:500]}...")
    elif hasattr(ai_response, 'text'):
        response_text = str(ai_response.text)
        print(f"📄 Extracted from .text: {response_text[:500]}...")
    elif hasattr(ai_response, 'response'):
        response_text = str(ai_response.response)
        print(f"📄 Extracted from .response: {response_text[:500]}...")
    elif hasattr(ai_response, 'message'):
        response_text = str(ai_response.message)
        print(f"📄 Extracted from .message: {response_text[:500]}...")
    else:
        response_text = str(ai_response)
        print(f"📄 Converted to string: {response_text[:500]}...")
    
    # Clean the response - remove markdown formatting and extra text
    response_text = response_text.strip()
    
    # Remove markdown code blocks if present
    if response_text.startswith('```'):
        lines = response_text.split('\n')
        response_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else response_text
    
    print(f"🧹 Cleaned response: {response_text[:300]}...")
    
    try:
        # First try to parse the entire response as JSON
        if response_text.startswith('{') and response_text.endswith('}'):
            parsed_json = json.loads(response_text)
            print(f"✅ Successfully parsed entire response as JSON")
            return parsed_json
        
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            parsed_json = json.loads(json_match.group())
            print(f"✅ Successfully extracted and parsed JSON")
            return parsed_json
            
    except Exception as e:
        print(f"❌ JSON parsing failed: {e}")
    
    # Enhanced fallback: try to extract basic information from text
    print(f"🔄 Using enhanced fallback parsing...")
    
    # Try to extract some basic info from the text response
    document_type = "Unknown"
    summary = response_text[:300] + "..." if len(response_text) > 300 else response_text
    
    # Simple keyword matching for document type
    text_lower = response_text.lower()
    if "lease" in text_lower or "rental" in text_lower or "rent" in text_lower:
        document_type = "Rental Agreement"
    elif "insurance" in text_lower or "policy" in text_lower:
        document_type = "Insurance Policy"
    elif "contract" in text_lower or "agreement" in text_lower:
        document_type = "Service Contract"
    
    return {
        "analysis_summary": {
            "document_type": document_type,
            "overall_risk_level": "MEDIUM",
            "complexity_score": 5,
            "summary": summary,
            "total_clauses_analyzed": 0,
            "parties_involved": [],
            "effective_date": None,
            "expiration_date": None,
            "document_title": None
        },
        "key_terms": [],
        "hidden_clauses": [],
        "risks_identified": [],
        "financial_implications": [],
        "recommendations": [],
        "confidence_score": 0.5
    }
