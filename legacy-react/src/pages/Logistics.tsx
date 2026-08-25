import { Truck, Package, ShieldCheck, MapPin, ArrowRight, ClipboardCheck } from 'lucide-react';
import { motion } from 'motion/react';

export default function Logistics() {
  return (
    <div className="bg-[#FAFAFA] text-stone-800 selection:bg-rose-100 selection:text-rose-900 min-h-screen">
      {/* Hero Section */}
      <header className="pt-48 pb-24 px-6 relative overflow-hidden bg-white border-b border-stone-100">
        <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-rose-50/30 rounded-full blur-[120px] -z-10"></div>
        <div className="max-w-4xl mx-auto text-center">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-3 px-6 py-2 bg-stone-50 border border-stone-200 rounded-full mb-8 shadow-sm"
          >
            <Truck className="w-3 h-3 text-stone-400" />
            <span className="text-[10px] font-black text-stone-500 uppercase tracking-[0.4em]">Fulfillment Logistics</span>
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-6xl md:text-8xl font-serif tracking-tighter text-stone-900 mb-8 leading-tight"
          >
            Hardware <span className="italic text-stone-400 font-light">Logistics.</span>
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-stone-500 text-xl font-serif italic max-w-2xl mx-auto leading-relaxed antialiased"
          >
            Total transparency regarding your device's physical chain of custody. We don't drop-ship; we verify and fulfill from our central node.
          </motion.p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-24 space-y-32">
        {/* The Mississippi Node */}
        <section className="bg-white border border-stone-200 rounded-[3rem] p-10 md:p-20 overflow-hidden relative shadow-sm">
          <div className="absolute bottom-0 right-0 w-80 h-80 bg-rose-50/40 rounded-full -mr-20 -mb-20 blur-3xl"></div>
          <div className="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div className="flex items-center gap-4">
                <MapPin className="w-8 h-8 text-rose-400" />
                <h3 className="text-3xl font-bold tracking-tight text-stone-900 leading-tight">The Mississippi Node</h3>
              </div>
              <p className="text-stone-500 leading-relaxed font-serif italic text-lg antialiased">
                "Every unit is physically received at my hub in Mississippi, personally inspected for material integrity, and serialized in the registry before it ships to you."
              </p>
              <div className="space-y-4">
                {[
                  "Intake Teardown & Batch Verification",
                  "Electronic Thermal Calibration Check",
                  "Secure Clinical-Grade Sterilization Packaging"
                ].map((step, i) => (
                  <div key={i} className="flex items-center gap-4 group">
                    <span className="w-10 h-10 rounded-full bg-stone-900 text-white flex items-center justify-center text-xs font-bold group-hover:scale-110 transition-transform">{i + 1}</span>
                    <p className="text-[10px] font-black uppercase tracking-widest text-stone-400">{step}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-stone-50 p-10 rounded-[2.5rem] border border-stone-100 space-y-6">
              <h5 className="text-[10px] font-black uppercase tracking-[0.3em] text-stone-400">Transit Standards</h5>
              <p className="text-sm text-stone-600 leading-relaxed">
                Orders are processed within 24-48 business hours. We utilize specialized shipping buffers to ensure delicate quartz and titanium components remain calibrated during transit. <strong>Adult Signature (21+) is mandatory</strong> for all deliveries—no exceptions.
              </p>
              <a href="https://vapes.pixiespantryshop.com/account" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 text-[10px] font-black text-rose-600 uppercase tracking-widest border-b border-rose-200 pb-1 hover:text-rose-800 transition-colors">
                Track Your Provision <ArrowRight className="w-3 h-3" />
              </a>
            </div>
          </div>
        </section>

        {/* Shipping Protocols */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: Package,
              title: "Clinical Packaging",
              desc: "Every device is packaged in a sterile environment using medical-grade materials to prevent contamination during transit."
            },
            {
              icon: ShieldCheck,
              title: "Insured Transit",
              desc: "All shipments are fully insured. If your hardware is damaged in transit, we replace it immediately to ensure care continuity."
            },
            {
              icon: ClipboardCheck,
              title: "Chain of Custody",
              desc: "We maintain a complete log of every hand that touches your device from the manufacturer to your doorstep."
            }
          ].map((protocol, i) => (
            <div key={i} className="bg-white p-10 rounded-[2.5rem] border border-stone-100 shadow-sm hover:border-rose-200 transition-all">
              <protocol.icon className="w-8 h-8 text-rose-400 mb-6" />
              <h4 className="text-xl font-bold mb-4 tracking-tight text-stone-900 uppercase">{protocol.title}</h4>
              <p className="text-sm text-stone-500 leading-relaxed font-serif italic antialiased">
                {protocol.desc}
              </p>
            </div>
          ))}
        </section>

        {/* FAQ CTA */}
        <section className="bg-stone-900 text-white p-12 md:p-24 rounded-[3.5rem] shadow-2xl relative overflow-hidden text-center">
          <div className="absolute top-0 right-0 w-96 h-96 bg-rose-500/10 rounded-full blur-[100px] -mr-32 -mt-32"></div>
          <div className="max-w-2xl mx-auto relative z-10 space-y-8">
            <h2 className="text-4xl md:text-6xl font-serif tracking-tighter leading-none italic">Order Support</h2>
            <p className="text-stone-400 font-serif italic text-xl leading-relaxed antialiased">
              Have questions about your delivery or need to update your coordinates? Our support desk is ready to assist.
            </p>
            <a 
              href="/support" 
              className="inline-flex items-center gap-3 px-12 py-6 bg-white text-stone-900 rounded-full text-[11px] font-black uppercase tracking-[0.2em] hover:bg-rose-50 transition-all"
            >
              Contact Support
            </a>
          </div>
        </section>
      </main>
    </div>
  );
}
