import { Shield, Award, CheckCircle, AlertTriangle, LifeBuoy, ExternalLink } from 'lucide-react';
import { motion } from 'motion/react';

export default function Warranty() {
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
            <Shield className="w-3 h-3 text-stone-400" />
            <span className="text-[10px] font-black text-stone-500 uppercase tracking-[0.4em]">The Protection Policy</span>
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-6xl md:text-8xl font-serif tracking-tighter text-stone-900 mb-8 leading-tight"
          >
            Warranty <span className="italic text-stone-400 font-light">& Protection.</span>
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-stone-500 text-xl font-serif italic max-w-2xl mx-auto leading-relaxed antialiased"
          >
            Standard hardware warranties are built to protect corporations. Ours is built to protect your titration schedule.
          </motion.p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-24 space-y-32">
        {/* Core Policy */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
          <div className="space-y-8">
            <h2 className="text-4xl md:text-5xl font-serif text-stone-900 italic leading-tight">Accountability in Care.</h2>
            <p className="text-stone-500 text-lg font-serif italic leading-relaxed antialiased">
              "If a device fails, your care stops—I make sure that gap is closed immediately. As an authorized distribution node, we honor the full factory warranty on all extraction devices."
            </p>
            <div className="space-y-6">
              {[
                "Full Manufacturer Parity",
                "90-Day Continuity Guarantee",
                "Direct Manufacturer Liaison",
                "Verified Clinical Account Priority"
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-4">
                  <CheckCircle className="w-5 h-5 text-rose-400" />
                  <span className="text-[11px] font-black uppercase tracking-widest text-stone-600">{item}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-stone-900 text-white p-12 rounded-[3rem] shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-rose-500/10 rounded-full blur-3xl"></div>
            <div className="relative z-10 space-y-8">
              <Award className="w-12 h-12 text-rose-300" />
              <h3 className="text-3xl font-serif italic">The Continuity Guarantee</h3>
              <p className="text-stone-400 font-serif italic leading-relaxed">
                If your device suffers a terminal electronic failure within the first 90 days, verified clinical accounts are eligible for an immediate replacement unit to minimize therapy interruption.
              </p>
              <div className="pt-6 border-t border-stone-800">
                <p className="text-[10px] text-stone-500 uppercase tracking-widest leading-relaxed">
                  *Subject to verification of clinical necessity and device diagnostic report.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Warranty Tiers */}
        <section className="space-y-12">
          <div className="text-center">
            <span className="text-[10px] font-black text-rose-500 uppercase tracking-[0.4em]">COVERAGE DOMAINS</span>
            <h2 className="text-4xl md:text-5xl font-serif mt-2 text-stone-900 italic">What's Protected</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Shield,
                title: "Electronic Systems",
                desc: "Full coverage for internal heaters, PID controllers, and battery management systems as per manufacturer specifications."
              },
              {
                icon: AlertTriangle,
                title: "Material Integrity",
                desc: "Protection against manufacturing defects in borosilicate, titanium, and medical-grade polymers."
              },
              {
                icon: LifeBuoy,
                title: "Technical Support",
                desc: "Lifetime access to our support desk for troubleshooting and maintenance guidance."
              }
            ].map((tier, i) => (
              <div key={i} className="bg-white p-10 rounded-[2.5rem] border border-stone-100 shadow-sm hover:border-rose-200 transition-all">
                <tier.icon className="w-8 h-8 text-rose-400 mb-6" />
                <h4 className="text-xl font-bold mb-4 tracking-tight text-stone-900 uppercase">{tier.title}</h4>
                <p className="text-sm text-stone-500 leading-relaxed font-serif italic antialiased">
                  {tier.desc}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Claim CTA */}
        <section className="bg-white border border-stone-200 rounded-[3rem] p-12 md:p-24 shadow-sm text-center space-y-8">
          <div className="max-w-2xl mx-auto space-y-6">
            <h2 className="text-4xl md:text-6xl font-serif tracking-tight text-stone-900 italic">Need to initiate a claim?</h2>
            <p className="text-stone-500 font-serif italic text-lg leading-relaxed px-6 antialiased">
              Our diagnostic team is ready to process your request. Please have your device serial number and proof of purchase ready.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row justify-center gap-6 px-6">
            <a href="mailto:support@pixies-pantry.com" className="px-12 py-6 bg-stone-900 text-white rounded-full text-[11px] font-black uppercase tracking-[0.2em] hover:bg-black transition-all shadow-xl shadow-stone-200 flex items-center justify-center gap-3">
               Initiate Claim <ExternalLink className="w-4 h-4" />
            </a>
            <a href="/support" className="px-12 py-6 bg-stone-50 border border-stone-200 text-stone-600 rounded-full text-[11px] font-black uppercase tracking-[0.2em] hover:border-stone-400 transition-all flex items-center justify-center gap-3">
               Support Desk
            </a>
          </div>
        </section>
      </main>
    </div>
  );
}
