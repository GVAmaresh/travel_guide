# import re
# from datetime import datetime, timezone
# from typing import Dict, List, Optional, TypedDict

# class InputSafetyCheckResult(TypedDict):
#     is_safe: bool
#     category: Optional[str]
#     risk_level: Optional[str]
#     refusal_message: Optional[str]
#     confidence: float
#     timestamp: str

# class InputSafetyFilter:
#     def __init__(self):
#         self.risk_keywords: Dict[str, List[str]] = self._build_keyword_database()
#         self.refusal_messages: Dict[str, str] = self._create_refusal_messages()

#     def _build_keyword_database(self) -> Dict[str, List[str]]:
#         return {
#             'Illegal Drug/Substance Manufacturing': ['synthesize', 'cook', 'meth', '...'],
#             'Weapons and Explosives': ['bomb', 'explosive', 'detonate', '...'],
#             'Violence and Harm': ['kill', 'murder', 'assassinate', '...'],
#             'Hacking and Cybercrime': ['hack', 'crack password', 'bypass security', '...'],
#             'Discrimination and Hate': ['racial slur', 'ethnic slur', 'hate speech', '...']
#         }

#     def _create_refusal_messages(self) -> Dict[str, str]:
#         return {
#             'Illegal Drug/Substance Manufacturing': "I cannot provide information about manufacturing illegal substances...",
#             'Weapons and Explosives': "I cannot provide information on creating weapons or explosives...",
#             'Violence and Harm': "I cannot answer questions that involve violence or harming others...",
#             'Hacking and Cybercrime': "I cannot provide information on hacking or cybercrime...",
#             'Discrimination and Hate': "I will not generate content that promotes hate speech or discrimination...",
#             'General': "I cannot provide a response to this request. It falls outside my safety guidelines."
#         }
    
#     def _detect_category(self, text: str) -> Optional[str]:
#         text_lower = text.lower()
#         max_score = 0
#         detected_category = None
#         for category, keywords in self.risk_keywords.items():
#             score = sum(1 for keyword in keywords if keyword in text_lower)
#             threshold = 2
#             if category in ['Weapons and Explosives', 'Hacking and Cybercrime']:
#                 threshold = 1
#             if score > max_score and score >= threshold:
#                 max_score = score
#                 detected_category = category
#         return detected_category

#     def _check_pattern_matches(self, text: str) -> List[str]:
#         dangerous_patterns = [
#             re.compile(r'\bhow (do i|can i|to) (make|create|build)\b', re.IGNORECASE),
#             re.compile(r'\b(step.?by.?step|detailed|instructions)\b', re.IGNORECASE),
#             re.compile(r'\bwithout (getting caught|detection)\b', re.IGNORECASE),
#         ]
#         return [p.pattern for p in dangerous_patterns if p.search(text)]

#     def check_query(self, query: str) -> InputSafetyCheckResult:
#         result: InputSafetyCheckResult = {
#             "is_safe": True, "category": None, "risk_level": None,
#             "refusal_message": None, "confidence": 0.0,
#             "timestamp": datetime.now(timezone.utc).isoformat()
#         }
#         detected_category = self._detect_category(query)
#         if detected_category:
#             result['is_safe'] = False
#             result['category'] = detected_category
#             result['risk_level'] = 'High'
#             result['confidence'] = 0.80
#         pattern_matches = self._check_pattern_matches(query)
#         if pattern_matches and result['category']:
#             result['risk_level'] = 'Critical'
#             result['confidence'] = min(0.95, result['confidence'] + 0.15)
#         if not result['is_safe']:
#             result['refusal_message'] = self.refusal_messages.get(result['category'], self.refusal_messages['General'])
#         return result