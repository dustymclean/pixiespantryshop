"""Editorial content for the pixiespantryshop.com link hubs.

Every entry: (partner_name_in_partners_json | None, display_name, what_it_is, why_i_recommend, override_url)
If partner_name is given, the outbound link is resolved from data/partners.json
(Impact tracking link, or an Awin deep link when AWIN_AFFID is configured).
"""

SHOP_URL = "https://pixies-pantry.com/shop"

HUBS = {
    "pixies-pantry": {
        "title": "Pixie's Pantry",
        "tagline": "The Standard for Explained-Before-You-Buy",
        "blurb": (
            "Hemp &amp; THCa flower, glass, and vaporizers &mdash; audited, explained, and sold "
            "without the headshop theatre. Everything below is either something we stock or a "
            "partner we send people to when we don't."
        ),
        "primary_cta": ("Shop Pixie's Pantry", SHOP_URL),
        "sections": [
            {
                "name": "Start Here",
                "note": "The store itself, and the pages people ask for most.",
                "items": [
                    (None, "Pixie's Pantry Shop", "Our own store: hemp &amp; THCa flower, glass, vaporizers and accessories, with $10 flat shipping and free shipping over $55.", "It's the only place where I control the sourcing, the photos, the descriptions and the aftercare. If I sell it, I've handled it.", SHOP_URL),
                    (None, "The Audit", "Our teardown and testing write-ups &mdash; material safety, thermal behaviour, cleanability, and what a device actually costs to own.", "This is the reason the store exists. Read the audit before you spend money anywhere, including here.", "https://pixies-pantry.com/the-audit/"),
                    (None, "Trust Center", "Sourcing, testing, compliance and return policy in one place.", "Transparency isn't a feature &mdash; it's the foundation. If you want the receipts, they're here.", "https://pixies-pantry.com/trust-center/"),
                    (None, "Current Deals", "Live discounts and bundles across the catalog.", "Where I put the actual price breaks instead of fake countdown timers.", "https://pixies-pantry.com/deals/"),
                ],
            },
            {
                "name": "Vaporizers &amp; Thermal Extraction",
                "note": "Devices that heat rather than burn. These are the brands I've tested hardest.",
                "items": [
                    ("Storz&Bickel", "Storz &amp; Bickel", "The German engineering house behind the Volcano, Mighty+, Venty and Crafty+, built under an ISO 13485 medical-device quality system.", "The only vaporizer maker whose manufacturing standard matches the medical claims people make about vaping. Expensive, and worth it &mdash; the Volcano outlives everything else in the room.", None),
                    ("DaVinci Vaporizers", "DaVinci Vaporizers", "American portable vaporizers (IQ series, ARTIQ) built around precision temperature control and inert airpaths.", "DaVinci publishes real material information about its airpath &mdash; zirconia and glass, not mystery alloys. Best pick when you want clinical control in a pocket device.", None),
                    ("Airvape USA", "AirVape", "US portable dry-herb vaporizer brand known for very slim, well-finished devices.", "The one I hand to people who found the Mighty too bulky. Solid vapour quality per dollar and genuinely pocketable.", None),
                    ("DynaVap", "DynaVap", "Battery-free, torch-heated dry herb vaporizers machined from stainless steel and titanium, with a temperature-indicating cap that clicks when it hits the right heat.", "No electronics, no charging, nothing to fail &mdash; it is the vaporizer I recommend to anyone tired of replacing a battery device every eighteen months. Made in Wisconsin, and the parts ecosystem means you can rebuild rather than rebuy.", None),
                    ("Dr.Dabber", "Dr. Dabber", "Concentrate-focused electronic rigs and pens (Boost, SwitchXL) with induction and e-nail heating.", "We're an authorized vendor, so I know the warranty is real. If you dab, this is the least fussy way to do it accurately.", None),
                ],
            },
            {
                "name": "Glass &amp; Filtration",
                "note": "Water pipes, rigs and modular systems &mdash; the part of the ritual you actually touch.",
                "items": [
                    ("Session Goods", "Session Goods", "Modern, minimalist glassware &mdash; bongs, pipes and stash kits designed to look like homewares.", "For anyone who wants good filtration without a novelty dragon on the shelf. Also the easiest glass on this page to clean.", None),
                    ("Vitae Glass", "VITAE Glass", "Modular water pipes that break down into parts for cleaning, customising and replacing.", "Modularity is the single biggest upgrade to glass hygiene. One cracked piece stops being a whole new bong.", None),
                    ("EYCE LLC", "EYCE", "Platinum-cured silicone pipes, rigs and accessories &mdash; effectively unbreakable.", "The right answer for travel, outdoors, and households with hardwood floors. Silicone that's actually rated for it, not craft-store rubber.", None),
                    ("Smoke Cartel", "Smoke Cartel", "One of the largest online headshops &mdash; 5,000+ products across glass, vapes and accessories.", "When I don't stock a shape you want, this is where the breadth is. 90-day cookie means their affiliate program is honest about how people shop.", None),
                    ("DankStop", "DankStop", "Long-running online glass and accessory retailer under High Tide.", "Deep bench of American-made borosilicate. Good place to compare joint sizes and percolator styles side by side.", None),
                    ("Cannabox", "Cannabox", "Monthly subscription box of glass, papers and accessories, plus a full online shop.", "The cheapest way to build an accessory drawer without buying 12 things at retail. Good gift, low commitment.", None),
                    ("Daily High Club Affiliate Program", "Daily High Club", "Subscription boxes and a large accessory catalog, heavy on papers, grinders and small glass.", "Similar idea to Cannabox with a different curation taste &mdash; pick whichever box matches how you actually smoke.", None),
                    ("Central Vapors", "Central Vapors", "Vape hardware and e-liquid retailer trading since 2013.", "Old guard, still shipping, still supporting what they sell &mdash; that longevity is rare in this category.", None),
                ],
            },
            {
                "name": "Accessories, Papers &amp; Hygiene",
                "note": "The consumables. Cheap to replace, expensive to get wrong.",
                "items": [
                (
                    "DHgate", "DHgate",
                    "Wholesale marketplace selling glass, grinders, storage and shop supplies straight "
                    "from the factories that produce them.",
                    "Useful for bulk consumables and cases where brand does not matter. I would not buy "
                    "anything you inhale through here &mdash; no lab reports, no material guarantees.",
                    None,
                ),
                    ("DaySavers", "DaySavers", "Rolling papers and cones tested to regulated-cannabis standards for heavy metals, microbials and pesticides.", "The only paper brand I've seen publish contaminant testing. You're inhaling the paper too &mdash; that matters more than the branding.", None),
                    ("King Palm", "King Palm", "Real palm-leaf wraps and cones, tobacco-free and hand-rolled.", "Slow, even burn without the chemical taste of flavoured blunt wraps. Good option if you're moving off tobacco leaf.", None),
                    ("Moose Labs LLC", "Moose Labs (MouthPeace)", "Silicone mouthpiece filters that sit between you and any shared pipe, filtering resin and bacteria.", "The most useful $10 accessory in the category, and the polite thing to carry in a session with friends.", None),
                    ("O2VAPE", "O2VAPE", "US Navy veteran- and woman-owned vape hardware maker with patented all-glass cartridge technology.", "All-glass carts avoid the plastic and cheap wick materials that dominate the market. Domestic, accountable, and they answer the phone.", None),
                    ("Mason Jar Lifestyle", "Mason Jar Lifestyle", "Lids, seals and accessories that turn ordinary Mason jars into proper storage.", "Best cheap cure-and-storage system there is. Glass, airtight, no plastic off-gassing into your flower.", None),
                    ("MOTIVAPE", "VapeBest", "Broad vapor-product retailer carrying mainstream vape hardware.", "Useful for hardware we deliberately don't carry. Listed for completeness, not as a headline pick.", None),
                ],
            },
            {
                "name": "Hemp, CBD &amp; Cultivation",
                "note": "21+ only. Compliance rules vary by state &mdash; check yours before ordering.",
                "items": [
                    ("Penguin CBD", "Penguin CBD", "Broad-spectrum CBD oils, gummies and creams with published third-party lab results.", "COAs on every batch, which is the entire bar for buying CBD online. If a brand won't show you the lab sheet, skip it.", None),
                    ("CBD For Life", "CBD For Life", "Topical-first CBD line &mdash; rubs, roll-ons and body care.", "Topicals are where CBD is easiest to judge for yourself. Good entry point for people who don't want to inhale anything.", None),
                    ("Hemp Bombs", "Hemp Bombs", "High-potency CBD gummies, capsules and tinctures produced from US-grown hemp.", "Consistent dosing per piece, which is what actually matters for a daily routine.", None),
                    ("Avid Hemp", "Avid Hemp", "US hemp brand covering CBD flower, edibles and vapes.", "Wide format range from one source, so you can compare delivery methods without changing brands.", None),
                    ("Enjoy Hemp", "Enjoy Hemp", "Hemp-derived cannabinoid products including Delta-8 and THCa formats.", "Relevant to what our own customers actually buy. Read your state law first &mdash; this category moves fast.", None),
                    ("Golden Goat CBD", "Golden Goat CBD", "Hemp-derived cannabinoid retailer with a large flower and edible selection.", "Good breadth for comparison shopping when you're learning the difference between cannabinoids.", None),
                    ("The Hemp Division", "The Hemp Division", "Hemp-derived product line spanning wellness and smokeable formats.", "Included for range. Judge it the same way as anything else here: labs first, marketing second.", None),
                    ("Blimburn Seeds", "Blimburn Seeds", "Cannabis seed bank with feminised and autoflower genetics.", "For legal home growers only, in states that allow it. Genetics documentation is better than most seed banks.", None),
                    ("TheBudGrower", "The Bud Grower", "Complete home-grow kits &mdash; tent, light, nutrients, instructions in one box.", "The least intimidating way into growing legally at home. One box, no guessing which fittings match.", None),
                    ("MushroomSupplies.com", "Mushroom Supplies", "Gourmet and functional mushroom cultivation supplies &mdash; substrates, grow kits and sterile equipment.", "Same mindset as the grow kits: legal cultivation, done properly, with equipment that isn't improvised.", None),
                ],
            },
        ],
    },

    "reviewed-by-dusty": {
        "title": "Reviewed by Dusty",
        "tagline": "Teardowns, Tools, and Honest Verdicts",
        "blurb": (
            "The review desk. This is the hardware I test with, the software that makes the "
            "reviews, and the gear I'd buy again with my own money. No brand pays for a verdict."
        ),
        "primary_cta": ("Read The Audit", "https://pixies-pantry.com/the-audit/"),
        "sections": [
            {
                "name": "The Review Desk",
                "note": "Where the work gets published.",
                "items": [
                    (None, "The Audit", "Long-form teardowns and standardised testing of consumption hardware.", "Every device gets the same protocol: material safety, dosage consistency, surgical-grade check, and sanitisation. Same test, every brand.", "https://pixies-pantry.com/the-audit/"),
                    (None, "Knowledge Base", "17+ explainer articles on how this hardware actually works.", "Start here if a review used a word you didn't recognise. No jargon left undefined.", "https://pixies-pantry.com/knowledge/"),
                    (None, "Comparison Guides", "Head-to-head pages for glass filtration, portable devices and desktop devices.", "For when you've narrowed it to two and want the difference stated plainly.", "https://pixies-pantry.com/compare-portable-devices/"),
                ],
            },
            {
                "name": "Camera &amp; Capture Gear",
                "note": "What the photos and teardown video are shot on.",
                "items": [
                    ("Leica Camera", "Leica", "German camera manufacturer &mdash; M rangefinders, SL and Q series, and the optics behind them.", "Aspirational, not casual. Leica glass renders material texture (glass, anodising, machining marks) more honestly than anything else I've shot product on.", None),
                    ("Ulanzi", "Ulanzi", "Affordable creator accessories: tripods, lights, mounts, cages and phone rigs.", "80% of the useful shot is lighting and a stable mount, and Ulanzi sells both for the price of a lens cap. Highest value-per-dollar on this page.", None),
                    ("APEXEL USA INC.", "Apexel", "Phone lens attachments including macro and microscope optics.", "Their macro lenses are how I get usable close-ups of airpath surfaces and screen mesh without a studio rig.", None),
                    ("Maono Technology Co., Ltd", "Maono", "Budget-to-mid USB and XLR microphones for podcasting and voiceover.", "Bad audio kills a good review faster than bad video. Maono is the cheapest way to sound legitimate.", None),
                    ("VSGO", "VSGO", "Camera cleaning and maintenance gear &mdash; sensor swabs, air blowers, lens kits.", "Boring, and it protects thousands of dollars of glass. Buy it once.", None),
                ],
            },
            {
                "name": "Editing, AI &amp; Publishing Software",
                "note": "The stack behind every post, video and product page.",
                "items": [
                    ("Viktor", "Viktor", "An AI employee platform: you connect it to email, Slack, Drive, Sheets, GitHub and your affiliate networks, and it does work inside those tools rather than just answering questions about them.", "It writes and runs its own scripts, so it built and now maintains this entire promo-code system &mdash; 455 merchant pages, refreshed weekly against Awin and Impact. There is no coupon for it; the signup link on my page is a referral link, and I say so on the page.", None),
                    ("CapCut Affiliate Program", "CapCut", "Video editor for desktop and mobile with auto-captions, templates and background removal.", "Fastest path from raw teardown footage to something watchable on TikTok. The auto-caption alone saves an hour per video.", None),
                    ("Krisp", "Krisp", "AI noise cancellation and meeting transcription that sits on top of any mic or call app.", "I record in a house, not a studio. Krisp removes the HVAC and the dog and nothing else.", None),
                    ("Bluehost", "Bluehost", "Shared and managed WordPress hosting with domains and one-click installs.", "The cheap on-ramp for a first WordPress site. Fine to start on, plan to outgrow it.", None),
                    ("Crazy Domains Affiliate Program", "Crazy Domains", "Domain registration, hosting and business email.", "Where you go when the .com you want is taken and you need to compare twelve extensions fast.", None),
                    ("101 Blockchains", "101 Blockchains", "Structured certification training in blockchain and Web3 fundamentals.", "For people who want the vocabulary and the credential rather than a YouTube rabbit hole.", None),
                ],
            },
            {
                "name": "Business Back Office",
                "note": "Boring infrastructure that keeps a one-person operation legal and paid.",
                "items": [
                    ("BusinessAnywhere LLC", "Business Anywhere", "LLC formation, registered agent, virtual mailbox, EIN filing and online notary in one dashboard.", "Formed properly, with a real registered address that isn't your kitchen. This is step one for anyone monetising a hobby.", None),
                    ("Easyship Ambassador Program", "Easyship", "Multi-carrier shipping rate comparison and label generation for ecommerce.", "Shipping is the second biggest line item in a small store. Easyship is how you stop overpaying one carrier out of habit.", None),
                    ("Talkroute Affiliate Program", "Talkroute", "Virtual business phone system that routes a real business number to your devices.", "Keeps your personal cell off the internet while still answering every call.", None),
                    ("SentryPC", "SentryPC", "Cloud-based computer monitoring, filtering and time management.", "Practical for family devices and for locking a shared work machine to work.", None),
                    ("Bitdefender", "Bitdefender", "Antivirus and endpoint security for Windows, macOS, Android and iOS.", "One compromised laptop takes down a store, a mailbox and a payment processor at once. Cheap insurance.", None),
                    ("Supplies Outlet", "Supplies Outlet", "Discount printer ink and toner, including compatible cartridges.", "We print labels, inserts and event material constantly. OEM ink pricing is a scam and this is the fix.", None),
                    ("Instant Funding", "Instant Funding", "Funding platform for traders and small operators seeking capital.", "Listed for transparency because it's in my portfolio. High-risk category &mdash; read every term before you fund anything.", None),
                ],
            },
            {
                "name": "Tech I Actually Use",
                "note": "Consumer hardware that survived long enough to get recommended.",
                "items": [
                    ("DynaVap", "DynaVap", "Battery-free thermal-extraction vaporizer, machined in Wisconsin from stainless steel and titanium.", "I keep coming back to it in teardowns because there is almost nothing to tear down &mdash; no board, no cell, no firmware. Serviceable with a screwdriver and a $6 o-ring kit, which is rare in this category. Code DUSTY for 10% off.", None),
                (
                    "DHgate", "DHgate",
                    "Factory-direct marketplace for electronics parts, camera accessories, cables, cages "
                    "and rigging &mdash; often the same units sold under Western brand names.",
                    "Where I source cheap accessories worth testing before recommending. Slow shipping and "
                    "uneven quality control are the trade for the price.",
                    None,
                ),
                    ("AnkerSOLIX", "Anker SOLIX", "Portable power stations and solar generators from Anker.", "Mississippi storms take the power out. A SOLIX runs the router, the lights and a laptop through it.", None),
                    ("Eufy US", "Eufy", "Smart home cameras, robot vacuums and doorbells with local storage options.", "The local-storage models mean footage of your front door doesn't have to live on someone's cloud.", None),
                    ("SimpliSafe Home Security", "SimpliSafe", "DIY home security system with optional professional monitoring, no contract.", "Renter-friendly, no drilling, no lock-in. Good fit for a home-run business holding inventory.", None),
                    ("Plaud US", "PLAUD", "AI voice recorders that transcribe and summarise meetings and notes.", "I talk through teardowns while my hands are busy. This turns that into usable notes.", None),
                    ("AtomStack", "AtomStack", "Desktop laser engravers and cutters for small-batch fabrication.", "How you get branded packaging, signage and event props without a print vendor and a minimum order.", None),
                    ("Roborock Amazon Seller", "Roborock", "Robot vacuums and mops with lidar mapping.", "A shop that photographs glass has to be dust-free. This runs while I sleep.", None),
                    ("Mount-It!", "Mount-It!", "Monitor arms, TV mounts, standing desk converters and ergonomic office hardware.", "Cheapest fix for the neck pain that comes with editing 8 hours a day.", None),
                ],
            },
        ],
    },

    "mellow-pixie": {
        "title": "Mellow Pixie",
        "tagline": "The Operator Behind the Pantry",
        "blurb": (
            "The person, not the storefront. Travel, everyday carry, wellness, home and the small "
            "luxuries that make a long build survivable. If it's here, it's in the house or in the bag."
        ),
        "primary_cta": ("Visit Pixie's Pantry", SHOP_URL),
        "sections": [
            {
                "name": "Travel &amp; Connectivity",
                "note": "Data abroad without a roaming bill. Buy the eSIM before you fly.",
                "items": [
                    ("Airalo", "Airalo", "The largest travel eSIM marketplace &mdash; buy a local data plan for 200+ countries and install it by QR code.", "First one I recommend because coverage and pricing are consistent everywhere. No SIM tray, no airport kiosk, no surprise roaming invoice.", None),
                    ("US Mobile Inc.", "US Mobile", "US carrier running on major networks with unusually flexible, cheap plans.", "Half the price of the big three for the same towers. If you're on a legacy plan you're donating money.", None),
                    ("Helium Mobile", "Helium Mobile", "US mobile service that offloads to a community-built wireless network to cut the price.", "Genuinely cheap nationwide coverage and an interesting model. Check coverage on your exact routes first.", None),
                    ("Amigo eSIM", "Amigo eSIM", "Prepaid travel eSIM plans with regional bundles.", "Good backup provider &mdash; I keep two eSIM vendors installed so one bad network isn't a dead phone.", None),
                    ("esimcards", "eSIMCards", "Travel eSIM store with country and multi-country data packages.", "Handy for multi-country trips where one regional plan beats five local ones.", None),
                    ("Total Wireless", "Total Wireless", "No-contract US prepaid phone service on a major network.", "Straightforward prepaid without a credit check. Good second line for a business number.", None),
                    ("VEGAS.com", "VEGAS.com", "Las Vegas hotels, shows and attraction tickets in one booking site.", "Where I price out trade-show trips. Bundling the room and the show beats booking them apart.", None),
                    ("Airport Transfer Portal", "Airport Transfer Portal", "Pre-booked private airport transfers worldwide.", "Book the ride before you land and the trip starts calm instead of in a taxi queue.", None),
                ],
            },
            {
                "name": "Points, Miles &amp; Loyalty",
                "note": "Points.com powers the official buy/transfer portals for these programs.",
                "items": [
                    ("Marriott Bonvoy - Points.com", "Marriott Bonvoy", "Official portal to buy, gift or transfer Marriott Bonvoy points.", "Topping up a balance is often far cheaper than paying cash for the last night of a stay. Do the maths first.", None),
                    ("Hilton Honors Rewards - Points.com", "Hilton Honors", "Official Hilton Honors points purchase and transfer portal.", "Same logic as Marriott. Watch for the periodic bonus sales &mdash; that's the only time buying points is a real deal.", None),
                    ("World of Hyatt - Points.com", "World of Hyatt", "Official World of Hyatt points portal.", "Hyatt points hold the highest real-world value per point of the big three chains.", None),
                    ("United Airlines MileagePlus - Points.com", "United MileagePlus", "Official portal for buying and transferring United miles.", "Useful to close a small gap on an award ticket you already found.", None),
                    ("Southwest Airlines Rapid Rewards - Points.com", "Southwest Rapid Rewards", "Official Southwest points portal.", "The practical one out of the South &mdash; two free bags and no change fees still beats a cheaper base fare.", None),
                    ("Alaska Airlines ATMOS Rewards - Points.com", "Alaska Mileage Plan", "Official Alaska Mileage Plan miles portal.", "Alaska's partner award chart is the best-kept secret in US loyalty.", None),
                    ("Air France KLM Flying Blue - Points.com", "Flying Blue", "Official Air France/KLM Flying Blue miles portal.", "Monthly Promo Rewards make Europe cheap if your dates are flexible.", None),
                    ("JetBlue TrueBlue - Points.com", "JetBlue TrueBlue", "Official JetBlue TrueBlue points portal.", "Points never expire and family pooling is free &mdash; rare and genuinely useful.", None),
                    ("Choice Privileges - Points.com", "Choice Privileges", "Official Choice Hotels points portal.", "Best coverage in small-town America, which is most of my actual driving.", None),
                    ("IHG Rewards Club - Points.com", "IHG One Rewards", "Official IHG points portal.", "Fourth-night-free on award stays is where the value is.", None),
                ],
            },
            {
                "name": "Home &amp; Everyday",
                "note": "Things in the house that earned their place.",
                "items": [
                (
                    "DHgate", "DHgate",
                    "China's big wholesale marketplace &mdash; the factory-direct source behind a lot of "
                    "what gets rebranded and resold at four times the price on Amazon.",
                    "Go here when you know exactly what part or accessory you want and do not care whose "
                    "logo is on it. Read the seller ratings, not the listing photos.",
                    None,
                ),
                    ("The Sill", "The Sill", "Live houseplants shipped potted, with care instructions matched to your light.", "Plants change a room more than furniture does, and The Sill actually tells you what will survive your window.", None),
                    ("Teak Warehouse", "Teak Warehouse", "Solid A-grade teak and all-weather outdoor furniture.", "Buy-once outdoor furniture. Teak greys and lasts twenty years instead of rusting in two summers.", None),
                    ("Brondell", "Brondell", "Bidet seats, water filtration and air purification for the home.", "A $99 bidet seat is the highest quality-of-life-per-dollar purchase in this entire hub. That's not a joke.", None),
                    ("Munchkin", "Munchkin", "Baby and toddler gear &mdash; feeding, bath, safety and cleaning.", "Family first. This is the stuff that's genuinely in our house.", None),
                    ("iTouchless", "iTouchless", "Sensor trash cans, air-purifying bins and touch-free home hardware.", "Touch-free bins in a kitchen and a workshop &mdash; obvious once you've lived with one.", None),
                    ("Gourmet Gift Basket Store", "Gourmet Gift Baskets", "Curated food and gift baskets for holidays and corporate sending.", "My default answer for a vendor thank-you when a branded box would be tacky.", None),
                    ("Snow Joe® + Sun Joe®", "Snow Joe + Sun Joe", "Electric outdoor tools &mdash; pressure washers, mowers, blowers and snow gear.", "Electric yard tools with no fuel to store. The pressure washer earns its keep before every pop-up event.", None),
                    ("Piscifun", "Piscifun", "Value-focused fishing reels, rods and tackle storage.", "Mississippi water. Good gear at a price that doesn't hurt when a rod goes in the lake.", None),
                ],
            },
            {
"name": "Wellness &amp; Recovery",
                "note": "Slow-down category. Nothing here is a medical claim.",
                "items": [
                    ("DynaVap", "DynaVap", "A torch-heated, battery-free vaporizer &mdash; a machined steel and titanium tip with a cap that clicks when it reaches temperature.", "The one piece of gear in my bag that never needs charging. It is slow, deliberate and mechanical, which is exactly the point on a quiet evening. Code DUSTY takes 10% off.", None),
                    ("Nalgene", "Nalgene", "Indestructible BPA-free water bottles made in the USA.", "One bottle, a decade, dishwasher safe. Hydration is the cheapest wellness intervention there is.", None),
                    ("HYDAWAY", "HYDAWAY", "Collapsible water bottles and food containers that pack flat.", "For a camera bag that's already full. Flat when empty, real bottle when you need one.", None),
                    ("Shakti Warrior", "Shakti Warrior", "Eco-conscious yoga mats, props and meditation gear.", "Mobility work after a day hunched over a light tent isn't optional past thirty.", None),
                    ("Max Recovery Clothing", "Max Recovery", "Compression and recovery apparel for training and post-workout.", "Trade show floors are twelve-hour standing days. Compression is the difference between day two and day three.", None),
                    ("PURTY BODY Affiliate Program", "Purty Body", "Small-batch natural body care.", "Independent maker, clean formulations, and a founder who answers her own email.", None),
                    ("Benigna Parfums LLC", "Benigna Parfums", "Independent fragrance house selling directly.", "Small luxury, no department store markup. Sample before you commit to a bottle.", None),
                ],
            },
            {
                "name": "Style, Gifts &amp; Small Luxuries",
                "note": "Great Gatsby energy on a Mississippi budget.",
                "items": [
                    ("Diamond Veneer Travel Jewelry", "Diamond Veneer", "Travel jewellery and simulated-stone pieces designed to be worn on the road.", "The sensible answer to travelling with anything you'd cry about losing.", None),
                    ("Baby Gold", "Baby Gold", "Fine 14k gold jewellery, personalised and stackable.", "Real gold, direct pricing, and the personalisation is done well rather than gimmicky.", None),
                    ("Grey State Apparel", "Grey State Apparel", "Elevated everyday apparel in sustainable fabrics.", "Fits the brand: quiet, well made, no logo shouting.", None),
                    ("TOTE & CARRY", "Tote &amp; Carry", "Bold luggage, duffels and backpacks from a Black-owned American brand.", "Loud in the right way, and the hardware holds up to real airport handling.", None),
                    ("Cosabella (US)", "Cosabella", "Italian-made lingerie and loungewear.", "Genuine Italian manufacturing at a price that isn't runway-insane. Reliable gift.", None),
                    ("Wine Express", "Wine Express", "Curated wine club and single-bottle delivery.", "Champagne coupes are the whole aesthetic here. This is how you keep them full.", None),
                    ("Memorialize Art (US)", "Memorialize Art", "Custom hand-drawn portraits from photographs.", "The gift that lands every time. Family, pets, people who are gone.", None),
                ],
            },
            {
                "name": "For the Household Zoo",
                "note": "Pets get a section. Non-negotiable.",
                "items": [
                    ("meowbox", "meowbox", "Monthly subscription box of cat toys and treats, with a box donated to shelters.", "The donation model is real, and the cats do not care about my quarterly targets.", None),
                    ("ZEAL PET", "Zeal Pet", "Pet supplies and accessories for cats and dogs.", "Everyday consumables without a boutique markup.", None),
                ],
            },
        ],
    },
}
