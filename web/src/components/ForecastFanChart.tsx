import React, { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';
import type { Data, Layout } from 'plotly.js-dist-min';

interface ForecastPoint {
  timestamp: string;
  median_price_eur: number;
  lower_bound_05_eur: number;
  upper_bound_95_eur: number;
  renewable_generation_mw: number;
}

interface Props {
  data: ForecastPoint[];
  showRenewables: boolean;
}

export const ForecastFanChart: React.FC<Props> = ({ data, showRenewables }) => {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!chartRef.current || data.length === 0) return;

    const timestamps = data.map(d => d.timestamp);
    const medians = data.map(d => d.median_price_eur);
    const lowers = data.map(d => d.lower_bound_05_eur);
    const uppers = data.map(d => d.upper_bound_95_eur);
    const renewables = data.map(d => d.renewable_generation_mw / 1000); // MW -> GW

    const traces: Data[] = [
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
        fillcolor: 'rgba(212, 142, 77, 0.15)',
        line: { width: 0 },
        name: '90% Confidence Interval',
        hoverinfo: 'skip',
      },
      {
        x: timestamps,
        y: medians,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#d48e4d', width: 3, shape: 'spline' },
        name: 'Median Price (q0.50)',
        hovertemplate: '%{y:.1f} €/MWh<extra></extra>',
      },
    ];

    if (showRenewables) {
      traces.push({
        x: timestamps,
        y: renewables,
        type: 'scatter',
        mode: 'lines',
        line: { color: '#10b981', width: 2, dash: 'dot' },
        name: 'Renewable Gen. (GW)',
        yaxis: 'y2',
        hovertemplate: '%{y:.1f} GW<extra></extra>',
      });
    }

    const layout: Partial<Layout> = {
      autosize: true,
      margin: { t: 10, r: showRenewables ? 60 : 20, b: 50, l: 60 },
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      xaxis: {
        title: { text: 'TIME (CET)', font: { family: 'Inter', color: '#64748b', size: 10 } },
        gridcolor: '#232328',
        tickfont: { family: 'JetBrains Mono', color: '#94a3b8', size: 11 },
      },
      yaxis: {
        title: { text: 'DAY-AHEAD PRICE (€/MWh)', font: { family: 'Inter', color: '#64748b', size: 10 } },
        gridcolor: '#232328',
        tickfont: { family: 'JetBrains Mono', color: '#94a3b8', size: 11 },
      },
      legend: {
        orientation: 'h',
        y: -0.25,
        x: 0.5,
        xanchor: 'center',
        font: { family: 'Inter', size: 11, color: '#94a3b8' },
      },
      hovermode: 'x unified',
      hoverlabel: {
        bgcolor: '#111113',
        bordercolor: '#232328',
        font: { family: 'JetBrains Mono', color: '#e2e8f0', size: 12 },
      },
    };

    if (showRenewables) {
      layout.yaxis2 = {
        title: { text: 'RENEWABLE GENERATION (GW)', font: { family: 'Inter', color: '#10b981', size: 10 } },
        overlaying: 'y',
        side: 'right',
        gridcolor: 'rgba(16, 185, 129, 0.05)',
        tickfont: { family: 'JetBrains Mono', color: '#10b981', size: 11 },
        showgrid: false,
      };
    }

    const config = { displayModeBar: false, responsive: true };

    Plotly.newPlot(chartRef.current, traces, layout, config);

    // Cleanup
    return () => {
      if (chartRef.current) {
        Plotly.purge(chartRef.current);
      }
    };
  }, [data, showRenewables]);

  return (
    <div className="w-full h-[420px] bg-transparent rounded-sm p-4">
      <div ref={chartRef} className="w-full h-full" />
    </div>
  );
};
