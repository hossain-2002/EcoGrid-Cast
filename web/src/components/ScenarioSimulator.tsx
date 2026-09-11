import React from 'react';
import { Wind, Sun } from 'lucide-react';

interface Props {
  windDelta: number;
  solarDelta: number;
  onWindChange: (val: number) => void;
  onSolarChange: (val: number) => void;
  onSimulate: () => void;
  isLoading: boolean;
}

export const ScenarioSimulator: React.FC<Props> = ({
  windDelta,
  solarDelta,
  onWindChange,
  onSolarChange,
  onSimulate,
  isLoading
}) => {
  return (
    <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl border border-white/20 p-6 space-y-6">
      <h3 className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-sky-500 bg-clip-text text-transparent">
        Weather Scenario
      </h3>
      
      <div className="space-y-6">
        <div className="space-y-3 group">
          <div className="flex justify-between items-center transition-transform group-hover:translate-x-1">
            <label className="flex items-center gap-2 text-sm font-semibold text-slate-700">
              <Wind className="w-5 h-5 text-sky-500" />
              Wind Speed
            </label>
            <span className="text-sm font-bold bg-sky-100 text-sky-700 px-2.5 py-1 rounded-full">
              {windDelta > 0 ? '+' : ''}{windDelta} m/s
            </span>
          </div>
          <input 
            type="range" 
            min="-10" 
            max="10" 
            step="0.5"
            value={windDelta}
            onChange={(e) => onWindChange(parseFloat(e.target.value))}
            className="w-full h-2.5 bg-slate-200 rounded-full appearance-none cursor-pointer accent-sky-500 hover:accent-sky-600 transition-all"
          />
        </div>

        <div className="space-y-3 group">
          <div className="flex justify-between items-center transition-transform group-hover:translate-x-1">
            <label className="flex items-center gap-2 text-sm font-semibold text-slate-700">
              <Sun className="w-5 h-5 text-amber-500" />
              Solar Radiation
            </label>
            <span className="text-sm font-bold bg-amber-100 text-amber-700 px-2.5 py-1 rounded-full">
              {solarDelta > 0 ? '+' : ''}{solarDelta} W/m²
            </span>
          </div>
          <input 
            type="range" 
            min="-200" 
            max="200" 
            step="10"
            value={solarDelta}
            onChange={(e) => onSolarChange(parseFloat(e.target.value))}
            className="w-full h-2.5 bg-slate-200 rounded-full appearance-none cursor-pointer accent-amber-500 hover:accent-amber-600 transition-all"
          />
        </div>
      </div>

      <button
        onClick={onSimulate}
        disabled={isLoading}
        className="w-full py-3 px-4 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-700 hover:to-indigo-600 active:scale-[0.98] shadow-lg shadow-indigo-500/30 disabled:opacity-70 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-all duration-200 flex justify-center items-center gap-2"
      >
        {isLoading ? (
          <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
        ) : (
          "Run Simulation"
        )}
      </button>
    </div>
  );
};
