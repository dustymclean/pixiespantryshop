import { ShieldCheck, Microscope, Thermometer, Cpu, Droplets, FlaskConical, BarChart3 } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { useState } from 'react';
import TeardownGuide from '../components/audit/TeardownGuide';
import DeviceComparison from '../components/audit/DeviceComparison';

export default function Audit() {
  const [activeLab, setActiveLab] = useState<'teardown' | 'comparison'>('teardown');

  return (
    <div className="min-h-screen bg-[#FDFCFD]">
      {/* Hero Section */}
      <header className="pt-32 md:pt-48 pb-20 px-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-[600px] md:w-[1000px] h-[600px] md:h-[1000px] bg-pink-100/20 rounded-full blur-[120px] -z-10 pointer-events-none"></div>
        <div className="max-w-4xl mx-auto text-center">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-3 px-6 py-2 bg-white border border-pink-100 rounded-full shadow-sm mb-10 cursor-default"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-pink-400" />
            <span className="text-[10px] font-black text-pink-500 uppercase tracking-[0.5em]">CLINICAL VERIFICATION</span>
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-6xl md:text-8xl font-serif tracking-tighter text-neutral-900 mb-12"
          >
            The Audit
          </motion.h1>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-left bg-white/40 backdrop-blur-md border border-white p-8 md:p-12 rounded-[2.5rem] shadow-sm"
          >
            <div className="max-w-3xl mx-auto space-y-8 text-neutral-600 text-lg md:text-xl font-serif italic leading-relaxed antialiased">
              <p>
                I am Miss Pixie. As a technologist and chronic illness advocate, I don’t just sell things; I audit them. My commitment is to provide access to superior consumption technology that aligns with advanced physiological care. Pixie’s Pantry is a verified distribution node, ensuring that every product is meticulously vetted for uncompromised quality and compliance.
              </p>
              <p>
                We specialize in medical-grade thermal extraction devices, advanced aerosol delivery systems, and precision accessories. Our focus is on clinical integrity and material science, prioritizing lead-free borosilicate glass, Grade 2 Titanium, USP Class VI Silicone, and other medically compliant materials. We are pioneers in titrated thermal extraction, designing devices for inert material delivery that support advanced physiological care while explicitly contraindicating combustion.
              </p>
              <p className="not-italic text-neutral-900 font-medium pt-4">
                Join our thriving community of discerning consumers and medical professionals. Learn more about our vetting process, product specifications, and the future of medical-grade consumption technology. <span className="gold-text font-black uppercase tracking-[0.3em] block mt-4 text-sm">THE STANDARD FOR MEDICAL-GRADE CONSUMOLOGY.</span>
              </p>
            </div>
          </motion.div>
        </div>
      </header>

      {/* Interactive Lab Section */}
      <section className="py-24 md:py-40 bg-pink-50/30 border-y border-pink-100">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16 md:mb-24">
            <span className="text-[10px] font-black text-pink-400 uppercase tracking-[0.5em] mb-4 block">THE INTERACTIVE LAB</span>
            <h3 className="text-4xl md:text-6xl font-serif text-neutral-900 tracking-tight mb-12 italic">Virtual Hardware Analysis</h3>
            
            <div className="flex justify-center gap-4">
              <button 
                onClick={() => setActiveLab('teardown')}
                className={`px-8 py-4 rounded-full text-[11px] font-black uppercase tracking-widest transition-all flex items-center gap-3 ${activeLab === 'teardown' ? 'bg-stone-900 text-white shadow-xl' : 'bg-white text-stone-400 border border-stone-100 hover:border-pink-200'}`}
              >
                <FlaskConical className="w-4 h-4" /> Teardown Guide
              </button>
              <button 
                onClick={() => setActiveLab('comparison')}
                className={`px-8 py-4 rounded-full text-[11px] font-black uppercase tracking-widest transition-all flex items-center gap-3 ${activeLab === 'comparison' ? 'bg-stone-900 text-white shadow-xl' : 'bg-white text-stone-400 border border-stone-100 hover:border-pink-200'}`}
              >
                <BarChart3 className="w-4 h-4" /> Device Comparison
              </button>
            </div>
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key={activeLab}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
            >
              {activeLab === 'teardown' ? <TeardownGuide /> : <DeviceComparison />}
            </motion.div>
          </AnimatePresence>
        </div>
      </section>

      {/* Methodology Section */}
      <section className="py-24 md:py-40 bg-white border-y border-pink-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col lg:flex-row justify-between items-start lg:items-end mb-20 md:mb-24 gap-10">
            <div className="max-w-2xl">
              <span className="text-[10px] font-black text-pink-400 uppercase tracking-[0.5em] mb-6 block">OUR METHODOLOGY</span>
              <h3 className="text-4xl md:text-5xl lg:text-6xl font-serif text-neutral-900 tracking-tight leading-tight">
                We don't just review it.<br className="hidden md:block"/>We audit it for health.
              </h3>
            </div>
            <div className="max-w-md text-neutral-500 font-serif italic leading-relaxed text-lg lg:text-xl border-l-2 border-pink-100 pl-6">
              "Before a device ever gets a spot in our shop, it has to survive our clinical workflow. We look past the marketing gimmicks and focus entirely on engineering, material sourcing, and respiratory safety."
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">
            {[
              {
                icon: Microscope,
                subtitle: "MATERIAL SAFETY (TTI)",
                title: "Vapor Path Purity",
                text: "We look for Total Thermal Isolation. If inhaled air passes over a circuit board, a battery, or cheap manufacturing glue, the device is immediately disqualified. We tear down every chassis to verify that the airpath is ≥ 98% composed of Borosilicate, Ceramic, 316L Stainless, Grade 2+ Titanium, or PEEK."
              },
              {
                icon: Thermometer,
                subtitle: "DOSAGE CONSISTENCY (PTC)",
                title: "Thermal Stability",
                text: "Marketing departments love to claim 'heats up in 10 seconds.' What they don't tell you is that the heater crashes the moment you take a draw. We run rigorous thermocouple testing to ensure real-time temperature fluctuations remain ≤ ± 2°F during active draw."
              },
              {
                icon: Cpu,
                subtitle: "SURGICAL GRADE (SGC)",
                title: "Bio-Compatibility",
                text: "Lab conditions are great, but how does it handle real-world wear? If insurance is ever going to cover a unit, it has to be built with ISO 10993 or USP Class VI compliant materials. We ensure that surfaces in contact with your mouth or the raw plant matter do not cause cytotoxic reactions."
              },
              {
                icon: Droplets,
                subtitle: "CLINICAL PROTOCOL",
                title: "Sanitization & Hygiene",
                text: "A multi-use medical tool is useless if it can't be thoroughly cleaned. We mandate Autoclave-Compatible Geometry. To pass our audit, a device must be ≥ 90% submersible in 91% Isopropyl Alcohol or be able to withstand 250°F steam sterilization."
              }
            ].map((pillar, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="bg-white rounded-[2rem] border border-neutral-100 p-8 md:p-12 hover:shadow-xl hover:border-pink-100 transition-all duration-500 group"
              >
                <div className="w-14 h-14 bg-pink-50 rounded-full flex items-center justify-center text-pink-400 mb-8 group-hover:scale-110 transition-transform shadow-sm">
                  <pillar.icon className="w-6 h-6" />
                </div>
                <span className="text-[9px] font-black text-neutral-400 tracking-[0.4em] uppercase mb-4 block">{pillar.subtitle}</span>
                <h4 className="text-2xl md:text-3xl font-serif text-neutral-900 mb-6">{pillar.title}</h4>
                <p className="text-neutral-500 leading-relaxed text-sm md:text-base">
                  {pillar.text}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* MGV-1 Roster Section */}
      <section className="py-24 md:py-40 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-20">
            <span className="text-[10px] font-black text-pink-400 uppercase tracking-[0.5em] mb-4 block">THE VERIFIED ROSTER</span>
            <h3 className="text-4xl md:text-6xl font-serif text-neutral-900 tracking-tight mb-6">The MGV-1 Contenders</h3>
            <p className="text-neutral-500 font-serif italic text-lg max-w-2xl mx-auto">
              Out of 1,649 items in our catalog, only 39 distinct lines cleared the data thresholds for clinical verification.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                tier: "Tier 1",
                title: "The Gold Standard",
                subtitle: "Pre-Certified Compliance",
                description: "These devices passed immediately because the manufacturers already comply with clinical and pharmaceutical manufacturing standards (ISO 13485, cGMP820).",
                devices: ["Storz & Bickel: Volcano Hybrid, MIGHTY+, Venty", "DaVinci: IQ2, IQC"],
                icon: ShieldCheck
              },
              {
                tier: "Tier 2",
                title: "Materially Pure",
                subtitle: "Bio-Compatible Airpaths",
                description: "Verified for negative cytotoxicity. These units utilize totally inert materials like Borosilicate 3.3 and Grade 2 Titanium in the high-heat zones.",
                devices: ["Arizer: Solo 3, Air SE, ArGo", "Dynavap: The 'M' Plus, Omni"],
                icon: Microscope
              },
              {
                tier: "Tier 3",
                title: "Extraction Consoles",
                subtitle: "Precision e-Rigs",
                description: "Advanced thermoregulation with thermal runaway protection. These consoles bridge the gap between desktop power and portable safety.",
                devices: ["Puffco: Peak Pro (V2), Proxy", "Focus V: Carta 2"],
                icon: Thermometer
              },
              {
                tier: "Tier 4",
                title: "Botanical Homogenizers",
                subtitle: "Zero-Shedding Mechanics",
                description: "Engineered to prevent metallic particulate shedding during the homogenization process. No lead, no zinc, no mystery alloys.",
                devices: ["Santa Cruz Shredder: 2-Piece, 3-Piece", "Flower Mill: Premium Edition"],
                icon: Cpu
              },
              {
                tier: "Tier 5",
                title: "Hydrated Particulate Filters",
                subtitle: "Clinical Glassware",
                description: "Borosilicate glass manifolds designed for autoclave sterilization and maximum particulate capture through hydration.",
                devices: ["MJ Arsenal: Standard Series", "Heir: Water Pipe"],
                icon: Droplets
              }
            ].map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="p-8 rounded-[2rem] border border-pink-50 bg-pink-50/10 hover:border-pink-200 transition-all group"
              >
                <div className="flex justify-between items-start mb-6">
                  <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center text-pink-400 shadow-sm group-hover:scale-110 transition-transform">
                    <item.icon className="w-5 h-5" />
                  </div>
                  <span className="text-[10px] font-black text-pink-300 uppercase tracking-widest">{item.tier}</span>
                </div>
                <h4 className="text-xl font-bold text-neutral-900 mb-1">{item.title}</h4>
                <p className="text-[10px] font-black text-pink-500 uppercase tracking-widest mb-4">{item.subtitle}</p>
                <p className="text-neutral-500 text-sm leading-relaxed mb-6 font-serif italic">
                  {item.description}
                </p>
                <div className="space-y-2">
                  {item.devices.map((device, j) => (
                    <div key={j} className="text-[11px] font-bold text-neutral-700 flex items-center gap-2">
                      <div className="w-1 h-1 bg-pink-300 rounded-full" />
                      {device}
                    </div>
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Verification Matrix Table */}
      <section className="py-24 md:py-40 bg-[#FDFCFD]">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16 md:mb-24">
            <span className="text-[10px] font-black text-pink-400 uppercase tracking-[0.5em] mb-4 block">FORMAL AUDIT PROTOCOL</span>
            <h3 className="text-4xl md:text-6xl font-serif text-neutral-900 tracking-tight">The MGV-1 Verification Matrix</h3>
          </div>

          <div className="overflow-hidden rounded-[2.5rem] border border-pink-100 shadow-2xl shadow-pink-500/5 bg-white mb-20">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse min-w-[1000px]">
                <thead>
                  <tr className="bg-pink-50/50 border-b border-pink-100">
                    <th className="px-10 py-8 text-[11px] font-black text-pink-500 uppercase tracking-widest w-[20%]">Audit Domain</th>
                    <th className="px-10 py-8 text-[11px] font-black text-pink-500 uppercase tracking-widest w-[40%]">Compliance Standard</th>
                    <th className="px-10 py-8 text-[11px] font-black text-pink-500 uppercase tracking-widest">Risk Benchmark</th>
                  </tr>
                </thead>
                <tbody className="text-neutral-600 font-serif">
                  {[
                    {
                      domain: "Vapor Path Composition",
                      sub: "Chemistry",
                      standard: "Hermetically isolated airpath ≥ 98% composed of ISO 3585 / Borosilicate 3.3, Grade 2 Titanium, or 316L Stainless Steel.",
                      fail: "FAIL: LEACHATE EXPOSURE - Air path intersection with circuit boards (PCB), lead-bearing solder, or non-food-grade alkaline battery housings."
                    },
                    {
                      domain: "Thermodynamic Stability",
                      sub: "Physics",
                      standard: "Precision Thermoregulation Control (PTC) maintaining ≤ ± 2°F active stability during maximum cubic airflow (> 15L/min).",
                      fail: "FAIL: THERMAL RUNAWAY - Surface temperatures breaching the 455°F combustion threshold, inducing carbon monoxide or benzene synthesis."
                    },
                    {
                      domain: "Molecular Adhesion",
                      sub: "VOC Mitigation",
                      standard: "Total elimination of industrial cyanoacrylates or epoxies in high-heat zones. Component seals must utilize USP Class VI friction or compression fitting.",
                      fail: "FAIL: CHEMICAL OFF-GASSING - Presence of manufacturing residues, flux, or un-vetted adhesives that activate at operational temperatures (> 300°F)."
                    },
                    {
                      domain: "Fracture Mechanics",
                      sub: "Domain: Structural",
                      standard: "Polarized light verification of glass annealing uniformity. Coefficient of Linear Thermal Expansion (3.3 × 10⁻⁶ K⁻¹) must be consistent across the manifold.",
                      fail: "FAIL: PARTICULATE RELEASE - Un-annealed glass with localized stress concentrations susceptible to micro-fracture \"dusting\" during thermal shock cycles."
                    },
                    {
                      domain: "Bio-Security & Hygiene",
                      sub: "Domain: Biology",
                      standard: "Autoclave-Compatible Geometry. Surfaces must withstand 250°F steam or 91% ISO immersion without material pitting or oxidative decay.",
                      fail: "FAIL: BIO-FILM ACCUMULATION - Fixed internal reservoirs or non-removable mouthpieces that trap moisture and botanical debris, creating un-sanitizable pathogen traps."
                    },
                    {
                      domain: "Pneumatic Control",
                      sub: "Domain: Aerodynamics",
                      standard: "Verification of standardized airflow resistance (≤ 2.0 inH₂O). Integrated Pressure Regulation Valves to prevent high-velocity aerosol throat irritation.",
                      fail: "FAIL: RESPIRATORY STRESS - Excessive draw resistance or turbulent flow geometry that induces secondary pulmonary irritation unrelated to the medicine."
                    },
                    {
                      domain: "Logic Redundancy",
                      sub: "Domain: Safety Systems",
                      standard: "Dual-layer protection: Software PID loop monitoring paired with a Physical Thermal Fuse (fail-safe) to isolate power during controller failure.",
                      fail: "FAIL: SYSTEMIC FAILURE - Single-point failure potential where a software bug allows unchecked heater activation during high-current charging or operation."
                    },
                    {
                      domain: "Metallurgical Traceability",
                      sub: "Domain: Metallurgy",
                      standard: "Certificate of Conformance (CoC) verifying AISI 316L or ASTM B265 Grade 2 Titanium. Zero zinc, lead, or chromium-plating in aerosol zones.",
                      fail: "FAIL: HEAVY METAL TOXICITY - Evidence of surface flaking, oxidative pitting, or the use of unidentified \"mystery alloys\" in the heat-exchange manifold."
                    }
                  ].map((row, i) => (
                    <tr key={i} className="border-b border-neutral-50 hover:bg-neutral-50/30 transition-colors">
                      <td className="px-10 py-10">
                        <div className="font-bold text-neutral-900 not-italic text-lg mb-1">{row.domain}</div>
                        <div className="text-[10px] font-bold text-pink-400 uppercase tracking-wider">{row.sub.startsWith('Domain') ? row.sub : `Domain: ${row.sub}`}</div>
                      </td>
                      <td className="px-10 py-10 italic text-lg leading-relaxed">
                        {row.standard}
                      </td>
                      <td className="px-10 py-10 text-neutral-500 leading-relaxed bg-red-50/10">
                        <span className="text-red-400 font-bold uppercase text-[10px] block mb-2">{row.fail.split(' - ')[0]}</span>
                        {row.fail.split(' - ')[1]}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* IN-DEPTH EXPLANATION SECTION */}
          <div className="max-w-4xl mx-auto space-y-24">
            {/* INTRODUCTION */}
            <div className="space-y-8">
              <h4 className="text-3xl md:text-4xl font-serif text-neutral-900 leading-tight">Giving Life to the MGV-1: The Blueprint for Respiratory Safety</h4>
              <div className="prose prose-neutral max-w-none text-neutral-600 font-serif italic text-lg md:text-xl leading-relaxed space-y-6">
                <p>
                  For decades, the market for thermal extraction has operated in a legal and clinical "gray zone." Devices were sold as novelties, lifestyle gadgets, or "for aromatherapy use only," allowing manufacturers to bypass the rigorous material science standards required for medical equipment. This ends with the MGV-1 Protocol.
                </p>
                <p>
                  The Medical-Grade Verification (Level 1) is not just a checklist; it is an active defense system for the human respiratory tract. We exist because "FDA-cleared plastics" are not enough when they are heated to 450°F. We exist because patients deserve to know if they are inhaling Grade 2 Titanium or a mystery alloy sourced from the lowest bidder.
                </p>
                <p>
                  To populate the interactive Audit lab, we pull directly from the MGV-1 Medical Verification Framework. Out of the 1,649 items in the catalog, only 39 distinct lines cleared the data thresholds. These are the specific devices identified as MGV-1 contenders, backed by exact material science justifications.
                </p>
              </div>
            </div>

            {/* COMPREHENSIVE BREAKDOWN */}
            <div className="space-y-12">
              <ExpandableSection 
                number="01"
                title="Who it Serves"
                content={
                  <>
                    <p className="text-neutral-900 font-bold not-italic border-l-2 border-pink-200 pl-6 py-1">
                      The MGV-1 framework is the definitive safety standard for patients across the entire Clinical Therapeutic Spectrum. Our protocol is designed to protect those managing Oncological and Palliative needs, Neuro-Immunological disorders, Refractory Chronic Pain, and Behavioral Health complexities.
                    </p>
                    <p>
                      Living with a chronic or terminal condition is an exhaustive exercise in risk management. Whether you are navigating an autoimmune disorder, oncology care, or refractory chronic pain, your body is already working overtime. You shouldn’t have to spend your limited energy wondering if your delivery hardware is off-gassing industrial glues or leaching heavy metals into your lungs.
                    </p>
                    <p>
                      The MGV-1 protocol is for the person who cannot afford a "minor" impurity. It serves the immuno-compromised, the palliative patient, and those managing neurological or spinal injuries where respiratory inflammation is a major physiological setback.
                    </p>
                  </>
                }
                layman="This standard was created specifically for people living with serious, long-term, or life-limiting health conditions who depend on these devices every day. Many patients already have enough to worry about with their health. The MGV-1 removes that uncertainty by holding every device to hospital-grade safety standards."
              />

              <ExpandableSection 
                number="02"
                title="The Path to Legal Standing"
                content={
                  <>
                    <p className="text-neutral-900 font-bold not-italic">Our final goal is the formal recodification of these devices. By adhering to ISO 13485 and HCPCS taxonomies, we are building the case for insurance coverage. We are moving from "vape shops" to "DME Suppliers," ensuring that medical-grade extraction is recognized as a human right.</p>
                    <p>Right now, the industry is stuck in a legal gray area. High-end hardware is sold as "lifestyle accessories" because most retailers want to avoid the technical and regulatory burden of a clinical classification. This isn't just a labeling issue; it’s a barrier to care.</p>
                    <div className="space-y-4 not-italic">
                      <h6 className="text-[10px] font-black text-pink-500 uppercase tracking-widest">The Execution Strategy:</h6>
                      <ul className="space-y-4 text-sm">
                        <li className="pl-4 border-l border-neutral-200"><span className="font-bold text-neutral-900">Material Accountability:</span> We require a comprehensive material audit for every device in our clinical silo.</li>
                        <li className="pl-4 border-l border-neutral-200"><span className="font-bold text-neutral-900">Financial Infrastructure:</span> We are navigating the specialized financial rails that bridge the gap between retail checkouts and pre-tax health dollars.</li>
                        <li className="pl-4 border-l border-neutral-200"><span className="font-bold text-neutral-900">Clinical Documentation:</span> By pairing engineering teardowns with verified medical necessity, we are providing the "technical rebuttal" that insurance carriers require.</li>
                      </ul>
                    </div>
                  </>
                }
                layman="Right now, these devices are often treated like recreational toys, which means patients usually have to pay the full price themselves. Our long-term goal is to change that. We are working to get these devices officially recognized by insurance companies as legitimate medical equipment."
              />

              <ExpandableSection 
                number="03"
                title="The Case for Harm Reduction Economics"
                content={
                  <>
                    <p>The current healthcare model is reactive. It waits for respiratory damage to happen and then bills for the treatment. We are advocating for a proactive shift. By reclassifying precision thermal extraction as <span className="not-italic font-bold text-neutral-900">Respiratory Harm Reduction</span>, we are addressing the root of the risk: <span className="not-italic font-bold text-neutral-900">Combustion</span>.</p>
                    <p>Standard "smoke shop" hardware is often built with materials that begin to degrade at the very temperatures required for effective titration. When a patient uses sub-standard hardware, they aren't just getting a poor experience; they are potentially inhaling heavy metal particulates and polymer off-gassing.</p>
                  </>
                }
                layman="Healthcare today usually waits until someone gets sick and then pays to treat the damage. We believe it makes more sense to prevent harm in the first place. Investing in safe hardware now is far cheaper than paying for the medical consequences of unsafe hardware years down the road."
              />

              <ExpandableSection 
                number="04"
                title="Technical Documentation & Traceability"
                content={
                  <>
                    <p>Every device that clears the MGV-1 audit is issued a comprehensive <span className="not-italic font-bold text-neutral-900">Clinical Data Pack</span>. We don’t expect a patient or a healthcare provider to just "take our word for it." This packet includes the full engineering teardown report, categorized Material Safety Data Sheets (MSDS), and the specific HCPCS billing alignment for that unit.</p>
                    <p>A central component of this documentation is the <span className="not-italic font-bold text-neutral-900">Material Bill of Lading (MBL)</span>. In the medical industry, if you can't prove what a device is made of, it doesn't exist. We mandate that manufacturers provide a line-item account of every material that touches the airpath.</p>
                  </>
                }
                layman="We don’t just say “trust us” when it comes to safety. Every device we approve comes with complete, detailed paperwork that proves exactly what materials were used and how the device was built. This level of transparency allows doctors and patients to have real confidence."
              />

              <ExpandableSection 
                number="05"
                title="Quality Assurance & Continuous Audit"
                content={
                  <>
                    <p>The MGV-1 is not a one-and-done certification. As materials like PEEK polymers and ceramic binders evolve, our thresholds adjust. We are constantly monitoring the metallurgical leaching data and thermal stability reports from our production nodes. If a manufacturer changes their material source to a lower-grade alloy, they lose their MGV-1 status instantly.</p>
                    <p>Our continuous audit also mandates <span className="not-italic font-bold text-neutral-900">Autoclave-Compatible Geometry</span>. A medical tool is a liability if it cannot be thoroughly sanitized. To pass our audit, a device must be capable of being fully sanitized through high-concentration isopropyl submersion or high-heat steam sterilization.</p>
                  </>
                }
                layman="Safety isn’t a one-time check — it’s an ongoing commitment. We keep watching the manufacturers to make sure they don’t quietly switch to cheaper or unsafe materials later. We also require that every device can be thoroughly cleaned and sterilized (like medical equipment in a hospital)."
              />
            </div>

            {/* FIELD GUIDE / FAQ */}
            <div className="bg-white border border-pink-100 rounded-[2.5rem] p-10 md:p-16 shadow-sm">
              <h4 className="text-2xl font-serif text-neutral-900 mb-10 text-center italic">The Auditor's Field Guide: Expanded Queries</h4>
              <div className="space-y-12 divide-y divide-pink-50">
                <FAQItem 
                  question="Why is 'Total Thermal Isolation' (TTI) a deal-breaker?"
                  answer="Most consumer devices are built with a 'form over function' mindset. If the air you inhale passes over the motherboard, the battery, or through a chamber held together by industrial adhesives, you aren't just inhaling medicine—you’re inhaling a chemical cocktail. If we can’t verify a hermetically sealed airpath that is physically separated from the electronics, the device is a respiratory liability. Period."
                />
                <FAQItem 
                  question="What is the actual risk of 'Mystery Metal' in cheaper devices?"
                  answer="'Mystery Metal' usually refers to cheap zinc alloys or chrome-plated plastics used in heat sinks and vapor paths to cut costs. Under thermal stress, these materials can flake or undergo oxidative breakdown, releasing heavy metal particulates (like lead or cadmium) directly into the aerosol. The MGV-1 requires 316L Surgical Steel or Grade 2 Titanium because these materials are bio-inert and stable at high temperatures."
                />
                <FAQItem 
                  question="How does the MGV-1 distinguish between 'Vaporization' and 'Combustion'?"
                  answer="This is where the math matters. Combustion—the literal burning of plant matter—starts at approximately 451°F. This process creates benzene, carbon monoxide, and tar. The MGV-1 mandates Precision Thermoregulation Control (PTC) that acts as a hard ceiling. We audit the heater’s ability to stay within the 'safe titration window' (typically 350°F–430°F)."
                />
                <FAQItem 
                  question="What is a 'Material Bill of Lading' (MBL) and why is it required?"
                  answer="In the medical world, you don't take a manufacturer's word for it; you check their receipts. An MBL is a technical document that lists every single material used in the construction of a device. We require this document because it’s the only way to perform a legitimate cytotoxicity audit. If a brand says their device is 'medical-grade' but won't provide an MBL, they're using the term for marketing, not for medicine."
                />
                <FAQItem 
                  question="Does insurance cover the accessories, or just the extraction device?"
                  answer="We have to be surgical here to protect the integrity of the claim. Generally, insurance and HSA/FSA funds are designated for the Durable Medical Equipment (DME)—the primary delivery tool itself. While the extraction unit is billable, 'lifestyle' accessories like cleaning kits or storage jars are often excluded. Our system is designed to segregate these SKUs at the point of sale."
                />
                <FAQItem 
                  question="How does the MGV-1 manage the risk of Bio-Film and Pathogen Trap?"
                  answer="In the medical world, if you can’t clean it, you can’t use it. Most consumer glassware and electronic rigs feature complex, non-removable internal geometries that are impossible to fully sanitize. Over time, these areas capture moisture and organic material, creating a 'Bio-Film'. Our audit requires Autoclave-Compatible Geometry. If a device has a 'hidden' reservoir or a non-removable mouthpiece that traps moisture, it is an immediate clinical fail."
                />
                <FAQItem 
                  question="Why is 'Chain of Custody' more important than the brand name on the box?"
                  answer="You can buy a Storz & Bickel or a DaVinci from a hundred different sites, but if they aren't a Verified Distribution Node, you have no guarantee of the material's integrity. The market is flooded with high-end clones that look identical but use lead-based solder and un-vetted plastics. Pixie’s Pantry operates as a closed-loop system. We don't drop-ship because we can't audit what we can't touch."
                />
                <FAQItem 
                  question="What is the 'Clinical vs. Recreational' Data Threshold?"
                  answer="The difference between a 'vape' and a TED is the data backing it. Most brands market to 'vibes'; we market to 'specs.' To pass the MGV-1, a product must cross our Data Threshold, involving a 5-step engineering cross-reference. We look for specific material markers. If a product lacks this transparency in its technical manual, our script flags it for manual rejection."
                />
              </div>
            </div>

            <div className="mt-20 flex flex-col md:flex-row justify-between items-center gap-6 border-t border-pink-50 pt-10">
              <p className="text-[10px] text-neutral-400 font-bold uppercase tracking-widest">Protocol Version: 1.0.4 — Compiled by the Auditor Node.</p>
              <div className="flex gap-4">
                <div className="px-4 py-2 border border-pink-100 rounded-full text-[9px] font-black text-pink-400 uppercase">ISO 13485 Alignment</div>
                <div className="px-4 py-2 border border-pink-100 rounded-full text-[9px] font-black text-pink-400 uppercase">ASTM F2913 Standards</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* THE CLINICAL BRIDGE DATA SECTION */}
      <section className="py-24 md:py-40 bg-white relative overflow-hidden">
        <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-amber-50/30 rounded-full blur-[100px] -z-10 pointer-events-none"></div>
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-start">
            <div>
              <span className="text-[10px] font-black text-pink-400 uppercase tracking-[0.5em] mb-6 block">RESEARCH & VALIDATION</span>
              <h3 className="text-4xl md:text-5xl font-serif text-neutral-900 tracking-tight leading-tight mb-8">
                The Clinical Bridge: Reclassifying Hardware as DME
              </h3>
              <p className="text-neutral-500 text-lg md:text-xl font-serif italic leading-relaxed mb-10 antialiased">
                "The industry standard is to treat these as lifestyle accessories. Our standard is to treat them as Durable Medical Equipment (DME). To bridge this gap, we rely on hard engineering data and established healthcare taxonomies."
              </p>
              
              <div className="space-y-12">
                <div className="border-l-4 border-pink-100 pl-8">
                  <h5 className="font-black text-[11px] text-pink-500 uppercase tracking-widest mb-3">MATERIAL SCIENCE INTEGRITY</h5>
                  <p className="text-neutral-600 leading-relaxed">
                    Our laboratory-grade borosilicate glass utilizes a Coefficient of Linear Thermal Expansion of 3.3 × 10⁻⁶ K⁻¹. This specifies an extreme resistance to thermal shock, ensuring that the internal vapor path remains micro-fracture-free during rapid heating cycles. We only verify alloys like 316L Stainless and Grade 2+ Titanium due to their proven bio-inert properties and resistance to oxidative stress.
                  </p>
                </div>
                <div className="border-l-4 border-amber-100 pl-8">
                  <h5 className="font-black text-[11px] text-amber-600 uppercase tracking-widest mb-3">THERMODYNAMIC PURITY</h5>
                  <p className="text-neutral-600 leading-relaxed">
                    Combustion (&gt; 451°F) introduces benzene and carbon monoxide. The MGV-1 Framework mandates Precision Thermoregulation Control (PTC) to ensure active decarboxylation stays within the safe titration window. By maintaining a real-time stability of ≤ ± 2°F, we eliminate the risk of accidental combustion, transforming a 'vape' into a clinical Thermal Extraction Device (TED).
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-neutral-900 rounded-[3rem] p-10 md:p-16 text-white relative shadow-2xl overflow-hidden">
              <div className="absolute top-0 right-0 w-64 h-64 bg-pink-500/10 rounded-full blur-3xl"></div>
              
              <div className="relative z-10">
                <h4 className="text-2xl font-serif mb-10 text-pink-100 italic">Healthcare Integration Registry</h4>
                
                <div className="space-y-10">
                  <div>
                    <span className="text-[9px] font-bold text-neutral-500 uppercase tracking-widest block mb-4">Common HCPCS Billing Codes</span>
                    <ul className="space-y-4 font-serif text-sm md:text-base">
                      <li className="flex justify-between border-b border-neutral-800 pb-2">
                        <span className="text-neutral-400 italic">E1399</span>
                        <span className="font-bold tracking-tight">DME, Miscellaneous</span>
                      </li>
                      <li className="flex justify-between border-b border-neutral-800 pb-2">
                        <span className="text-neutral-400 italic">E0570</span>
                        <span className="font-bold tracking-tight">Nebulizer, Ultrasonic</span>
                      </li>
                      <li className="flex justify-between border-b border-neutral-800 pb-2">
                        <span className="text-neutral-400 italic">E0619</span>
                        <span className="font-bold tracking-tight">Steam Vaporizer</span>
                      </li>
                    </ul>
                  </div>

                  <div>
                    <span className="text-[9px] font-bold text-neutral-500 uppercase tracking-widest block mb-4">The Lexicon Transition</span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs md:text-sm">
                      <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                        <div className="text-neutral-500 uppercase text-[8px] font-black mb-1">Legacy Term</div>
                        <div className="italic">"Vape / Vaporizer"</div>
                      </div>
                      <div className="p-4 bg-pink-500/10 rounded-2xl border border-pink-500/20">
                        <div className="text-pink-400 uppercase text-[8px] font-black mb-1">Clinical Reclassification</div>
                        <div className="font-bold text-pink-100">Thermal Extraction Device</div>
                      </div>
                      <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                        <div className="text-neutral-500 uppercase text-[8px] font-black mb-1">Legacy Term</div>
                        <div className="italic">"Bong / Water Pipe"</div>
                      </div>
                      <div className="p-4 bg-pink-500/10 rounded-2xl border border-pink-500/20">
                        <div className="text-pink-400 uppercase text-[8px] font-black mb-1">Clinical Reclassification</div>
                        <div className="font-bold text-pink-100">Hydrated Particulate Filter</div>
                      </div>
                      <div className="p-4 bg-white/5 rounded-2xl border border-white/10">
                        <div className="text-neutral-500 uppercase text-[8px] font-black mb-1">Legacy Term</div>
                        <div className="italic">"Grinder"</div>
                      </div>
                      <div className="p-4 bg-pink-500/10 rounded-2xl border border-pink-500/20">
                        <div className="text-pink-400 uppercase text-[8px] font-black mb-1">Clinical Reclassification</div>
                        <div className="font-bold text-pink-100">Botanical Homogenizer</div>
                      </div>
                    </div>
                  </div>

                  <div className="pt-6">
                    <p className="text-[10px] text-neutral-500 leading-relaxed italic antialiased">
                      Notice: Pixie's Pantry operates as a registered NPI holder (Taxonomy: 332B00000X). We are actively bridging the gap between high-end manufacturing (ISO 13485) and patient-led respiratory therapy.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER SIGNATURE */}
      <footer className="py-32 bg-pink-50/20 border-t border-pink-50 relative overflow-hidden text-center">
        <div className="max-w-4xl mx-auto px-6 relative z-10">
          <div className="w-20 h-[1px] bg-amber-200 mx-auto mb-10"></div>
          <p className="text-4xl font-serif italic text-neutral-700 leading-tight mb-12 antialiased">
            "Transparency isn't a feature—it's the foundation."
          </p>
          <div className="flex flex-col items-center">
            <span className="text-[12px] font-black text-pink-500 uppercase tracking-[0.6em] mb-2">— DUSTY LYN MCLEAN</span>
            <span className="text-[9px] font-bold text-neutral-400 uppercase tracking-widest">FOUNDER & CHIEF AUDITOR</span>
          </div>
        </div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-[15vw] font-serif italic opacity-[0.03] select-none pointer-events-none whitespace-nowrap">
          Pixie's Pantry
        </div>
      </footer>
    </div>
  );
}

const ExpandableSection = ({ number, title, content, layman }: any) => {
  const [isExpanded, setIsExpanded] = useState(false);
  return (
    <div 
      onClick={() => setIsExpanded(!isExpanded)} 
      className={`audit-card bg-white border border-pink-100 rounded-[2.5rem] p-10 md:p-14 cursor-pointer group transition-all duration-400 ${isExpanded ? 'border-pink-500 shadow-xl' : ''}`}
    >
      <div className="flex items-center gap-3 mb-6">
        <span className="w-8 h-8 rounded-full bg-pink-50 text-pink-500 flex items-center justify-center text-xs font-black">{number}</span>
        <h5 className="text-xl font-bold text-neutral-900 tracking-tight">{title}</h5>
      </div>
      <div className="text-neutral-500 font-serif leading-relaxed italic space-y-4">
        {content}
      </div>
      <div className="mt-10 text-[10px] text-pink-600 font-medium flex items-center gap-2 opacity-70">↓ CLICK FOR LAYMAN'S EXPLANATION</div>
      <AnimatePresence>
        {isExpanded && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="mt-8 pt-8 border-t border-pink-100 text-sm leading-relaxed">
              <span className="inline-block bg-pink-100 text-pink-700 text-[10px] font-black tracking-widest px-3 py-1 rounded-full mb-3">IN SIMPLE TERMS</span>
              <p className="text-neutral-600">
                {layman}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const FAQItem = ({ question, answer }: any) => (
  <div className="pt-10 first:pt-0">
    <h6 className="font-bold text-neutral-900 mb-4 tracking-tight">{question}</h6>
    <p className="text-neutral-500 font-serif leading-relaxed text-sm md:text-base italic">
      {answer}
    </p>
  </div>
);
