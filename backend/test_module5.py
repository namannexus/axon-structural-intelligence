import os
from app.explainability.llm_engine import ExplainabilityEngine

def run_module_5():
    print("🚀 Initializing Explainability Engine (LLM)...")
    
    graph_file = "structural_graph.json"
    recs_file = "material_recommendations.json"
    
    if not os.path.exists(graph_file) or not os.path.exists(recs_file):
        print("❌ Error: Missing JSON files. Please run Module 2 and Module 4 first!")
        return

    engine = ExplainabilityEngine(graph_path=graph_file, recommendations_path=recs_file)
    
    print("🧠 Prompting AI model for structural analysis and reasoning...")
    json_result = engine.generate_explanation()
    
    print("✅ Analysis Complete! Plain English Report:")
    print("-" * 50)
    print(json_result)
    print("-" * 50)
    
    # Save output
    with open("llm_explanation_report.json", "w") as f:
        f.write(json_result)
    print("💾 Saved explanation to 'llm_explanation_report.json'")

if __name__ == "__main__":
    run_module_5()