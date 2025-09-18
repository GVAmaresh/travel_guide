# import re
# from typing import Dict, List, Optional, TypedDict

# class ResponseCheckResult(TypedDict):
#     is_appropriate: bool
#     issues_found: List[str] 
#     sanitized_text: str 

# class ResponseSafetyFilter:
#     def __init__(self):
#         self.profanity: List[str] = self._load_profanity_list()
#         self.pii_patterns: Dict[str, re.Pattern] = self._build_pii_patterns()

#     def _load_profanity_list(self) -> List[str]:
#         return [
#             'hell', 'damn', 'bitch', 'asshole', 'fuck', 'shit' 
#         ]

#     def _build_pii_patterns(self) -> Dict[str, re.Pattern]:
#         return {
#             "EMAIL": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
#             "PHONE_NUMBER": re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'),
#             "CREDIT_CARD": re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
#         }
    
#     def check_response(self, text: str) -> ResponseCheckResult:
#         issues_found: List[str] = []
#         sanitized_text = text
#         for word in self.profanity:
#             pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
#             if pattern.search(sanitized_text):
#                 if "Profanity" not in issues_found:
#                     issues_found.append("Profanity")
#                 sanitized_text = pattern.sub('*' * len(word), sanitized_text)

#         for pii_type, pattern in self.pii_patterns.items():
#             if pattern.search(sanitized_text):
#                 if "Potential_PII" not in issues_found:
#                     issues_found.append("Potential_PII")
#                 sanitized_text = pattern.sub(f"[{pii_type}_REDACTED]", sanitized_text)
        
#         result: ResponseCheckResult = {
#             "is_appropriate": not bool(issues_found),
#             "issues_found": issues_found,
#             "sanitized_text": sanitized_text
#         }

#         return result