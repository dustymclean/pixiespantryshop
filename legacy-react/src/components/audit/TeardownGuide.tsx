import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { ArrowLeft, ArrowRight, Info, AlertTriangle, X } from 'lucide-react';
import { Device, devices } from '../../data/devices';

export default function TeardownGuide() {
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [showTerm, setShowTerm] = useState(false);

  const handleNext = () => {
    if (selectedDevice && currentStep < selectedDevice.teardown.length - 1) {
      setCurrentStep(prev => prev + 1);
      setShowTerm(false);
    }
  };

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
      setShowTerm(false);
    }
  };

  const reset = () => {
    setSelectedDevice(null);
    setCurrentStep(0);
    setShowTerm(false);
  };

  if (!selectedDevice) {
    return (
      <div className="space-y-12">
        <div className="text-center max-w-2xl mx-auto">
          <h3 className="text-3xl font-serif text-neutral-900 mb-4 italic">Virtual Teardown Lab</h3>
          <p className="text-neutral-500 font-serif italic">Select a device to begin the step-by-step clinical disassembly and material audit.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {devices.map((device) => (
            <div 
              key={device.id}
              onClick={() => setSelectedDevice(device)}
              className="bg-white border border-pink-100 rounded-[2.5rem] p-8 cursor-pointer hover:border-pink-500 hover:shadow-xl transition-all group text-center"
            >
              <img src={device.image} alt={device.name} className="w-32 h-32 mx-auto mb-6 rounded-2xl object-cover grayscale group-hover:grayscale-0 transition-all" />
              <h4 className="text-xl font-bold text-neutral-900 mb-2">{device.name}</h4>
              <p className="text-xs text-pink-500 font-black uppercase tracking-widest">{device.brand}</p>
            </div>
          ))}
        </div>
      </div>
    );
  }

  const step = selectedDevice.teardown[currentStep];

  return (
    <div className="bg-neutral-900 rounded-[3rem] p-8 md:p-16 text-white relative overflow-hidden shadow-2xl">
      <button 
        onClick={reset}
        className="absolute top-8 right-8 text-neutral-500 hover:text-white transition-colors"
      >
        <X className="w-6 h-6" />
      </button>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <div className="relative aspect-square bg-white/5 rounded-[2rem] flex items-center justify-center overflow-hidden">
          <motion.div
            key={currentStep}
            initial={{ scale: 0.8, opacity: 0, rotate: -10 }}
            animate={{ scale: 1, opacity: 1, rotate: 0 }}
            className="text-center p-12"
          >
            <div className="w-48 h-48 bg-pink-500/20 rounded-full blur-3xl absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
            <img 
              src={selectedDevice.image} 
              alt={step.title} 
              className="w-full h-full object-contain relative z-10 opacity-50"
            />
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-8xl font-serif italic text-white/10 select-none">STEP {currentStep + 1}</span>
            </div>
          </motion.div>
        </div>

        <div className="space-y-8">
          <div>
            <span className="text-[10px] font-black text-pink-400 uppercase tracking-[0.4em] mb-4 block">
              {selectedDevice.name} — COMPONENT {currentStep + 1} OF {selectedDevice.teardown.length}
            </span>
            <h4 className="text-3xl md:text-4xl font-serif italic mb-6">{step.title}</h4>
            <p className="text-neutral-400 font-serif italic text-lg leading-relaxed">
              {step.description}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 bg-white/5 rounded-2xl border border-white/10">
              <h5 className="text-[10px] font-black text-neutral-500 uppercase tracking-widest mb-2">MATERIAL COMPOSITION</h5>
              <p className="text-pink-100 font-bold">{step.material}</p>
            </div>
            <div className="p-6 bg-white/5 rounded-2xl border border-white/10">
              <h5 className="text-[10px] font-black text-neutral-500 uppercase tracking-widest mb-2">MGV-1 RELEVANCE</h5>
              <p className="text-neutral-300 text-sm italic">{step.auditRelevance}</p>
            </div>
          </div>

          <div className="flex flex-wrap gap-4">
            {step.technicalTerm && (
              <button 
                onClick={() => setShowTerm(!showTerm)}
                className="flex items-center gap-2 px-4 py-2 bg-pink-500/10 border border-pink-500/20 rounded-full text-[10px] font-black text-pink-400 uppercase tracking-widest hover:bg-pink-500/20 transition-all"
              >
                <Info className="w-3 h-3" /> {step.technicalTerm.term}
              </button>
            )}
            {step.safetyWarning && (
              <div className="flex items-center gap-2 px-4 py-2 bg-amber-500/10 border border-amber-500/20 rounded-full text-[10px] font-black text-amber-400 uppercase tracking-widest">
                <AlertTriangle className="w-3 h-3" /> SAFETY WARNING
              </div>
            )}
          </div>

          <AnimatePresence>
            {showTerm && step.technicalTerm && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="p-6 bg-pink-500/5 border border-pink-500/10 rounded-2xl"
              >
                <p className="text-sm text-pink-100/80 italic leading-relaxed">
                  <span className="font-bold text-pink-400 not-italic uppercase mr-2">{step.technicalTerm.term}:</span>
                  {step.technicalTerm.definition}
                </p>
              </motion.div>
            )}
            {step.safetyWarning && (
              <div className="p-4 bg-amber-500/5 border border-amber-500/10 rounded-xl text-xs text-amber-200/70 italic">
                {step.safetyWarning}
              </div>
            )}
          </AnimatePresence>

          <div className="pt-8 flex justify-between items-center border-t border-white/10">
            <button 
              onClick={handlePrev}
              disabled={currentStep === 0}
              className={`flex items-center gap-2 text-[10px] font-black uppercase tracking-widest transition-all ${currentStep === 0 ? 'text-neutral-700' : 'text-neutral-400 hover:text-white'}`}
            >
              <ArrowLeft className="w-4 h-4" /> Previous
            </button>
            <div className="flex gap-2">
              {selectedDevice.teardown.map((_, i) => (
                <div key={i} className={`w-1.5 h-1.5 rounded-full transition-all ${i === currentStep ? 'bg-pink-500 scale-125' : 'bg-neutral-700'}`}></div>
              ))}
            </div>
            <button 
              onClick={handleNext}
              disabled={currentStep === selectedDevice.teardown.length - 1}
              className={`flex items-center gap-2 text-[10px] font-black uppercase tracking-widest transition-all ${currentStep === selectedDevice.teardown.length - 1 ? 'text-neutral-700' : 'text-pink-400 hover:text-pink-300'}`}
            >
              Next Component <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
