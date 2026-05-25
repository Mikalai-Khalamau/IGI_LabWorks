# Lab 4, Task 2
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module for text analysis using regex, statistics, and OOP.
Implements Variant 27 specific tasks and general text analysis requirements.
"""
import re
from typing import List, Dict, Any

class BaseTextAnalyzer:
    """Base class providing core text storage and OOP features."""
    _analysis_version = "1.0"  # Static attribute

    def __init__(self, text: str = ""):
        self._text = text
        self._results: Dict[str, Any] = {}
        self._last_operation = "init"  # Dynamic attribute

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value
        self._last_operation = "text_updated"

    def get_text(self) -> str:
        return self._text

    def set_text(self, value: str):
        self.text = value

    def __len__(self) -> int:
        return len(self._text)

    def __str__(self) -> str:
        return f"TextAnalyzer(v={self._analysis_version}, length={len(self._text)})"

class RegexMixin:
    """Mixin implementing Variant 27 regex-specific tasks."""
    def find_uppercase_english(self) -> List[str]:
        """Returns all uppercase English letters in the text."""
        return re.findall(r'[A-Z]', self._text)

    def replace_pattern_rbc(self) -> str:
        """Replaces sequence 'р...рb...bc...c' with 'ddd'.
        Uses Cyrillic 'р' and 'с', Latin 'b' as per task description.
        """
        pattern = r'р+bb+с+'
        return re.sub(pattern, 'ddd', self._text)

class StatsMixin:
    """Mixin implementing general text statistics."""
    def count_sentences(self) -> int:
        """Counts total sentences (split by . ! ?)."""
        return len([s for s in re.split(r'[.!?]+', self._text) if s.strip()])

    def count_sentence_types(self) -> Dict[str, int]:
        """Counts declarative, interrogative, and imperative sentences."""
        return {
            "declarative (.)": len(re.findall(r'[^.!?]*\.', self._text)),
            "interrogative (?)": len(re.findall(r'[^.!?]*\?', self._text)),
            "imperative (!)": len(re.findall(r'[^.!?]*!', self._text))
        }

    def avg_sentence_length_words_only(self) -> float:
        """Average sentence length in characters (only words counted)."""
        sents = re.split(r'[.!?]+', self._text)
        total_chars, count = 0, 0
        for sent in sents:
            words = re.findall(r'\b\w+\b', sent)
            if words:
                total_chars += sum(len(w) for w in words)
                count += 1
        return total_chars / count if count else 0.0

    def avg_word_length(self) -> float:
        """Average word length in the entire text."""
        words = re.findall(r'\b\w+\b', self._text)
        return sum(len(w) for w in words) / len(words) if words else 0.0

    def count_smileys(self) -> int:
        """Counts valid smileys: [;:] + optional '-' + identical brackets (1+)."""
        # Explicit alternatives ensure brackets are identical within one match
        pattern = r'[;:][-]*(\(\)+|\)\)+|\[+|\]+)'
        return len(re.findall(pattern, self._text))

class AdvancedTextAnalyzer(BaseTextAnalyzer, RegexMixin, StatsMixin):
    """Main analyzer combining regex, stats, and variant-specific logic."""
    def __init__(self, text: str = ""):
        super().__init__(text)  # Inheritance chain initialization

    def analyze_all(self) -> Dict[str, Any]:
        """Executes all required analyses and caches results."""
        words = re.findall(r'\b\w+\b', self._text)
        self._results = {
            "uppercase_english": self.find_uppercase_english(),
            "replaced_text_preview": self.replace_pattern_rbc()[:100] + ("..." if len(self.replace_pattern_rbc())>100 else ""),
            "total_sentences": self.count_sentences(),
            "sentence_types": self.count_sentence_types(),
            "avg_sentence_len_words": round(self.avg_sentence_length_words_only(), 2),
            "avg_word_len": round(self.avg_word_length(), 2),
            "smiley_count": self.count_smileys(),
            "words_len_less_5": [w for w in words if len(w) < 5],
            "shortest_ending_d": min((w for w in words if w.endswith('d')), key=len, default="Not found"),
            "words_desc_len": sorted(words, key=len, reverse=True)
        }
        self._last_operation = "full_analysis"
        return self._results