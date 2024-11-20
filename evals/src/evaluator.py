import os
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class TarotReading:
    """Represents a single tarot reading interaction"""
    question: str
    card_name: str
    user_reflection: str
    ai_response: str
    timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'question': self.question,
            'card_name': self.card_name,
            'user_reflection': self.user_reflection,
            'ai_response': self.ai_response,
            'timestamp': self.timestamp
        }

@dataclass
class EvalMetrics:
    """Stores evaluation metrics for a reading"""
    personalization_score: float
    card_accuracy_score: float
    insight_depth_score: float
    overlooked_elements_score: float
    consistency_score: float
    
    def average_score(self) -> float:
        scores = [
            self.personalization_score,
            self.card_accuracy_score,
            self.insight_depth_score,
            self.overlooked_elements_score,
            self.consistency_score
        ]
        return np.mean(scores)
    
    def to_dict(self) -> Dict:
        return {
            'personalization_score': self.personalization_score,
            'card_accuracy_score': self.card_accuracy_score,
            'insight_depth_score': self.insight_depth_score,
            'overlooked_elements_score': self.overlooked_elements_score,
            'consistency_score': self.consistency_score,
            'average_score': self.average_score()
        }

class TarotEvaluator:
    """Main class for evaluating tarot readings"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.card_meanings = self._load_card_meanings()
    
    def _load_card_meanings(self) -> Dict:
        """Load card meanings from JSON file"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        meanings_path = os.path.join(current_dir, 'data', 'card_meanings.json')
        with open(meanings_path, 'r') as f:
            return json.load(f)
    
    def _create_eval_prompt(self, reading: TarotReading) -> str:
        """Create evaluation prompt for GPT-4"""
        card_info = self.card_meanings.get(reading.card_name, {})
        
        return f"""You are an expert tarot evaluation system. Evaluate this reading and provide scores (0-10) for each aspect.

CONTEXT:
USER QUESTION: "{reading.question}"
CARD DRAWN: {reading.card_name}
USER REFLECTION: "{reading.user_reflection}"
AI RESPONSE: "{reading.ai_response}"

TRADITIONAL CARD MEANINGS:
- Meanings: {', '.join(card_info.get('traditional_meanings', []))}
- Key Symbols: {', '.join(card_info.get('key_symbols', []))}
- Themes: {', '.join(card_info.get('themes', []))}

Provide your evaluation in the following JSON format ONLY, no other text:
{{
    "personalization": {{"score": X, "explanation": "brief explanation"}},
    "card_accuracy": {{"score": X, "explanation": "brief explanation"}},
    "insight_depth": {{"score": X, "explanation": "brief explanation"}},
    "overlooked_elements": {{"score": X, "explanation": "brief explanation"}},
    "consistency": {{"score": X, "explanation": "brief explanation"}}
}}"""

    def evaluate_reading(self, reading: TarotReading) -> EvalMetrics:
        """Evaluate a single tarot reading"""
        prompt = self._create_eval_prompt(reading)
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert tarot evaluation system. Respond with JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        try:
            eval_results = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {response.choices[0].message.content}")
            raise
        
        return EvalMetrics(
            personalization_score=eval_results['personalization']['score'],
            card_accuracy_score=eval_results['card_accuracy']['score'],
            insight_depth_score=eval_results['insight_depth']['score'],
            overlooked_elements_score=eval_results['overlooked_elements']['score'],
            consistency_score=eval_results['consistency']['score']
        )

    def batch_evaluate(self, readings: List[TarotReading]) -> Dict:
        """Evaluate multiple readings and generate statistics"""
        results = []
        for reading in readings:
            metrics = self.evaluate_reading(reading)
            results.append({
                'reading': reading.to_dict(),
                'metrics': metrics.to_dict()
            })
        
        # Calculate aggregate statistics
        all_metrics = [r['metrics'] for r in results]
        stats = {
            'overall_stats': {
                'mean_score': np.mean([m['average_score'] for m in all_metrics]),
                'std_score': np.std([m['average_score'] for m in all_metrics]),
                'total_readings': len(readings)
            },
            'detailed_results': results
        }
        
        return stats