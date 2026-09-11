import { useEffect, useState } from 'react';
import axios from 'axios';
import { Activity, Leaf } from 'lucide-react';
import { ForecastFanChart } from './components/ForecastFanChart';
import { ScenarioSimulator } from './components/ScenarioSimulator';
import { MetricBar } from './components/MetricBar';

interface ForecastPoint {
  timestamp: string;
  median_price_eur: number;
  lower_bound_05_eur: number;
  upper_bound_95_eur: number;
  renewable_generation_mw: number;
}

const API_BASE_URL = 'http://localhost:8000/api/v1/forecast';

function App() {
  const [data, setData] = useState<ForecastPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [windDelta, setWindDelta] = useState(0);
  const [solarDelta, setSolarDelta] = useState(0);
  const [showRenewables, setShowRenewables] = useState(false);

  const fetchLatest = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE_URL}/latest?bidding_zone=DE_LU&horizon_hours=48`);
      setData(res.data.points);
    } catch (err) {
      console.error("Failed to fetch latest forecast", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE_URL}/simulate`, {
        bidding_zone: "DE_LU",
        horizon_hours: 48,
        wind_speed_delta: windDelta,
        solar_radiation_delta: solarDelta
      });
      setData(res.data.points);
    } catch (err) {
      console.error("Failed to simulate forecast", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLatest();
  }, []);

  return (
    <div className="min-h-screen text-slate-200 font-sans">
      
      {/* Sticky Navbar */}
      <nav className="sticky top-0 z-50 backdrop-blur-[20px] bg-[#0a0a0b]/60 border-b border-[#232328] px-4 md:px-8 py-3 shadow-lg">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            {/* Copper brand badge */}
            <div className="p-2 bg-[#111113] border border-[#232328] rounded-sm text-[#d48e4d] shadow-[0_4px_12px_rgba(0,0,0,0.5)]">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-slate-100 tracking-wider uppercase">EcoGrid-Cast</h1>
            </div>
          </div>
          
          {/* Status Pill */}
          <div className="flex items-center gap-3 px-3 py-1.5 bg-[#111113] border border-[#232328] rounded-sm shadow-inner">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="font-mono text-[10px] text-emerald-500 uppercase tracking-widest">Grid Bus Online</span>
          </div>
        </div>
      </nav>

      <div className="p-4 md:p-8">
        <div className="max-w-7xl mx-auto space-y-8">
          
          {/* Industrial Hero Section */}
          <div className="flex flex-col space-y-4 pb-8 border-b border-[#232328]/60">
            <div className="flex items-center gap-2 text-[#d48e4d] font-mono text-[11px] uppercase tracking-[0.25em]">
              <div className="w-1.5 h-1.5 bg-[#d48e4d]"></div>
              SYSTEM IDENTIFIER // DE-LU GRID
            </div>
            
            <h2 className="font-black text-6xl md:text-7xl tracking-[-0.04em] leading-[0.88] flex flex-col">
              <span className="bg-gradient-to-b from-white to-zinc-400 bg-clip-text text-transparent">
                PROBABILISTIC
              </span>
              <span className="bg-gradient-to-b from-zinc-300 to-zinc-600 bg-clip-text text-transparent">
                DISPATCH
              </span>
            </h2>
            
            <p className="text-sm text-zinc-400 max-w-2xl font-sans pt-2">
              Conformal day-ahead wholesale electricity price calibration and renewable generation forecasting. Precise, calibrated, and rigorously bounded under extreme market volatility.
            </p>
          </div>

          {/* Metric Summary Bar */}
          <MetricBar />

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 flex flex-col space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-slate-100 uppercase tracking-wide">
                  48-Hour Price Forecast
                </h2>
                <button
                  onClick={() => setShowRenewables(!showRenewables)}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-sm text-[11px] font-mono transition-all duration-200 border ${
                    showRenewables 
                      ? 'bg-[#17171a] text-[#10b981] border-[#10b981]/30 shadow-[inset_0_1px_0_rgba(255,255,255,0.05)]' 
                      : 'bg-[#111113] text-slate-400 border-[#232328] hover:border-slate-500 hover:text-slate-300'
                  }`}
                >
                  <Leaf className={`w-3.5 h-3.5 ${showRenewables ? 'text-[#10b981]' : 'text-slate-500'}`} />
                  {showRenewables ? 'RENEWABLES: ON' : 'RENEWABLES: OFF'}
                </button>
              </div>
              
              {loading && data.length === 0 ? (
                <div className="w-full h-[420px] bg-[#111113] rounded-sm animate-pulse flex items-center justify-center border border-[#232328] shadow-[0_20px_50px_-10px_rgba(0,0,0,0.95),0_0_0_1px_rgba(255,255,255,0.03)]">
                  <div className="flex flex-col items-center gap-3">
                    <div className="w-8 h-8 border-4 border-[#232328] border-t-[#d48e4d] rounded-full animate-spin"></div>
                    <p className="text-slate-500 font-mono text-xs uppercase tracking-widest">Fetching telemetry...</p>
                  </div>
                </div>
              ) : (
                <div className="bg-[#111113] p-1 rounded-sm shadow-[0_20px_50px_-10px_rgba(0,0,0,0.95),0_0_0_1px_rgba(255,255,255,0.03)] border border-[#232328] relative group">
                  {/* Copper hairline highlight on hover */}
                  <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#d48e4d]/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  <ForecastFanChart data={data} showRenewables={showRenewables} />
                </div>
              )}
            </div>
            
            <div className="flex flex-col space-y-6">
              <ScenarioSimulator 
                windDelta={windDelta}
                solarDelta={solarDelta}
                onWindChange={setWindDelta}
                onSolarChange={setSolarDelta}
                onSimulate={handleSimulate}
                isLoading={loading}
              />
              
              <div className="p-5 bg-[#111113] border border-[#232328] rounded-sm shadow-[0_20px_50px_-10px_rgba(0,0,0,0.95),0_0_0_1px_rgba(255,255,255,0.03)] relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-32 h-32 bg-[#d48e4d]/5 rounded-full blur-3xl -mr-10 -mt-10 transition-transform group-hover:scale-150 duration-700"></div>
                <h4 className="font-bold text-slate-300 mb-2 uppercase text-xs tracking-wider">System Notes</h4>
                <p className="text-[11px] text-slate-500 leading-relaxed font-mono relative z-10">
                  Adjust the wind and solar sliders to perturb the base weather forecast. Increased renewables typically suppress median day-ahead prices and tighten conformal intervals due to grid merit-order effects.
                </p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;
