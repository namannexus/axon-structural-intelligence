import React, { useState } from 'react';
import FloorPlan3D from './components/FloorPlan3D';
import { analyzeFloorplan } from './services/api';
import './index.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResults(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await analyzeFloorplan(selectedFile);
      setResults(data);
    } catch (err) {
      setError("Failed to analyze floorplan. Ensure the Python backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans pb-20 selection:bg-blue-200">
      
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 tracking-tight flex items-center gap-2">
              <span className="text-blue-600">🏗️</span> Autonomous Structural Intelligence
            </h1>
            <p className="text-sm text-gray-500 mt-1">AI-driven geometry extraction and material analysis</p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Upload Section */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-8 max-w-3xl mx-auto flex flex-col sm:flex-row items-center gap-4 transition-all hover:shadow-md">
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleFileChange} 
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 transition-colors cursor-pointer"
          />
          <button 
            onClick={handleUpload} 
            disabled={!selectedFile || loading}
            className={`w-full sm:w-auto px-6 py-2.5 rounded-full font-medium text-white transition-all flex items-center justify-center min-w-[180px]
              ${(!selectedFile || loading) ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 hover:shadow-lg active:scale-95'}`}
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </>
            ) : "Generate Analysis"}
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded-md max-w-3xl mx-auto">
            <div className="flex">
              <div className="flex-shrink-0">⚠️</div>
              <div className="ml-3">
                <p className="text-sm text-red-700 font-medium">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Results Grid - Responsive 1 to 2 columns */}
        {results && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
            
            {/* LEFT COLUMN: Visuals */}
            <div className="flex flex-col gap-8">
              
              {/* Image Preview Card */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden group">
                <div className="bg-gray-50 px-4 py-3 border-b border-gray-100">
                  <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider">Original Floorplan</h3>
                </div>
                <div className="p-4 flex justify-center bg-gray-100/50">
                  <img src={previewUrl} alt="Preview" className="max-h-[300px] object-contain rounded-lg shadow-sm group-hover:scale-[1.02] transition-transform duration-300" />
                </div>
              </div>
              
              {/* 3D Render Card */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col">
                <div className="bg-gray-50 px-4 py-3 border-b border-gray-100 flex justify-between items-center">
                  <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider">3D Structural Model</h3>
                  <span className="text-xs text-gray-400 bg-white px-2 py-1 rounded border border-gray-200 shadow-sm">
                    Scroll: Zoom | Drag: Rotate
                  </span>
                </div>
                {/* 3D Container - Dark theme for professional CAD look */}
                <div className="relative w-full h-[450px] bg-slate-900 cursor-move">
                  <FloorPlan3D graphData={results.graph} />
                </div>
              </div>

            </div>

            {/* RIGHT COLUMN: Intelligence */}
            <div className="flex flex-col gap-8">
              
              {/* AI Report Card */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                <div className="bg-blue-50 px-4 py-3 border-b border-blue-100 flex items-center gap-2">
                  <span>🧠</span>
                  <h3 className="text-sm font-semibold text-blue-900 uppercase tracking-wider">Engineering Report</h3>
                </div>
                <div className="p-6 space-y-6">
                  <div>
                    <h4 className="text-xs font-bold text-gray-400 uppercase mb-2">Executive Summary</h4>
                    <p className="text-gray-700 leading-relaxed text-sm">{results?.explanation?.summary || "No summary available."}</p>
                  </div>
                  
                  <div>
                    <h4 className="text-xs font-bold text-gray-400 uppercase mb-2">Material Reasoning</h4>
                    <p className="text-gray-700 leading-relaxed text-sm">{results?.explanation?.material_reasoning || "No reasoning available."}</p>
                  </div>

                  <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mt-4">
                    <h4 className="text-xs font-bold text-amber-800 uppercase mb-2 flex items-center gap-1">
                      <span>⚠️</span> Structural Risks
                    </h4>
                    <p className="text-amber-900 leading-relaxed text-sm">{results?.explanation?.structural_risks || "No risks detected."}</p>
                  </div>
                </div>
              </div>

              {/* Materials Card */}
              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col max-h-[600px]">
                <div className="bg-gray-50 px-4 py-3 border-b border-gray-100 flex items-center gap-2 sticky top-0">
                  <span>🧱</span>
                  <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider">Material Recommendations</h3>
                </div>
                
                <div className="overflow-y-auto p-4 space-y-4 custom-scrollbar">
                  {results?.materials?.recommendations ? (
                    results.materials.recommendations.map((rec, index) => (
                      <div key={index} className="bg-white border border-gray-100 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow">
                        <h4 className="font-semibold text-gray-800 mb-3 border-b border-gray-50 pb-2">{rec.element}</h4>
                        <div className="space-y-3">
                          {rec.recommended_materials?.slice(0, 3).map((mat, idx) => (
                            <div key={idx} className="flex items-center justify-between group">
                              <span className="text-sm font-medium text-gray-600 group-hover:text-blue-600 transition-colors">
                                {idx + 1}. {mat.material}
                              </span>
                              <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${
                                idx === 0 ? 'bg-green-100 text-green-800' : 
                                idx === 1 ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                              }`}>
                                {(mat.score * 100).toFixed(0)}% Match
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-gray-500 text-sm italic text-center py-8">Material data is currently unavailable.</p>
                  )}
                </div>
              </div>

            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;