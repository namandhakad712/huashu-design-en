import { useState } from 'react'

const OUTPUT_TYPES = [
  { id: 'animation', label: 'Product Launch Animation', icon: '🎬' },
  { id: 'prototype', label: 'Clickable App Prototype', icon: '📱' },
  { id: 'deck', label: 'Editable PPT Deck', icon: '📊' },
  { id: 'infographic', label: 'Print-Grade Infographic', icon: '🖨️' },
]

const DESIGN_STYLES = [
  'Apple Gallery', 'Claude Brand', 'Linear Style', 'Vercel Design',
  'Notion Minimal', 'Figma Style', 'Stripe Clean', 'Airbnb Plus',
]

function App() {
  const [prompt, setPrompt] = useState('')
  const [outputType, setOutputType] = useState('animation')
  const [style, setStyle] = useState('')
  const [brandAssets, setBrandAssets] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [result, setResult] = useState(null)

  const handleGenerate = async () => {
    if (!prompt.trim()) return
    setIsGenerating(true)
    
    // Simulate generation - in real impl, would call Kimi CLI
    setTimeout(() => {
      setIsGenerating(false)
      setResult({
        html: '/demos/hero-animation-v9.html',
        preview: 'Animation generated successfully!'
      })
    }, 2000)
  }

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) setBrandAssets(file.name)
  }

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 p-6 flex flex-col">
        <h1 className="text-xl font-bold mb-8">
          <span className="text-[#D97757]">Huashu</span> Workbench
        </h1>
        
        <nav className="space-y-2 mb-8">
          <a href="#" className="block px-3 py-2 rounded-lg bg-gray-100 font-medium">
            New Design
          </a>
          <a href="#" className="block px-3 py-2 rounded-lg hover:bg-gray-50 text-gray-600">
            Recent Projects
          </a>
          <a href="#" className="block px-3 py-2 rounded-lg hover:bg-gray-50 text-gray-600">
            Templates
          </a>
          <a href="#" className="block px-3 py-2 rounded-lg hover:bg-gray-50 text-gray-600">
            Brand Assets
          </a>
        </nav>

        <div className="mt-auto pt-6 border-t">
          <p className="text-xs text-gray-400">Powered by huashu-design skill</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-auto">
        <div className="max-w-3xl mx-auto">
          {/* Prompt Input */}
          <div className="mb-8">
            <label className="block text-sm font-medium mb-2">What do you want to create?</label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="e.g., Create a product launch animation for our AI coding assistant, showing the workflow from input to code output..."
              className="w-full h-32 p-4 border border-gray-200 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-[#D97757] focus:border-transparent text-base"
            />
          </div>

          {/* Output Type */}
          <div className="mb-8">
            <label className="block text-sm font-medium mb-3">Output Type</label>
            <div className="grid grid-cols-2 gap-3">
              {OUTPUT_TYPES.map((type) => (
                <button
                  key={type.id}
                  onClick={() => setOutputType(type.id)}
                  className={`p-4 rounded-xl border-2 text-left transition-all ${
                    outputType === type.id
                      ? 'border-[#D97757] bg-orange-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <span className="text-xl mr-2">{type.icon}</span>
                  <span className="font-medium">{type.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Design Style */}
          <div className="mb-8">
            <label className="block text-sm font-medium mb-3">Design Style (optional)</label>
            <div className="flex flex-wrap gap-2">
              {DESIGN_STYLES.map((s) => (
                <button
                  key={s}
                  onClick={() => setStyle(style === s ? '' : s)}
                  className={`px-4 py-2 rounded-full text-sm transition-all ${
                    style === s
                      ? 'bg-[#D97757] text-white'
                      : 'bg-white border border-gray-200 hover:border-gray-300'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          {/* Brand Assets */}
          <div className="mb-8">
            <label className="block text-sm font-medium mb-3">Brand Assets (optional)</label>
            <div className="border-2 border-dashed border-gray-200 rounded-xl p-6 text-center hover:border-gray-300 transition-colors cursor-pointer">
              <input
                type="file"
                onChange={handleFileUpload}
                className="hidden"
                id="brand-upload"
                accept=".zip,.png,.jpg,.svg"
              />
              <label htmlFor="brand-upload" className="cursor-pointer">
                {brandAssets ? (
                  <p className="text-[#D97757] font-medium">📎 {brandAssets}</p>
                ) : (
                  <p className="text-gray-400">Drop logo, colors, or UI screenshots here</p>
                )}
              </label>
            </div>
          </div>

          {/* Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={!prompt.trim() || isGenerating}
            className={`w-full py-4 rounded-xl font-semibold text-lg transition-all ${
              !prompt.trim() || isGenerating
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-[#D97757] text-white hover:bg-[#B85D3D]'
            }`}
          >
            {isGenerating ? 'Generating...' : 'Generate Design'}
          </button>

          {/* Result */}
          {result && (
            <div className="mt-8 p-6 bg-white rounded-xl border border-gray-200">
              <h3 className="font-semibold mb-3">✅ Generated Successfully</h3>
              <p className="text-gray-600">{result.preview}</p>
              <a
                href={result.html}
                target="_blank"
                className="inline-block mt-4 px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200"
              >
                View Output →
              </a>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App