import React from 'react';
import { ShieldCheck, MapPin, Zap } from 'lucide-react';

const cards = [
  {
    icon: ShieldCheck,
    label: 'Empirical Coverage',
    value: '91.2%',
    sub: 'Target: 90%',
    iconColor: 'text-slate-400',
    hoverColor: 'group-hover:text-[#d48e4d]',
  },
  {
    icon: MapPin,
    label: 'Bidding Zone',
    value: 'DE-LU',
    sub: 'Germany-Luxembourg',
    iconColor: 'text-slate-400',
    hoverColor: 'group-hover:text-[#d48e4d]',
  },
  {
    icon: Zap,
    label: 'Model Latency',
    value: '<50 ms',
    sub: 'Redis Cached',
    iconColor: 'text-slate-400',
    hoverColor: 'group-hover:text-[#d48e4d]',
  },
] as const;

export const MetricBar: React.FC = () => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className="group relative flex items-center gap-4 p-4 rounded-sm border border-[#232328] bg-[#111113] shadow-[0_20px_50px_-10px_rgba(0,0,0,0.95),0_0_0_1px_rgba(255,255,255,0.03)] overflow-hidden transition-all duration-300 hover:border-[#3a3a40]"
        >
          {/* Copper hairline highlight on hover */}
          <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#d48e4d]/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          <div className="p-2.5 rounded-sm bg-[#17171a] border border-[#232328] shadow-inner transition-colors duration-300">
            <card.icon className={`w-5 h-5 ${card.iconColor} ${card.hoverColor} transition-colors duration-300`} />
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">{card.label}</span>
            <div className="flex items-baseline gap-2 mt-0.5">
              <span className="text-xl font-mono text-slate-200">{card.value}</span>
              <span className="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded-sm bg-[#0a0a0b] text-slate-400 border border-[#232328] uppercase">{card.sub}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
