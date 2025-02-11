from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from groq import Groq
import logging
from fastapi.middleware.cors import CORSMiddleware

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load environment variables
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
HF_API_TOKEN = "YOUR_HF_API_KEY"

# Load Models
custom_model = pipeline(
    "text-classification",
    model="Rasmuzeri/imdb-sentiment-distilbert",
    token=HF_API_TOKEN
)

groq_client = Groq(api_key=GROQ_API_KEY)

# New structured prompt for Llama
LLAMA_PROMPT = """Analyze the sentiment of this movie review and respond STRICTLY in the format: 
'sentiment:confidence' where:
- sentiment must be either 'positive' or 'negative'
- confidence must be a decimal number between 0 and 1 with exactly 2 decimal places

Examples of valid responses:
positive:0.95
negative:0.82

Review: {text}
Response:"""

class AnalysisRequest(BaseModel):
    text: str
    model: str  # "custom" or "llama"

class AnalysisResponse(BaseModel):
    sentiment: str
    confidence: float

def parse_llama_response(response_text: str) -> tuple[str, float]:
    """Parse the Llama response into sentiment and confidence"""
    try:
        # Clean the response and split into parts
        cleaned = response_text.strip().lower()
        if ":" not in cleaned:
            raise ValueError("Missing colon separator")
            
        sentiment_part, confidence_part = cleaned.split(":", 1)
        sentiment = "positive" if "positive" in sentiment_part else "negative"
        confidence = max(0.0, min(1.0, float(confidence_part)))
        
        return sentiment, round(confidence, 2)
        
    except Exception as e:
        logging.warning(f"Failed to parse Llama response: {response_text} - {str(e)}")
        # Fallback to simple sentiment detection
        sentiment = "positive" if "positive" in cleaned else "negative"
        return sentiment, 1.0 if sentiment == "positive" else 0.0

@app.post("/analyze/", response_model=AnalysisResponse)
async def analyze_sentiment(request: AnalysisRequest):
    try:
        if request.model == "custom":
            result = custom_model(request.text)[0]
            return {
                "sentiment": "positive" if result['label'] == "LABEL_1" else "negative",
                "confidence": result['score']
            }
            
        elif request.model == "llama":
            response = groq_client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": LLAMA_PROMPT.format(text=request.text)
                }],
                model="llama3-70b-8192",
                temperature=0.1,
                max_tokens=20
            )
            
            raw_response = response.choices[0].message.content
            sentiment, confidence = parse_llama_response(raw_response)
            
            return {
                "sentiment": sentiment,
                "confidence": confidence
            }
            
        else:
            raise HTTPException(status_code=400, detail="Invalid model specified")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))