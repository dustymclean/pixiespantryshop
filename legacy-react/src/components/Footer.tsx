import { Link } from 'react-router-dom';
import { Shield, Award, BookOpen } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-[#FAFAFA] pt-32 pb-16 px-6 border-t border-stone-200 relative overflow-hidden text-left">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-16 lg:gap-20 mb-24">
        <div className="lg:col-span-5 space-y-10">
          <div className="flex items-center gap-3">
            <img src="https://i.imgur.com/vmJPD4c.png" alt="Logo" className="h-16 w-auto object-contain" />
            <h1 className="text-4xl font-serif tracking-tight flex items-center leading-none">
              <span className="text-stone-900 font-bold">Pixie's</span>
              <span className="text-stone-400 font-light italic ml-2">Pantry</span>
            </h1>
          </div>
          <div className="space-y-4 border-l-2 border-rose-200 pl-6 py-2">
            <p className="text-stone-600 font-serif leading-relaxed italic text-xl max-w-lg">
              "Transparency isn't a feature—it's the foundation. We aren't just selling hardware; we're pushing for healthcare recognition."
            </p>
          </div>
          <div className="pt-4">
             <p className="text-[9px] font-black text-stone-400 uppercase tracking-[0.4em] mb-2">ENTITY VERIFICATION</p>
             <p className="text-xs font-bold text-stone-900 uppercase tracking-widest">BUILT BY DUSTY MCLEAN // MYNODE</p>
          </div>
        </div>
        <div className="lg:col-span-4 grid grid-cols-2 gap-10">
          <div>
            <h4 className="text-[10px] font-black uppercase tracking-[0.4em] mb-8 text-stone-400">REGISTRY</h4>
            <ul className="space-y-5 text-[11px] font-bold text-stone-600 uppercase tracking-[0.2em]">
              <li><a href="https://vapes.pixiespantryshop.com" target="_blank" rel="noopener noreferrer" className="hover:text-rose-500 transition-colors">PROVISIONS</a></li>
              <li><Link to="/" className="hover:text-rose-500 transition-colors">MAIN PORTAL</Link></li>
              <li><Link to="/audit" className="hover:text-rose-500 transition-colors">THE AUDIT</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-[10px] font-black uppercase tracking-[0.4em] mb-8 text-stone-400">SANCTUARY</h4>
            <ul className="space-y-5 text-[11px] font-bold text-stone-600 uppercase tracking-[0.2em]">
              <li><Link to="/sanctuary" className="hover:text-rose-500 transition-colors">KNOWLEDGE BASE</Link></li>
              <li><Link to="/logistics" className="hover:text-rose-500 transition-colors">LOGISTICS</Link></li>
              <li><Link to="/warranty" className="hover:text-rose-500 transition-colors">WARRANTY</Link></li>
              <li><Link to="/support" className="hover:text-rose-500 transition-colors">SUPPORT DESK</Link></li>
            </ul>
          </div>
        </div>
        <div className="lg:col-span-3 lg:text-right space-y-8">
          <h4 className="text-[10px] font-black uppercase tracking-[0.4em] mb-8 text-stone-400">COORDINATES</h4>
          <div className="space-y-2">
            <p className="text-xl font-serif text-stone-800 italic">Mississippi</p>
            <p className="text-[11px] text-stone-500 font-mono tracking-[0.2em]">30.15.54.N 90.45.22.W</p>
          </div>
          <div className="flex lg:justify-end gap-6 pt-8 text-stone-300">
             <Shield className="w-5 h-5" />
             <Award className="w-5 h-5" />
             <BookOpen className="w-5 h-5" />
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto pt-10 border-t border-stone-200/60 text-center">
        <p className="text-[9px] text-stone-500 font-black uppercase tracking-[0.4em]">© 2026 PIXIE'S PANTRY // PROFESSIONAL REGISTRY</p>
      </div>
    </footer>
  );
}