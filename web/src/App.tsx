import { useEffect, useState } from 'react';
import axios from 'axios';
import { Activity } from 'lucide-react';
import { ForecastFanChart } from './components/ForecastFanChart';
import { ScenarioSimulator } from './components/ScenarioSimulator';

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
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-200">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl text-white shadow-lg shadow-indigo-500/30">
              <Activity className="w-8 h-8" />
            </div>
            <div>
              <h1 className="text-3xl font-extrabold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent tracking-tight">EcoGrid-Cast</h1>
              <p className="text-slate-500 font-medium mt-1">Conformal Forecasts & Simulations</p>
            </div>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 flex flex-col space-y-4">
            <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
              48-Hour Price Forecast
            </h2>
            {loading && data.length === 0 ? (
              <div className="w-full h-[400px] bg-white rounded-2xl animate-pulse flex items-center justify-center border border-slate-200 shadow-sm">
                <div className="flex flex-col items-center gap-3">
                  <div className="w-8 h-8 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
                  <p className="text-slate-400 font-medium">Fetching realtime forecasts...</p>
                </div>
              </div>
            ) : (
              <div className="bg-white p-2 rounded-2xl shadow-sm border border-slate-200 transition-all duration-300 hover:shadow-md">
                <ForecastFanChart data={data} />
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
            
            <div className="p-5 bg-gradient-to-br from-blue-50 to-indigo-50/50 border border-blue-100/50 rounded-2xl shadow-sm relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl -mr-10 -mt-10 transition-transform group-hover:scale-150 duration-700"></div>
              <h4 className="font-semibold text-blue-900 mb-2">How it works</h4>
              <p className="text-sm text-blue-800/80 leading-relaxed relative z-10">
                Adjust the wind and solar sliders to perturb the base weather forecast. Increased renewables typically suppress median day-ahead prices and tighten conformal intervals due to grid merit-order effects.
              </p>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
