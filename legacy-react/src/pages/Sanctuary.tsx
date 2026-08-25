import { BookOpen, ThermometerSnowflake, Layers, ClipboardCheck, LifeBuoy, Mail, ExternalLink, ArrowRight, Shield, Award } from 'lucide-react';
import { motion } from 'motion/react';

export default function Sanctuary() {
  return (
    <div className="bg-[#FAFAFA] text-stone-800 selection:bg-rose-100 selection:text-rose-900">
      {/* Hero Section */}
      <header className="pt-48 pb-24 px-6 relative overflow-hidden bg-white border-b border-stone-100">
        <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-rose-50/30 rounded-full blur-[120px] -z-10"></div>
        <div className="max-w-4xl mx-auto text-center">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-3 px-6 py-2 bg-stone-50 border border-stone-200 rounded-full mb-8 shadow-sm"
          >
            <BookOpen className="w-3 h-3 text-stone-400" />
            <span className="text-[10px] font-black text-stone-500 uppercase tracking-[0.4em]">The Sanctuary</span>
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-6xl md:text-8xl font-serif tracking-tighter text-stone-900 mb-8 leading-tight"
          >
            Intelligence <span className="italic text-stone-400 font-light">Hub.</span>
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-stone-500 text-xl font-serif italic max-w-2xl mx-auto leading-relaxed antialiased"
          >
            The centralized repository for hardware documentation, clinical guides, and the technical bridge between extraction technology and human health.
          </motion.p>
        </div>
      </header>

      {/* Anchor Navigation */}
      <div className="sticky top-24 w-full bg-white/60 backdrop-blur-md border-b border-stone-100 z-40 py-4">
        <div className="max-w-7xl mx-auto px-6 flex justify-center gap-8 md:gap-16">
          <a href="#knowledge" className="text-[9px] font-black uppercase tracking-widest text-stone-400 hover:text-rose-600 transition-colors">Knowledge</a>
          <a href="/logistics" className="text-[9px] font-black uppercase tracking-widest text-stone-400 hover:text-rose-600 transition-colors">Logistics</a>
          <a href="/warranty" className="text-[9px] font-black uppercase tracking-widest text-stone-400 hover:text-rose-600 transition-colors">Warranty</a>
          <a href="/support" className="text-[9px] font-black uppercase tracking-widest text-stone-400 hover:text-rose-600 transition-colors">Support</a>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-24 space-y-32">
        
        {/* Section: Knowledge */}
        <section id="knowledge" className="space-y-12 scroll-mt-40">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 border-b border-stone-100 pb-8">
            <div>
              <span className="text-[10px] font-black text-rose-500 uppercase tracking-[0.4em]">01 / FOUNDATIONS</span>
              <h2 className="text-4xl md:text-5xl font-serif mt-2 text-stone-900">Technical Registry</h2>
            </div>
            <p className="text-stone-400 font-serif italic max-w-xs leading-relaxed">Vetted guidance on device operation and surgical-grade material safety.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="glass-card p-10 rounded-[2.5rem] hover:border-rose-200 transition-all group shadow-sm">
              <div className="w-12 h-12 bg-rose-50 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-rose-100 transition-colors">
                <ThermometerSnowflake className="w-6 h-6 text-rose-400" />
              </div>
              <h4 className="text-xl font-bold mb-4 tracking-tight text-stone-900 uppercase">Thermal Indexing</h4>
              <p className="text-sm text-stone-500 leading-relaxed font-serif italic antialiased">
                Comprehensive guide to precision temperature selection. We provide data-driven titration curves to ensure medicine is released without ever hitting the 451°F combustion threshold.
              </p>
            </div>
            <div className="glass-card p-10 rounded-[2.5rem] hover:border-rose-200 transition-all group shadow-sm">
              <div className="w-12 h-12 bg-stone-100 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-stone-200 transition-colors">
                <Layers className="w-6 h-6 text-stone-400" />
              </div>
              <h4 className="text-xl font-bold mb-4 tracking-tight text-stone-900 uppercase">Material Analysis</h4>
              <p className="text-sm text-stone-500 leading-relaxed font-serif italic antialiased">
                A rigorous audit of Borosilicate 3.3, Grade 2 Titanium, and 316L Stainless Steel. We verify certificates of conformance to ensure zero heavy metal leaching in high-heat zones.
              </p>
            </div>
            <div className="glass-card p-10 rounded-[2.5rem] hover:border-rose-200 transition-all group shadow-sm">
              <div className="w-12 h-12 bg-stone-100 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-stone-200 transition-colors">
                <ClipboardCheck className="w-6 h-6 text-stone-400" />
              </div>
              <h4 className="text-xl font-bold mb-4 tracking-tight text-stone-900 uppercase">Sterilization</h4>
              <p className="text-sm text-stone-500 leading-relaxed font-serif italic antialiased">
                Maintenance protocols for respiratory safety. If a hardware component cannot withstand a 91% ISO soak or steam sterilization, it is reclassified as a liability.
              </p>
            </div>
          </div>
        </section>

        {/* Section: Advanced Guides */}
        <section className="space-y-12">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 border-b border-stone-100 pb-8">
            <div>
              <span className="text-[10px] font-black text-rose-500 uppercase tracking-[0.4em]">02 / ADVANCED</span>
              <h2 className="text-4xl md:text-5xl font-serif mt-2 text-stone-900">Clinical Protocols</h2>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-white border border-stone-200 rounded-[3rem] p-12 shadow-sm space-y-6">
              <h3 className="text-2xl font-serif text-stone-900 italic">Titration Methodology</h3>
              <p className="text-stone-500 font-serif italic leading-relaxed">
                Learn how to effectively titrate your medicine using precision thermal extraction. We cover the physiological effects of different temperature ranges and how to optimize for specific therapeutic outcomes.
              </p>
              <a href="/audit" className="inline-flex items-center gap-2 text-[10px] font-black text-rose-600 uppercase tracking-widest border-b border-rose-200 pb-1 hover:text-rose-800 transition-colors">
                View Audit Specs <ArrowRight className="w-3 h-3" />
              </a>
            </div>
            <div className="bg-white border border-stone-200 rounded-[3rem] p-12 shadow-sm space-y-6">
              <h3 className="text-2xl font-serif text-stone-900 italic">Material Traceability</h3>
              <p className="text-stone-500 font-serif italic leading-relaxed">
                Understanding the Certificate of Conformance (CoC). We explain how to read manufacturer data sheets to verify the purity of the titanium and stainless steel used in your hardware.
              </p>
              <a href="/audit" className="inline-flex items-center gap-2 text-[10px] font-black text-rose-600 uppercase tracking-widest border-b border-rose-200 pb-1 hover:text-rose-800 transition-colors">
                Explore the Audit <ArrowRight className="w-3 h-3" />
              </a>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="text-center space-y-12 py-20 bg-rose-50/30 rounded-[3rem] border border-rose-100 shadow-sm">
          <div className="max-w-2xl mx-auto space-y-6">
            <div className="w-16 h-16 bg-white rounded-full shadow-sm flex items-center justify-center mx-auto mb-6">
              <Shield className="w-8 h-8 text-rose-400" />
            </div>
            <h2 className="text-4xl md:text-6xl font-serif tracking-tight text-stone-900 italic">Further Intelligence</h2>
            <p className="text-stone-500 font-serif italic text-lg leading-relaxed px-6 antialiased">
              Our support team is available for direct technical diagnostics and clinical hardware inquiries.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row justify-center gap-6 px-6">
            <a href="/support" className="px-12 py-6 bg-stone-900 text-white rounded-full text-[11px] font-black uppercase tracking-[0.2em] hover:bg-black transition-all shadow-xl shadow-stone-200 flex items-center justify-center gap-3">
               Support Desk
            </a>
            <a href="/logistics" className="px-12 py-6 bg-white border border-stone-200 text-stone-600 rounded-full text-[11px] font-black uppercase tracking-[0.2em] hover:border-stone-400 transition-all flex items-center justify-center gap-3">
               Logistics Info
            </a>
          </div>
        </section>

      </main>
    </div>
  );
}
