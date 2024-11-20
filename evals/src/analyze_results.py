import json
from pathlib import Path
from typing import Dict, List
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class ResultsAnalyzer:
    def __init__(self, results_path: str):
        with open(results_path, 'r') as f:
            self.results = json.load(f)
        
    def create_summary_dataframe(self) -> pd.DataFrame:
        """Convert results into a pandas DataFrame for analysis"""
        readings = []
        for result in self.results['detailed_results']:
            reading = result['reading']
            metrics = result['metrics']
            
            reading_data = {
                'question': reading['question'],
                'card': reading['card_name'],
                'personalization_score': metrics['personalization_score'],
                'card_accuracy_score': metrics['card_accuracy_score'],
                'insight_depth_score': metrics['insight_depth_score'],
                'overlooked_elements_score': metrics['overlooked_elements_score'],
                'consistency_score': metrics['consistency_score'],
                'average_score': metrics['average_score']
            }
            readings.append(reading_data)
        
        return pd.DataFrame(readings)

    def generate_metrics_chart(self, output_path: str):
        """Generate a bar chart of average scores for each metric"""
        df = self.create_summary_dataframe()
        metrics = ['personalization_score', 'card_accuracy_score', 
                  'insight_depth_score', 'overlooked_elements_score', 
                  'consistency_score']
        
        plt.figure(figsize=(10, 6))
        avg_scores = df[metrics].mean()
        bars = plt.bar(range(len(metrics)), avg_scores)
        
        # Customize the chart
        plt.title('Average Scores by Evaluation Metric')
        plt.xlabel('Metric')
        plt.ylabel('Score')
        plt.xticks(range(len(metrics)), 
                  [m.replace('_score', '').replace('_', ' ').title() 
                   for m in metrics], 
                  rotation=45)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def generate_report(self, output_dir: Path):
        """Generate a comprehensive analysis report"""
        df = self.create_summary_dataframe()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = output_dir / f"analysis_report_{timestamp}.md"
        chart_path = output_dir / f"metrics_chart_{timestamp}.png"
        
        # Generate metrics chart
        self.generate_metrics_chart(str(chart_path))
        
        # Create report content
        report_content = f"""# Tarot Reading Evaluation Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overall Statistics
- Total Readings Evaluated: {len(df)}
- Average Overall Score: {df['average_score'].mean():.2f}
- Score Range: {df['average_score'].min():.2f} - {df['average_score'].max():.2f}

## Metric Breakdown
| Metric | Average Score | Std Dev |
|--------|---------------|---------|
"""
        
        # Add metric details to report
        metrics = ['personalization_score', 'card_accuracy_score', 
                  'insight_depth_score', 'overlooked_elements_score', 
                  'consistency_score']
        
        for metric in metrics:
            name = metric.replace('_score', '').replace('_', ' ').title()
            avg = df[metric].mean()
            std = df[metric].std()
            report_content += f"| {name} | {avg:.2f} | {std:.2f} |\n"
        
        # Add recommendations based on scores
        report_content += "\n## Analysis & Recommendations\n"
        
        # Find lowest scoring metrics
        avg_scores = df[metrics].mean()
        lowest_metric = avg_scores.idxmin()
        lowest_score = avg_scores.min()
        
        report_content += f"""
### Areas for Improvement
The lowest scoring metric was {lowest_metric.replace('_score', '').replace('_', ' ').title()} 
with an average score of {lowest_score:.2f}. Consider:

1. {'Enhancing personalization by more directly addressing user questions' if lowest_metric == 'personalization_score' else
    'Strengthening alignment with traditional card meanings' if lowest_metric == 'card_accuracy_score' else
    'Developing deeper, more meaningful insights' if lowest_metric == 'insight_depth_score' else
    'Better highlighting overlooked card elements' if lowest_metric == 'overlooked_elements_score' else
    'Maintaining more consistent interpretation style'}

### Strongest Areas
The highest performing metric was {avg_scores.idxmax().replace('_score', '').replace('_', ' ').title()}
with an average score of {avg_scores.max():.2f}.
"""
        
        # Write report to file
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        return report_path, chart_path

def main():
    # Get the most recent results file
    results_dir = Path('results')
    results_files = list(results_dir.glob('eval_results_*.json'))
    if not results_files:
        print("No results files found!")
        return
    
    latest_results = max(results_files, key=lambda x: x.stat().st_mtime)
    print(f"Analyzing results from: {latest_results}")
    
    # Create analyzer and generate report
    analyzer = ResultsAnalyzer(str(latest_results))
    report_path, chart_path = analyzer.generate_report(results_dir)
    
    print(f"\nAnalysis complete!")
    print(f"Report saved to: {report_path}")
    print(f"Chart saved to: {chart_path}")

if __name__ == "__main__":
    main()