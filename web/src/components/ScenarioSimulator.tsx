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
    <div className="bg-[#111113] rounded-sm shadow-[0_20px_50px_-10px_rgba(0,0,0,0.95),0_0_0_1px_rgba(255,255,255,0.03)] border border-[#232328] p-6 space-y-8 relative overflow-hidden group">
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#d48e4d]/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

      <h3 className="text-sm font-bold text-slate-100 tracking-wider uppercase border-b border-[#232328] pb-3">
        Scenario Simulator
      </h3>
      
      <div className="space-y-8">
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <label className="flex items-center gap-2 text-[11px] font-bold text-slate-400 uppercase tracking-widest">
              <Wind className="w-4 h-4 text-slate-500" />
              Wind Speed
            </label>
            <span className="text-xs font-mono font-bold bg-[#0a0a0b] text-[#d48e4d] px-2 py-1 border border-[#232328] rounded-sm shadow-inner">
              {windDelta > 0 ? '+' : ''}{windDelta.toFixed(1)} m/s
            </span>
          </div>
          <input 
            type="range" 
            min="-10" 
            max="10" 
            step="0.5"
            value={windDelta}
            onChange={(e) => onWindChange(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-[#0a0a0b] rounded-none appearance-none cursor-pointer border border-[#232328] accent-[#d48e4d] hover:accent-[#e09e5f] focus:outline-none focus:ring-1 focus:ring-[#d48e4d]/50 transition-all"
            style={{ WebkitAppearance: 'none' }}
          />
        </div>

        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <label className="flex items-center gap-2 text-[11px] font-bold text-slate-400 uppercase tracking-widest">
              <Sun className="w-4 h-4 text-slate-500" />
              Solar Radiation
            </label>
            <span className="text-xs font-mono font-bold bg-[#0a0a0b] text-[#d48e4d] px-2 py-1 border border-[#232328] rounded-sm shadow-inner">
              {solarDelta > 0 ? '+' : ''}{solarDelta.toFixed(0)} W/m²
            </span>
          </div>
          <input 
            type="range" 
            min="-200" 
            max="200" 
            step="10"
            value={solarDelta}
            onChange={(e) => onSolarChange(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-[#0a0a0b] rounded-none appearance-none cursor-pointer border border-[#232328] accent-[#d48e4d] hover:accent-[#e09e5f] focus:outline-none focus:ring-1 focus:ring-[#d48e4d]/50 transition-all"
            style={{ WebkitAppearance: 'none' }}
          />
        </div>
      </div>

      <button
        onClick={onSimulate}
        disabled={isLoading}
        className="w-full py-3 px-4 bg-[#17171a] border border-[#d48e4d]/50 hover:bg-[#d48e4d] hover:text-[#0a0a0b] active:bg-[#c27c3c] shadow-[0_0_15px_rgba(212,142,77,0.1)] hover:shadow-[0_0_25px_rgba(212,142,77,0.4)] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-[#17171a] disabled:hover:text-[#d48e4d] disabled:hover:shadow-[0_0_15px_rgba(212,142,77,0.1)] text-[#d48e4d] font-bold uppercase tracking-widest text-xs rounded-sm transition-all duration-300 flex justify-center items-center gap-3"
      >
        {isLoading ? (
          <>
            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
            <span className="font-mono">Processing...</span>
          </>
        ) : (
          "Run Simulation"
        )}
      </button>
    </div>
  );
};
