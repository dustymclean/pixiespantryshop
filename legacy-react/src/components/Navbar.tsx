import { Link } from 'react-router-dom';
import { ShoppingBag } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-[100] bg-white/80 backdrop-blur-xl border-b border-stone-100 font-sans">
      <div className="max-w-7xl mx-auto px-6 h-24 flex justify-between items-center">
        <Link to="/" className="flex items-center gap-3 group">
          <img 
            src="https://i.imgur.com/vmJPD4c.png" 
            alt="Logo" 
            className="h-12 w-auto object-contain group-hover:opacity-80 transition-opacity" 
            onError={(e) => (e.currentTarget.src = 'https://i.imgur.com/Xqc4bAF.png')}
          />
          <h1 className="text-2xl font-serif tracking-tight flex items-center leading-none">
            <span className="text-stone-900 font-bold">Pixie's</span>
            <span className="text-stone-400 font-light italic ml-2 group-hover:text-stone-600 transition-colors">Pantry</span>
          </h1>
        </Link>

        <div className="hidden lg:flex items-center gap-8">
          <a href="https://vapes.pixiespantryshop.com" target="_blank" rel="noopener noreferrer" className="text-[10px] font-black text-stone-400 hover:text-stone-900 uppercase tracking-[0.3em] transition-all">Provisions</a>
          <Link to="/audit" className="text-[10px] font-black text-stone-400 hover:text-stone-900 uppercase tracking-[0.3em] transition-all">The Audit</Link>
          <Link to="/sanctuary" className="text-[10px] font-black text-stone-400 hover:text-stone-900 uppercase tracking-[0.3em] transition-all">Knowledge Base</Link>
          <Link to="/logistics" className="text-[10px] font-black text-stone-400 hover:text-stone-900 uppercase tracking-[0.3em] transition-all">Logistics</Link>
          <Link to="/warranty" className="text-[10px] font-black text-stone-400 hover:text-stone-900 uppercase tracking-[0.3em] transition-all">Warranty</Link>
          <Link to="/support" className="text-[10px] font-black text-stone-400 hover:text-stone-900 uppercase tracking-[0.3em] transition-all">Support</Link>
        </div>

        <div className="flex items-center gap-4">
          <a href="https://vapes.pixiespantryshop.com/" target="_blank" rel="noopener noreferrer" className="relative group flex items-center gap-3 bg-stone-900 hover:bg-black px-6 py-2.5 rounded-full transition-all duration-300 shadow-lg shadow-stone-200">
            <ShoppingBag className="w-4 h-4 text-rose-300" />
            <span className="text-[10px] font-black text-white uppercase tracking-widest">Shop Provisions</span>
          </a>
        </div>
      </div>
    </nav>
  );
}
