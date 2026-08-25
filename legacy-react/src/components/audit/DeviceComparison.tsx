import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Plus, X, Check, AlertCircle, Info } from 'lucide-react';
import { Device, devices } from '../../data/devices';

export default function DeviceComparison() {
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  const toggleDevice = (id: string) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter(i => i !== id));
    } else if (selectedIds.length < 3) {
      setSelectedIds([...selectedIds, id]);
    }
  };

  const selectedDevices = devices.filter(d => selectedIds.includes(d.id));

  return (
    <div className="space-y-16">
      <div className="text-center max-w-2xl mx-auto">
        <h3 className="text-3xl font-serif text-neutral-900 mb-4 italic">Device Comparison Tool</h3>
        <p className="text-neutral-500 font-serif italic">Select up to three devices to compare clinical audit metrics and material specifications side-by-side.</p>
      </div>

      {/* Device Selection Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {devices.map((device) => {
          const isSelected = selectedIds.includes(device.id);
          return (
            <button
              key={device.id}
              onClick={() => toggleDevice(device.id)}
              disabled={!isSelected && selectedIds.length >= 3}
              className={`p-4 rounded-3xl border transition-all text-center group relative ${
                isSelected 
                  ? 'border-pink-500 bg-pink-50/50 ring-2 ring-pink-500/20' 
                  : 'border-neutral-100 bg-white hover:border-pink-200 disabled:opacity-50 disabled:cursor-not-allowed'
              }`}
            >
              <div className="aspect-square mb-3 bg-neutral-50 rounded-2xl flex items-center justify-center overflow-hidden">
                <img src={device.image} alt={device.name} className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all" />
              </div>
              <p className="text-[10px] font-bold text-neutral-900 truncate">{device.name}</p>
              {isSelected && (
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-pink-500 text-white rounded-full flex items-center justify-center shadow-lg">
                  <Check className="w-3 h-3" />
                </div>
              )}
            </button>
          );
        })}
      </div>

      {/* Comparison Table */}
      <AnimatePresence mode="wait">
        {selectedDevices.length > 0 ? (
          <motion.div
            key="comparison-table"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="overflow-hidden rounded-[2.5rem] border border-pink-100 bg-white shadow-xl shadow-pink-500/5"
          >
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse min-w-[800px]">
                <thead>
                  <tr className="bg-pink-50/30 border-b border-pink-100">
                    <th className="px-8 py-8 text-[11px] font-black text-pink-500 uppercase tracking-widest w-1/4">Audit Metric</th>
                    {selectedDevices.map(device => (
                      <th key={device.id} className="px-8 py-8 text-center">
                        <div className="flex flex-col items-center">
                          <span className="text-[10px] font-black text-neutral-400 uppercase tracking-widest mb-2">{device.brand}</span>
                          <span className="text-xl font-serif text-neutral-900 italic">{device.name}</span>
                        </div>
                      </th>
                    ))}
                    {Array.from({ length: 3 - selectedDevices.length }).map((_, i) => (
                      <th key={`empty-${i}`} className="px-8 py-8 text-center text-neutral-300 italic font-serif text-sm">
                        Empty Slot
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-pink-50">
                  {/* Summary Score */}
                  <tr className="bg-pink-50/10">
                    <td className="px-8 py-6">
                      <div className="font-bold text-neutral-900 text-sm uppercase tracking-tight">Audit Summary Score</div>
                      <div className="text-[9px] text-pink-400 font-black uppercase tracking-widest">MGV-1 COMPLIANCE</div>
                    </td>
                    {selectedDevices.map(device => (
                      <td key={device.id} className="px-8 py-6 text-center">
                        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-white border-2 border-pink-200 shadow-sm">
                          <span className="text-2xl font-serif font-bold text-pink-500">{device.auditScore}</span>
                        </div>
                      </td>
                    ))}
                    {Array.from({ length: 3 - selectedDevices.length }).map((_, i) => (
                      <td key={`empty-score-${i}`} className="px-8 py-6 text-center text-neutral-200">—</td>
                    ))}
                  </tr>

                  {/* Metrics Rows */}
                  {[
                    { key: 'vaporPathPurity', label: 'Vapor Path Purity', sub: 'Material Isolation' },
                    { key: 'thermalStability', label: 'Thermal Stability', sub: 'PTC Consistency' },
                    { key: 'bioCompatibility', label: 'Bio-Compatibility', sub: 'ISO 10993 Standards' },
                    { key: 'sanitization', label: 'Sanitization', sub: 'Autoclave Geometry' },
                    { key: 'traceability', label: 'Traceability', sub: 'Material Provenance' },
                  ].map((metric) => (
                    <tr key={metric.key} className="hover:bg-neutral-50/50 transition-colors">
                      <td className="px-8 py-6">
                        <div className="font-bold text-neutral-900 text-sm">{metric.label}</div>
                        <div className="text-[9px] text-neutral-400 font-bold uppercase tracking-widest">{metric.sub}</div>
                      </td>
                      {selectedDevices.map(device => (
                        <td key={device.id} className="px-8 py-6 text-center">
                          <div className="flex flex-col items-center gap-2">
                            <div className="w-full max-w-[100px] h-1.5 bg-neutral-100 rounded-full overflow-hidden">
                              <motion.div 
                                initial={{ width: 0 }}
                                animate={{ width: `${(device.metrics as any)[metric.key]}%` }}
                                className={`h-full ${(device.metrics as any)[metric.key] >= 95 ? 'bg-pink-500' : (device.metrics as any)[metric.key] >= 90 ? 'bg-amber-400' : 'bg-red-400'}`}
                              />
                            </div>
                            <span className="text-xs font-bold text-neutral-700">{(device.metrics as any)[metric.key]}%</span>
                          </div>
                        </td>
                      ))}
                      {Array.from({ length: 3 - selectedDevices.length }).map((_, i) => (
                        <td key={`empty-metric-${i}`} className="px-8 py-6 text-center text-neutral-200">—</td>
                      ))}
                    </tr>
                  ))}

                  {/* Specs Rows */}
                  <tr>
                    <td className="px-8 py-6 bg-neutral-50/50">
                      <div className="font-bold text-neutral-900 text-sm">Primary Materials</div>
                      <div className="text-[9px] text-neutral-400 font-bold uppercase tracking-widest">AIRPATH COMPOSITION</div>
                    </td>
                    {selectedDevices.map(device => (
                      <td key={device.id} className="px-8 py-6 text-center text-xs text-neutral-600 italic font-serif leading-relaxed">
                        {device.specs.materials.join(', ')}
                      </td>
                    ))}
                    {Array.from({ length: 3 - selectedDevices.length }).map((_, i) => (
                      <td key={`empty-materials-${i}`} className="px-8 py-6 text-center text-neutral-200">—</td>
                    ))}
                  </tr>

                  <tr>
                    <td className="px-8 py-6 bg-neutral-50/50">
                      <div className="font-bold text-neutral-900 text-sm">Heating Technology</div>
                      <div className="text-[9px] text-neutral-400 font-bold uppercase tracking-widest">THERMODYNAMIC METHOD</div>
                    </td>
                    {selectedDevices.map(device => (
                      <td key={device.id} className="px-8 py-6 text-center text-xs text-neutral-600 font-serif">
                        {device.specs.heatingType}
                      </td>
                    ))}
                    {Array.from({ length: 3 - selectedDevices.length }).map((_, i) => (
                      <td key={`empty-heating-${i}`} className="px-8 py-6 text-center text-neutral-200">—</td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="empty-state"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="h-64 border-2 border-dashed border-pink-100 rounded-[2.5rem] flex flex-col items-center justify-center text-neutral-400 italic font-serif"
          >
            <Plus className="w-8 h-8 mb-4 opacity-20" />
            <p>Select devices from the grid above to compare</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Comparison Legend */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <div className="flex items-start gap-4 p-6 bg-white border border-pink-50 rounded-3xl">
          <Check className="w-5 h-5 text-pink-500 shrink-0" />
          <div>
            <h6 className="text-xs font-bold text-neutral-900 uppercase tracking-tight mb-1">Clinical Grade</h6>
            <p className="text-[10px] text-neutral-500 leading-relaxed italic">Scores ≥ 95% indicate full compliance with MGV-1 surgical-grade standards.</p>
          </div>
        </div>
        <div className="flex items-start gap-4 p-6 bg-white border border-amber-50 rounded-3xl">
          <AlertCircle className="w-5 h-5 text-amber-500 shrink-0" />
          <div>
            <h6 className="text-xs font-bold text-neutral-900 uppercase tracking-tight mb-1">Standard Compliance</h6>
            <p className="text-[10px] text-neutral-500 leading-relaxed italic">Scores 90-94% indicate high-quality materials with minor audit deviations.</p>
          </div>
        </div>
        <div className="flex items-start gap-4 p-6 bg-white border border-neutral-50 rounded-3xl">
          <Info className="w-5 h-5 text-neutral-400 shrink-0" />
          <div>
            <h6 className="text-xs font-bold text-neutral-900 uppercase tracking-tight mb-1">Audit Methodology</h6>
            <p className="text-[10px] text-neutral-500 leading-relaxed italic">All metrics are verified through physical teardowns and material traceability reports.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
