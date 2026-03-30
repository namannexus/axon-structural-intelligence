import React, { useState } from 'react';
import FloorPlan3D from './components/FloorPlan3D';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
      const res = await fetch('http://127.0.0.1:8000/process-floorplan', { method: 'POST', body: formData });
      const data = await res.json();
      setResults(data);
    } catch (err) { alert("Backend Error"); }
    setLoading(false);
  };

  const downloadPDF = async () => {
    const res = await fetch('http://127.0.0.1:8000/generate-report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(results),
    });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = "Structural_Report.pdf";
    a.click();
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-200">
        <header className="bg-slate-900 p-6 text-white flex justify-between items-center">
          <h1 className="text-xl font-bold">🏗️ AXON Intelligence</h1>
          {results && (
            <button onClick={downloadPDF} className="bg-blue-600 px-4 py-2 rounded-lg font-bold">📥 Download PDF</button>
          )}
        </header>

        <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-8">
          <section className="space-y-4">
            <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} className="block w-full border p-2 rounded" />
            <button onClick={handleUpload} disabled={loading} className="w-full bg-blue-600 text-white p-3 rounded font-bold">
              {loading ? "Analyzing..." : "Analyze Floorplan"}
            </button>
            {results && (
              <div className="h-[400px] border rounded-xl overflow-hidden bg-slate-100">
                <FloorPlan3D graphData={results.graph} />
              </div>
            )}
          </section>

          <section>
            {results ? (
              <div className="space-y-6">
                <div>
                  <h3 className="font-bold text-gray-400 uppercase text-xs">Summary</h3>
                  <p className="text-sm">{results.explanation.summary}</p>
                </div>
                <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
                  <h3 className="font-bold text-amber-800 text-xs uppercase">Risks</h3>
                  <p className="text-sm text-amber-900">{results.explanation.structural_risks}</p>
                </div>
              </div>
            ) : <p className="text-gray-400 italic">Upload a file to begin analysis.</p>}
          </section>
        </div>
      </div>
    </div>
  );
}
export default App;