import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Audit from './pages/Audit';
import Sanctuary from './pages/Sanctuary';
import Support from './pages/Support';
import Logistics from './pages/Logistics';
import Warranty from './pages/Warranty';

function ScrollToTop() {
  const { pathname, hash } = useLocation();

  useEffect(() => {
    if (hash) {
      const element = document.getElementById(hash.replace('#', ''));
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    } else {
      window.scrollTo(0, 0);
    }
  }, [pathname, hash]);

  return null;
}

export default function App() {
  return (
    <Router>
      <ScrollToTop />
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/audit" element={<Audit />} />
            <Route path="/sanctuary" element={<Sanctuary />} />
            <Route path="/support" element={<Support />} />
            <Route path="/logistics" element={<Logistics />} />
            <Route path="/warranty" element={<Warranty />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}
