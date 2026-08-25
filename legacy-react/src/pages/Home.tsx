import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'motion/react';
import { CircleDot, Thermometer, Layers, Droplets } from 'lucide-react';

const AuditCard = ({ title, subtitle, description, layman, icon: Icon }: any) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div 
      onClick={() => setIsExpanded(!isExpanded)}
      className={`audit-card bg-white rounded-[2rem] md:rounded-[3rem] border border-stone-200 p-8 md:p-12 cursor-pointer group flex flex-col h-full transition-all duration-400 ${isExpanded ? 'border-rose-500 shadow-[0_20px_25px_-5px_rgb(225_29_72_/_0.1)]' : ''}`}
    >
      <div className="w-14 h-14 bg-stone-50 border border-stone-200 rounded-full flex items-center justify-center mb-8 group-hover:bg-rose-900 group-hover:border-rose-900 transition-all duration-500">
        <Icon className="w-7 h-7 text-stone-900 group-hover:text-white transition-colors" />
      </div>
      <div className="mb-6">
        <span className="text-[9px] font-black text-stone-400 tracking-[0.4em] uppercase mb-4 block group-hover:text-stone-600">{subtitle}</span>
        <h4 className="text-2xl md:text-3xl font-serif text-stone-900 tracking-tight leading-tight mb-4">{title}</h4>
      </div>
      <p className="text-stone-500 leading-relaxed text-sm md:text-base antialiased flex-grow">
        {description}
      </p>
      
      <div className="mt-auto pt-6 text-[10px] text-rose-600 font-medium flex items-center gap-2 opacity-70">
        <span>↓</span> CLICK FOR LAYMAN'S EXPLANATION
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="mt-8 pt-6 border-t border-stone-100 text-sm leading-relaxed">
              <span className="inline-block bg-rose-100 text-rose-700 text-[10px] font-black tracking-widest px-3 py-1 rounded-full mb-3">IN SIMPLE TERMS</span>
              <p className="text-stone-600">
                {layman}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="pt-48 md:pt-64 pb-24 md:pb-32 px-6 relative overflow-hidden hero-glow">
        <div className="absolute top-0 right-0 w-[700px] md:w-[1100px] h-[700px] md:h-[1100px] bg-rose-50/40 rounded-full blur-[140px] -z-10"></div>
        <div className="absolute bottom-0 left-0 w-[600px] md:w-[900px] h-[600px] md:h-[900px] bg-rose-50/30 rounded-full blur-[110px] -z-10"></div>

        <div className="max-w-6xl mx-auto text-center">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-3 px-6 py-2 bg-white border border-stone-200 rounded-full shadow-[0_2px_15px_-5px_rgba(0,0,0,0.05)] mb-10"
          >
            <span className="text-[10px] font-black text-stone-600 uppercase tracking-[0.4em]">THE MEDICAL HARDWARE PORTAL</span>
          </motion.div>

          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-6xl md:text-8xl lg:text-[9rem] font-serif tracking-tighter text-stone-900 mb-10 leading-[0.9] md:leading-[0.85]"
          >
            Precision <span className="italic text-stone-500 font-medium pr-2">Hardware.</span><br className="hidden md:block" />
            <span className="gold-text">Zero Noise.</span>
          </motion.h2>

          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="max-w-3xl mx-auto text-stone-500 text-lg md:text-xl font-light leading-relaxed mb-14 font-serif italic antialiased px-4"
          >
            The industry is flooded with cheap plastics and paid reviews. I got tired of guessing, so I started tearing them apart myself. We are pivoting from being just a boutique to building the infrastructure for FSA/HSA eligibility and, ultimately, insurance coverage. We are getting this hardware recognized for what it actually is: medical equipment. Welcome to Pixie's Pantry—where the research is already done.
          </motion.p>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-5 justify-center items-center px-6"
          >
            <a href="https://vapes.pixiespantryshop.com" target="_blank" rel="noopener noreferrer"
               className="w-full sm:w-auto px-12 py-5 bg-stone-900 hover:bg-stone-800 text-white font-bold rounded-full shadow-2xl shadow-stone-900/10 hover:shadow-stone-900/20 hover:-translate-y-0.5 transition-all duration-500 uppercase tracking-[0.3em] text-[11px] inline-flex items-center justify-center gap-3">
              ENTER THE SHOP →
            </a>
            <Link to="/audit"
               className="w-full sm:w-auto px-12 py-5 bg-white border border-stone-200 text-stone-500 hover:text-stone-900 hover:border-stone-300 font-bold rounded-full shadow-sm hover:shadow transition-all duration-500 uppercase tracking-[0.3em] text-[11px] inline-flex items-center justify-center">
              OUR CLINICAL AUDIT
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Trust Registry Bar */}
      <section className="py-16 md:py-24 border-y border-stone-100 bg-white/40 backdrop-blur-md relative z-10">
        <div className="max-w-7xl mx-auto px-6 overflow-x-auto no-scrollbar scroll-smooth">
          <div className="flex justify-between items-center min-w-[1000px] gap-8 pb-4 md:pb-0">
            {[
              'VERIFIED SERIAL REGISTRY',
              'MEDICAL GRADE STANDARDS',
              'TEARDOWN VERIFIED',
              'ACTIVE FSA/HSA INITIATIVE',
              'CANDID HARDWARE AUDITS'
            ].map((text) => (
              <div key={text} className="flex items-center gap-3 px-5 py-2.5 rounded-full border border-stone-200 bg-white shadow-[0_2px_10px_-4px_rgba(0,0,0,0.05)] hover:border-rose-200 transition-all duration-500 group">
                <span className="text-stone-500 text-xl leading-none">•</span>
                <span className="text-[10px] font-black text-stone-500 uppercase tracking-[0.25em] group-hover:text-stone-800">{text}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Main Audit Section */}
      <main id="the-audit" className="max-w-7xl mx-auto px-6 py-24 md:py-40 scroll-mt-20">
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-end mb-20 md:mb-24 gap-10">
          <div className="max-w-2xl">
            <span className="text-[10px] font-black text-stone-400 uppercase tracking-[0.5em] mb-6 block">OUR METHODOLOGY</span>
            <h3 className="text-4xl md:text-5xl lg:text-6xl font-serif text-stone-900 tracking-tight leading-tight">
              We don't just review it.<br className="hidden md:block"/>We audit it for health.
            </h3>
          </div>
          <div className="max-w-md text-stone-500 font-serif italic leading-relaxed text-lg lg:text-xl border-l-2 border-stone-200 pl-6">
            "Before a device ever gets a spot in our shop, it has to survive our clinical workflow. We look past the marketing gimmicks and focus entirely on engineering, material sourcing, and respiratory safety."
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">
          <AuditCard 
            subtitle="MATERIAL SAFETY (TTI)"
            title="Vapor Path Purity"
            description="We look for Total Thermal Isolation. If inhaled air passes over a circuit board, a battery, or cheap manufacturing glue, the device is immediately disqualified. We tear down every chassis to verify that the airpath is ≥ 98% composed of Borosilicate, Ceramic, 316L Stainless, Grade 2+ Titanium, or PEEK. This guarantees zero polymer off-gassing at temperatures up to 450°F."
            layman="The air you breathe in should never touch plastic, glue, circuit boards, or any cheap materials. We only approve devices where the entire vapor path is made from safe, high-grade materials like medical glass, ceramic, or surgical metal. This stops any toxic chemicals from being released when the device gets hot — exactly what you want for clean, safe daily use."
            icon={CircleDot}
          />
          <AuditCard 
            subtitle="DOSAGE CONSISTENCY (PTC)"
            title="Thermal Stability"
            description="Marketing departments love to claim 'heats up in 10 seconds.' What they don't tell you is that the heater crashes the moment you take a draw. We run rigorous thermocouple testing to ensure real-time temperature fluctuations remain ≤ ± 2°F during active draw. Medical efficacy requires consistent thermal mass to ensure decarboxylation without ever breaching the 455°F combustion threshold."
            layman="Cheap devices heat up quickly but then cool down the second you inhale. This gives you an uneven dose and can create harmful chemicals. We test every device to make sure the temperature stays perfectly steady (±2°F) the entire time you’re using it — so you get the exact same clean, effective dose on every single draw without burning anything."
            icon={Thermometer}
          />
          <AuditCard 
            subtitle="SURGICAL GRADE (SGC)"
            title="Bio-Compatibility"
            description="Lab conditions are great, but how does it handle real-world wear? If insurance is ever going to cover a unit, it has to be built with ISO 10993 or USP Class VI compliant materials. We ensure that surfaces in contact with your mouth or the raw plant matter do not cause cytotoxic reactions or systemic toxicity over time."
            layman="The parts that touch your mouth or the plant material must be made from the same hospital-grade materials used for long-term medical implants. We only accept devices that meet the strictest international safety standards so they won’t slowly release toxins into your body over months or years of regular use."
            icon={Layers}
          />
          <AuditCard 
            subtitle="CLINICAL PROTOCOL"
            title="Sanitization & Hygiene"
            description="A multi-use medical tool is useless if it can't be thoroughly cleaned. We mandate Autoclave-Compatible Geometry. To pass our audit, a device must be ≥ 90% submersible in 91% Isopropyl Alcohol or be able to withstand 250°F steam sterilization without warping, staining, or breaking down."
            layman="If you’re going to use something every day like a medical tool, it has to be easy to clean completely. We require that the device can be fully soaked in strong rubbing alcohol or placed in a high-temperature steam sterilizer (the kind dentists use) without warping or breaking. If it can’t be properly sanitized, it’s not safe for repeated use."
            icon={Droplets}
          />
        </div>

        {/* Call to Action */}
        <div className="mt-32 md:mt-40 bg-stone-950 rounded-[2rem] md:rounded-[3rem] p-10 md:p-20 lg:p-24 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-[300px] md:w-[500px] h-[300px] md:h-[500px] bg-rose-900/10 rounded-full blur-[80px] md:blur-[100px]"></div>
          <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-rose-900/5 rounded-full blur-[80px]"></div>

          <div className="relative z-10 flex flex-col lg:flex-row items-center justify-between gap-12 text-center lg:text-left">
            <div className="max-w-2xl">
              <h4 className="text-3xl md:text-4xl lg:text-5xl font-serif text-white tracking-tight mb-6">
                Ready to see what survived?
              </h4>
              <p className="text-stone-400 font-serif italic text-lg md:text-xl leading-relaxed">
                As we work towards full FSA/HSA integration, you can skip the trial and error today. Every unit in our hardware shop has passed the clinical audit, complete with our candid teardown notes.
              </p>
            </div>
            <a href="https://vapes.pixiespantryshop.com" target="_blank" rel="noopener noreferrer"
               className="gold-gradient px-10 py-6 text-white font-bold rounded-full uppercase tracking-[0.3em] text-[11px] shadow-xl shadow-yellow-600/10 hover:shadow-2xl hover:shadow-yellow-600/30 hover:-translate-y-1 transition-all duration-500 flex items-center justify-center gap-3 w-full lg:w-auto">
              BROWSE PROVISIONS →
            </a>
          </div>
        </div>
      </main>

      {/* Signature */}
      <section className="py-32 md:py-40 bg-stone-50/50 overflow-hidden relative border-t border-stone-100">
        <div className="max-w-4xl mx-auto px-6 text-center relative z-10">
          <div className="w-16 md:w-24 h-[2px] bg-gradient-to-r from-transparent via-rose-300 to-transparent mx-auto mb-12 md:mb-16"></div>
          <p className="text-3xl md:text-4xl lg:text-5xl font-serif italic text-stone-700 leading-tight md:leading-tight mb-16 antialiased">
            "Transparency isn't a feature—it's the foundation. We aren't just selling hardware; we're pushing for healthcare recognition. If it's on our shelf, I've personally verified its integrity."
          </p>
          <div className="flex flex-col items-center gap-3">
            <span className="text-[11px] md:text-[12px] font-black text-stone-900 uppercase tracking-[0.4em] md:tracking-[0.6em]">
              — DUSTY LYN MCLEAN
            </span>
            <span className="text-[9px] md:text-[10px] font-bold text-stone-400 uppercase tracking-[0.3em] md:tracking-widest">
              FOUNDER & CHIEF AUDITOR
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}
