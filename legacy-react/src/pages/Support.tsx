import { LifeBuoy, Mail, ExternalLink, MessageSquare, Clock, ShieldCheck } from 'lucide-react';
import { motion } from 'motion/react';

export default function Support() {
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
            <LifeBuoy className="w-3 h-3 text-stone-400" />
            <span className="text-[10px] font-black text-stone-500 uppercase tracking-[0.4em]">The Support Desk</span>
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-6xl md:text-8xl font-serif tracking-tighter text-stone-900 mb-8 leading-tight"
          >
            Diagnostic <span className="italic text-stone-400 font-light">Support.</span>
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-stone-500 text-xl font-serif italic max-w-2xl mx-auto leading-relaxed antialiased"
          >
            Direct access to technical troubleshooting, cleaning protocols, and clinical hardware specifications. We treat support tickets as diagnostic requests.
          </motion.p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-24 space-y-32">
        {/* Contact Methods */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-12">
          <div className="bg-white border border-stone-200 rounded-[3rem] p-12 shadow-sm space-y-8">
            <div className="w-16 h-16 bg-stone-900 rounded-2xl flex items-center justify-center">
              <Mail className="w-8 h-8 text-rose-300" />
            </div>
            <div className="space-y-4">
              <h3 className="text-3xl font-serif text-stone-900 italic">Email Diagnostics</h3>
              <p className="text-stone-500 font-serif italic leading-relaxed">
                For detailed technical issues, material inquiries, or order-specific diagnostics. Our team responds within 24-48 business hours.
              </p>
              <a 
                href="mailto:support@pixies-pantry.com" 
                className="inline-flex items-center gap-3 text-[11px] font-black text-rose-600 uppercase tracking-widest border-b border-rose-200 pb-1 hover:text-rose-800 transition-colors"
              >
                support@pixies-pantry.com <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>

          <div className="bg-white border border-stone-200 rounded-[3rem] p-12 shadow-sm space-y-8">
            <div className="w-16 h-16 bg-rose-50 rounded-2xl flex items-center justify-center">
              <MessageSquare className="w-8 h-8 text-rose-400" />
            </div>
            <div className="space-y-4">
              <h3 className="text-3xl font-serif text-stone-900 italic">Community Portal</h3>
              <p className="text-stone-500 font-serif italic leading-relaxed">
                Join our Discord server for real-time peer support, community troubleshooting, and direct access to the Auditor Node.
              </p>
              <a 
                href="https://discord.gg/R98q86nm" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="inline-flex items-center gap-3 text-[11px] font-black text-rose-600 uppercase tracking-widest border-b border-rose-200 pb-1 hover:text-rose-800 transition-colors"
              >
                Join the Discord <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        </section>

        {/* Support Tiers */}
        <section className="space-y-12">
          <div className="text-center">
            <span className="text-[10px] font-black text-rose-500 uppercase tracking-[0.4em]">SERVICE PROTOCOLS</span>
            <h2 className="text-4xl md:text-5xl font-serif mt-2 text-stone-900 italic">Response Standards</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Clock,
                title: "Response Time",
                desc: "Standard tickets are addressed within 24-48 hours. Clinical priority accounts receive expedited 12-hour response windows."
              },
              {
                icon: ShieldCheck,
                title: "Material Verification",
                desc: "Every support request involving hardware failure triggers a material audit to ensure no safety compromises occurred."
              },
              {
                icon: LifeBuoy,
                title: "Continuity Support",
                desc: "If your device is non-functional, we prioritize continuity solutions to ensure your titration schedule remains uninterrupted."
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

        {/* FAQ CTA */}
        <section className="bg-stone-900 text-white p-12 md:p-24 rounded-[3.5rem] shadow-2xl relative overflow-hidden text-center">
          <div className="absolute top-0 right-0 w-96 h-96 bg-rose-500/10 rounded-full blur-[100px] -mr-32 -mt-32"></div>
          <div className="max-w-2xl mx-auto relative z-10 space-y-8">
            <h2 className="text-4xl md:text-6xl font-serif tracking-tighter leading-none italic">Need immediate answers?</h2>
            <p className="text-stone-400 font-serif italic text-xl leading-relaxed antialiased">
              Our Knowledge Base contains detailed teardowns, cleaning guides, and technical specifications for all verified hardware.
            </p>
            <a 
              href="/sanctuary" 
              className="inline-flex items-center gap-3 px-12 py-6 bg-white text-stone-900 rounded-full text-[11px] font-black uppercase tracking-[0.2em] hover:bg-rose-50 transition-all"
            >
              Explore the Sanctuary
            </a>
          </div>
        </section>
      </main>
    </div>
  );
}
