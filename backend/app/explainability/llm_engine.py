import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.core.models import ExplanationReport

class ExplainabilityEngine:
    def __init__(self, graph_path: str, recommendations_path: str):
        # Load environment variables (API Key)
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if self.api_key and self.api_key != "your_api_key_here":
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.use_ai = True
        else:
            self.use_ai = False
            print("⚠️ WARNING: No valid Gemini API Key found. Using rule-based fallback mode.")

        # Load the data we generated in Modules 2 & 4
        with open(graph_path, 'r') as f:
            self.graph_data = json.load(f)
            
        with open(recommendations_path, 'r') as f:
            self.recommendations_data = json.load(f)

    def _generate_fallback_explanation(self) -> str:
        """A hardcoded fallback so your demo doesn't crash if the Wi-Fi drops."""
        report = ExplanationReport(
            summary="Floor plan analyzed successfully. Multiple load-bearing and partition walls detected.",
            material_reasoning="High-Strength Steel and Hollow Concrete Blocks were selected based on a 50/50 tradeoff between cost efficiency and structural strength.",
            structural_risks="Warning: Ensure load-bearing walls are properly aligned. Fallback mode active; connect API for deep analysis."
        )
        return report.model_dump_json(indent=2)

    def generate_explanation(self) -> str:
        """Sends data to the LLM to generate a plain English engineering report."""
        if not self.use_ai:
            return self._generate_fallback_explanation()

        # 1. Prepare Data Summary for the LLM
        # Sending 50+ walls takes too many tokens. We summarize the logic instead.
        load_bearing_count = sum(1 for v in self.graph_data['wall_types'].values() if v == 'load-bearing')
        partition_count = sum(1 for v in self.graph_data['wall_types'].values() if v == 'partition')
        
        # Grab a sample recommendation to show the LLM the math
        sample_rec = self.recommendations_data['recommendations'][0]
        
        # 2. Construct the Prompt (Prompt Engineering)
        prompt = f"""
        You are an expert AI Structural Engineer and System Architect.
        I have run a computer vision and physics analysis pipeline on a building floor plan.
        
        DATA SUMMARY:
        - Load-Bearing Walls Detected: {load_bearing_count}
        - Partition Walls Detected: {partition_count}
        - Sample Recommendation for {sample_rec['element']}: 
          {json.dumps(sample_rec['recommended_materials'], indent=2)}
          (Scores are based on a 50% Cost / 50% Strength tradeoff algorithm).

        TASK:
        Generate a professional, non-generic plain-English explanation of this analysis. 
        Format your response strictly as a JSON object with the following keys:
        - "summary": A brief overview of the floor plan structure.
        - "material_reasoning": Explain why specific materials (like Steel or Hollow Blocks) scored highly based on cost vs strength tradeoffs.
        - "structural_risks": Mention 2 potential structural risks (e.g., unsupported spans, non-90-degree joints) that a builder should watch out for based on this automated analysis.
        
        Return ONLY valid JSON. No markdown formatting, no code blocks, just raw JSON.
        """

        try:
            # 3. Call the LLM
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            
            # Strip out markdown code block formatting if the LLM accidentally includes it
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:-3]
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:-3]
                
            # Validate output matches our Pydantic schema
            parsed_json = json.loads(raw_text)
            final_report = ExplanationReport(**parsed_json)
            
            return final_report.model_dump_json(indent=2)
            
        except Exception as e:
            print(f"❌ LLM Error: {e}. Switching to fallback.")
            return self._generate_fallback_explanation()