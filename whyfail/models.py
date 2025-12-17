"""
Data structures for whyfail error explanations.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Explanation:
    """
    Represents a human-readable explanation for an exception.
    
    Attributes:
        title: Brief description of what went wrong
        reason: Detailed explanation of why it happened
        suggestions: List of actionable fix suggestions
        context: Optional additional context information
    """
    title: str
    reason: str
    suggestions: List[str]
    context: Optional[str] = None

    def format_output(self) -> str:
        """
        Format the explanation as a human-readable string.
        
        Returns:
            Formatted explanation string
        """
        output = ["\n" + "=" * 60]
        output.append("[WHYFAIL] Human-Readable Error Explanation")
        output.append("=" * 60)
        output.append(f"❌ {self.title}")
        output.append("")
        output.append(f"📌 Why this happened:")
        output.append(f"   {self.reason}")
        output.append("")
        output.append(f"💡 How to fix it:")
        for i, suggestion in enumerate(self.suggestions, 1):
            output.append(f"   {i}. {suggestion}")
        
        if self.context:
            output.append("")
            output.append(f"🔍 Additional context:")
            output.append(f"   {self.context}")
        
        output.append("=" * 60 + "\n")
        return "\n".join(output)
