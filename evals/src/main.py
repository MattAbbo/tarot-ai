import json
from datetime import datetime
from pathlib import Path
from evaluator import TarotEvaluator, TarotReading

def main():
    # Initialize evaluator
    evaluator = TarotEvaluator()
    
    # Sample readings to evaluate
    test_readings = [
        TarotReading(
            question="Will my new business succeed?",
            card_name="The Magician",
            user_reflection="I see potential and power in the card.",
            ai_response="""Looking at the Magician card in relation to your business question, 
            there's a strong emphasis on manifestation and utilizing your resources. The four 
            elements on the table that you haven't mentioned - the wand, cup, pentacle, and 
            sword - represent all the tools needed for success. Your observation of potential 
            and power aligns with the Magician's upward-pointing wand, suggesting your ability 
            to channel higher inspiration into practical results.""",
            timestamp=datetime.now().isoformat()
        )
    ]
    
    try:
        # Run evaluation
        print("Starting evaluation...")
        results = evaluator.batch_evaluate(test_readings)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("results")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"eval_results_{timestamp}.json"
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Evaluation complete. Results saved to {output_path}")
        
        # Print summary
        print("\nEvaluation Summary:")
        print(f"Total readings evaluated: {results['overall_stats']['total_readings']}")
        print(f"Average score: {results['overall_stats']['mean_score']:.2f}")
        print(f"Standard deviation: {results['overall_stats']['std_score']:.2f}")
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise

if __name__ == "__main__":
    main()