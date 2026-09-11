import React from 'react';
import Plot from 'react-plotly.js';

interface ForecastPoint {
  timestamp: string;
  median_price_eur: number;
  lower_bound_05_eur: number;
  upper_bound_95_eur: number;
  renewable_generation_mw: number;
}

interface Props {
  data: ForecastPoint[];
}

export const ForecastFanChart: React.FC<Props> = ({ data }) => {
  const timestamps = data.map(d => d.timestamp);
  const medians = data.map(d => d.median_price_eur);
  const lowers = data.map(d => d.lower_bound_05_eur);
  const uppers = data.map(d => d.upper_bound_95_eur);

  return (
    <div className="w-full h-[400px] bg-white rounded-xl shadow-sm border border-slate-200 p-4">
      <Plot
        data={[
          {
            x: timestamps,
            y: lowers,
            type: 'scatter',
            mode: 'lines',
            line: { width: 0 },
            showlegend: false,
            hoverinfo: 'skip',
          },
          {
            x: timestamps,
            y: uppers,
            type: 'scatter',
            mode: 'lines',
            fill: 'tonexty',
            fillcolor: 'rgba(59, 130, 246, 0.2)', // Tailwind blue-500 with opacity
            line: { width: 0 },
            name: '90% Confidence Interval',
            hoverinfo: 'skip',
          },
          {
            x: timestamps,
            y: medians,
            type: 'scatter',
            mode: 'lines+markers',
            line: { color: '#2563eb', width: 3 }, // Tailwind blue-600
            marker: { size: 6 },
            name: 'Median Price',
          }
        ]}
        layout={{
          autosize: true,
          margin: { t: 20, r: 20, b: 40, l: 40 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          xaxis: { 
            gridcolor: '#e2e8f0', // slate-200
            tickfont: { color: '#64748b' } // slate-500
          },
          yaxis: { 
            title: 'Price (€/MWh)',
            gridcolor: '#e2e8f0',
            tickfont: { color: '#64748b' },
            titlefont: { color: '#475569' }
          },
          legend: { orientation: 'h', y: -0.2 }
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
    </div>
  );
};
