# app/utils/text_processing.py
import re
from typing import Dict, List, Optional
import openai
from ..config import Settings

async def generate_title(case_description: str) -> str:
    """Generate a brief title from the case description."""
    try:
        client = openai.OpenAI(api_key=Settings().openai_api_key)
        messages = [
            {
                "role": "system",
                "content": "You are a medical assistant that generates brief (4-6 words) clinical case titles. Make them professional and medical in nature."
            },
            {
                "role": "user",
                "content": f"Generate a brief clinical case title from this description:\n{case_description}"
            }
        ]
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=50,
            temperature=0.7
        )
        
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip().replace('"', '')
        else:
            return "Case Review"
            
    except Exception as e:
        return "Case Review"

def extract_sections(text: str, selected_capabilities: List[str]) -> Dict[str, any]:
    """Extract different sections from the generated text."""
    try:
        sections = {
            "brief_description": "",
            "capabilities": {},
            "reflection": "",
            "learning_needs": ""
        }
        
        # Extract brief description
        summary_pattern = r"Brief Description:\s*(.*?)(?=\n\n|$)"
        summary_match = re.search(summary_pattern, text, re.DOTALL)
        if summary_match:
            sections["brief_description"] = summary_match.group(1).strip()
        
        # Extract capabilities - handle both formats
        for cap_name in selected_capabilities:
            # Try multiple patterns to match different formats
            patterns = [
                # Pattern 1: Full format with "Capability:" prefix and "Justification:"
                f"Capability: {re.escape(cap_name)}.*?Justification.*?:(.*?)(?=Capability:|Reflection:|Learning needs|$)",
                # Pattern 2: Just capability name with colon
                f"{re.escape(cap_name)}:(.*?)(?=\n\n[A-Za-z]|Reflection:|Learning needs|$)",
                # Pattern 3: Just capability name without colon
                f"{re.escape(cap_name)}\n(.*?)(?=\n\n[A-Za-z]|Reflection:|Learning needs|$)"
            ]
            
            content = None
            for pattern in patterns:
                match = re.search(pattern, text, re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    break
            
            if content:
                sections["capabilities"][cap_name] = content
            else:
                sections["capabilities"][cap_name] = ""
        
        # Extract reflection (handle with or without question mark)
        reflection_patterns = [
            r"Reflection: What will I maintain, improve or stop\?(.*?)(?=Learning needs|$)",
            r"Reflection: What will I maintain, improve or stop(.*?)(?=Learning needs|$)",
            r"Reflection:(.*?)(?=Learning needs|$)"
        ]
        
        for pattern in reflection_patterns:
            reflection_match = re.search(pattern, text, re.DOTALL)
            if reflection_match:
                sections["reflection"] = reflection_match.group(1).strip()
                break
        
        # Extract learning needs
        learning_pattern = r"Learning needs identified from this event:(.*?)(?=$)"
        learning_match = re.search(learning_pattern, text, re.DOTALL)
        if learning_match:
            sections["learning_needs"] = learning_match.group(1).strip()
        
        return sections
    except Exception as e:
        raise Exception(f"Error extracting sections: {str(e)}")