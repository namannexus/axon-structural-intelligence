import os
from app.materials.analyzer import MaterialAnalyzer

def run_module_4():
    print("🚀 Initializing Material Analysis Engine...")
    
    # Ensure Module 2 output exists
    if not os.path.exists("structural_graph.json"):
        print("❌ Error: structural_graph.json not found. Run Module 2 first!")
        return

    with open("structural_graph.json", "r") as f:
        graph_json = f.read()
        
    analyzer = MaterialAnalyzer(graph_json)
    
    print("⚙️ Computing Cost vs Strength tradeoffs...")
    json_result = analyzer.analyze()
    
    print("✅ Analysis Complete! Output Data:")
    # Print preview
    print(json_result[:600] + "\n... [Output Truncated] ...\n")
    
    # Save to file to pass to Module 5 (LLM Engine)
    with open("material_recommendations.json", "w") as f:
        f.write(json_result)
    print("💾 Saved material analysis to 'material_recommendations.json'")

if __name__ == "__main__":
    run_module_4()