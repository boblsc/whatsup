"""
LLM-based paper relevance evaluator using OpenAI API
"""

from openai import OpenAI
from typing import Dict, Any, List


class LLMEvaluator:
    """Evaluate paper relevance using OpenAI's GPT models."""
    
    def __init__(
        self, 
        api_key: str,
        model: str = "gpt-4o-mini",
        threshold: float = 7.0
    ):
        """
        Initialize the LLM evaluator.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (e.g., gpt-4o-mini)
            threshold: Minimum score for relevance (0-10)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.threshold = threshold
    
    def evaluate_papers(
        self,
        papers: List[Dict[str, Any]],
        research_context: str,
        user_interests: str
    ) -> List[Dict[str, Any]]:
        """
        Evaluate multiple papers for relevance.
        
        Args:
            papers: List of paper dictionaries
            research_context: Summary from Zotero library
            user_interests: User's interest description
            
        Returns:
            List of relevant papers with scores
        """
        relevant_papers = []
        
        for paper in papers:
            result = self._evaluate_single_paper(
                paper, research_context, user_interests
            )
            
            if result['score'] >= self.threshold:
                paper['relevance_score'] = result['score']
                paper['relevance_reason'] = result['reason']
                relevant_papers.append(paper)
        
        # Sort by relevance score (highest first)
        relevant_papers.sort(
            key=lambda x: x['relevance_score'], 
            reverse=True
        )
        
        return relevant_papers
    
    def _evaluate_single_paper(
        self,
        paper: Dict[str, Any],
        research_context: str,
        user_interests: str
    ) -> Dict[str, Any]:
        """
        Evaluate a single paper.
        
        Args:
            paper: Paper dictionary
            research_context: Summary from Zotero library
            user_interests: User's interest description
            
        Returns:
            Dictionary with score and reason
        """
        prompt = self._build_prompt(
            paper, research_context, user_interests
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an academic research "
                            "assistant. Evaluate the relevance "
                            "of papers to the user's research "
                            "interests."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_completion_tokens=200
            )
            
            content = response.choices[0].message.content
            score, reason = self._parse_response(content)
            
            return {'score': score, 'reason': reason}
            
        except Exception as e:
            print(
                f"Error evaluating paper "
                f"'{paper['title'][:50]}...': {e}"
            )
            return {'score': 0.0, 'reason': 'Evaluation error'}
    
    def _build_prompt(
        self,
        paper: Dict[str, Any],
        research_context: str,
        user_interests: str
    ) -> str:
        """Build the evaluation prompt."""
        prompt = f"""Given the following research background 
and interests, evaluate the relevance of this new arXiv paper.

{research_context}

CURRENT SPECIFIC INTERESTS:
{user_interests}

NEW PAPER TO EVALUATE:
Title: {paper['title']}
Abstract: {paper['abstract']}

Rate the relevance of this paper on a scale of 0-10:
- 0-3: Not relevant
- 4-6: Somewhat relevant
- 7-8: Relevant
- 9-10: Highly relevant

Respond in the format:
SCORE: [0-10]
REASON: [One sentence explanation]"""
        
        return prompt
    
    def _parse_response(self, content: str) -> tuple:
        """
        Parse LLM response to extract score and reason.
        
        Args:
            content: LLM response text
            
        Returns:
            Tuple of (score, reason)
        """
        score = 0.0
        reason = "No reason provided"
        
        lines = content.strip().split('\n')
        
        for line in lines:
            if line.startswith('SCORE:'):
                try:
                    score_text = line.replace(
                        'SCORE:', ''
                    ).strip()
                    # Extract first number found
                    import re
                    match = re.search(r'\d+\.?\d*', score_text)
                    if match:
                        score = float(match.group())
                except (ValueError, AttributeError):
                    score = 0.0
            elif line.startswith('REASON:'):
                reason = line.replace('REASON:', '').strip()
        
        return score, reason

