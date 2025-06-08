from flask import Flask
import os

app = Flask(__name__) 

@app.route('/')
def home(): 
  return ''' 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DHET PhD Scholarship | Finalized Venue Guide</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #005A9C; /* DHET Blue */
            --secondary: #2c3e50; /* Dark Blue-Gray */
            --accent: #D4AF37; /* Gold */
            --light: #f8f9fa;
            --dark: #34495e;
            --university-bg: linear-gradient(135deg, #005A9C, #3498db);
            --private-bg: linear-gradient(135deg, #2c3e50, #576d81);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        }

        body {
            background-color: #f0f4f8;
            color: var(--dark);
            line-height: 1.6;
        }

        header {
            background: var(--secondary);
            color: white;
            padding: 2.5rem 1.5rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        }

        .subtitle {
            font-size: 1.1rem;
            font-weight: 300;
            opacity: 0.9;
            max-width: 800px;
            margin: 0 auto;
        }

        .container {
            max-width: 1400px;
            margin: 30px auto;
            padding: 0 20px;
        }

        .controls {
            position: sticky;
            top: 10px;
            z-index: 100;
            background: rgba(255,255,255,0.98);
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(5px);
        }

        .filter-btn {
            background: white;
            border: 2px solid #ccc;
            color: var(--dark);
            padding: 10px 20px;
            border-radius: 30px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .filter-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .filter-btn.active {
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .filter-btn[data-filter="all"].active { background: var(--secondary); border-color: var(--secondary); }
        .filter-btn[data-filter="university"].active { background: var(--primary); border-color: var(--primary); }
        .filter-btn[data-filter="private"].active { background: #9b59b6; border-color: #9b59b6; }


        .search-container input {
            width: 300px;
            padding: 12px 20px;
            border-radius: 30px;
            border: 2px solid #ddd;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .search-container input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(0, 90, 156, 0.2);
            outline: none;
        }

        .venues-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 25px;
            margin-top: 20px;
        }

        .venue-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
        }

        .venue-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 25px rgba(0,0,0,0.12);
        }

        .card-header {
            padding: 20px;
            color: white;
            position: relative;
        }
        .venue-card.university .card-header { background: var(--university-bg); }
        .venue-card.private .card-header { background: var(--private-bg); }

        .rank-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(0,0,0,0.25);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.1rem;
            border: 2px solid rgba(255,255,255,0.5);
        }
        
        .venue-name { font-size: 1.5rem; margin-bottom: 5px; font-weight: 700; }
        .venue-location { font-size: 0.95rem; opacity: 0.9; }
        
        .stars {
            margin-top: 10px;
            font-size: 1.2rem;
            color: var(--accent);
        }

        .card-body {
            padding: 20px;
            flex-grow: 1;
        }
        
        .vibe-tag {
            background: var(--light);
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.9rem;
            margin-bottom: 15px;
            font-style: italic;
            border: 1px solid #e0e0e0;
        }
        
        .card-footer {
            padding: 15px 20px;
            background: var(--light);
            border-top: 1px solid #e9ecef;
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }
        
        .details-btn {
            background: var(--secondary);
            color: white;
            padding: 10px 20px;
            border-radius: 30px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: all 0.3s ease;
        }

        .details-btn:hover {
            background: var(--dark);
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }

        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: 1000;
            overflow-y: auto;
            padding: 20px;
            backdrop-filter: blur(5px);
            align-items: center;
            justify-content: center;
        }

        .modal-content {
            background: white;
            max-width: 800px;
            width: 100%;
            border-radius: 15px;
            overflow: hidden;
            animation: modalopen 0.4s ease-out;
            display: flex;
            flex-direction: column;
            max-height: 95vh;
        }

        @keyframes modalopen {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        .modal-header { padding: 25px 30px; color: white; position: relative; }
        .modal-body { padding: 25px 30px; overflow-y: auto; }
        
        .close-modal {
            position: absolute;
            top: 10px; right: 15px;
            font-size: 2rem; color: white;
            cursor: pointer; transition: all 0.3s ease;
            line-height: 1;
        }
        .close-modal:hover { transform: rotate(90deg); }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .info-card {
            background: var(--light);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid var(--primary);
        }
        .info-card h4 {
            margin-bottom: 10px;
            color: var(--secondary);
            display: flex; align-items: center; gap: 10px;
        }
        .info-card h4 .fa { color: var(--primary); }
        
        .pro-tip {
            background: #eef7ff;
            border-left: 4px solid var(--primary);
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        .pro-tip h3 { color: var(--primary); }
        .pro-tip ul { padding-left: 20px; }
        
        .modal-footer {
            padding: 15px 30px;
            background: var(--light);
            text-align: right;
            border-top: 1px solid #e0e0e0;
        }
        
        .btn-close-modal {
            background: #6c757d;
            color: white;
            padding: 10px 25px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
        }
        
        .btn-website {
            background: var(--primary);
            color: white;
            padding: 10px 25px;
            border: none;
            border-radius: 25px;
            text-decoration: none;
            margin-right: 10px;
            font-weight: 600;
        }

        /* Chart Section */
        .comparison-section { margin: 40px 0; padding: 30px; background: white; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
        .chart-container { height: 400px; margin-top: 20px; }
        
        footer { text-align: center; padding: 20px; margin-top: 40px; color: #7f8c8d; font-size: 0.9rem; }

    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>DHET PhD Scholarship Orientation</h1>
            <p class="subtitle">A Finalized Interactive Guide to the Top 10 Venues in Pretoria</p>
        </div>
    </header>

    <div class="container">
        <div class="controls">
            <button class="filter-btn active" data-filter="all"><i class="fas fa-globe-africa"></i> All Venues</button>
            <button class="filter-btn" data-filter="university"><i class="fas fa-university"></i> University Venues</button>
            <button class="filter-btn" data-filter="private"><i class="fas fa-briefcase"></i> Private Venues</button>
            <div class="search-container">
                <input type="text" id="search-input" placeholder="Search by name, location, vibe...">
            </div>
        </div>

        <div class="venues-container" id="venues-container">
            <!-- Venue cards will be dynamically inserted here -->
        </div>

        <div class="comparison-section">
            <h2><i class="fas fa-chart-bar"></i> Venue Rating Comparison</h2>
            <p>Compare key metrics across the top-ranked venues.</p>
            <div class="chart-container">
                <canvas id="comparison-chart"></canvas>
            </div>
        </div>
    </div>

    <div class="modal" id="venue-modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close-modal">×</span>
                <h2 id="modal-venue-name"></h2>
                <div class="stars" id="modal-stars"></div>
                <div class="venue-location"><i class="fas fa-map-marker-alt"></i> <span id="modal-location"></span></div>
            </div>
            <div class="modal-body">
                <div class="vibe-tag" id="modal-vibe"></div>
                
                <div class="info-grid">
                    <div class="info-card"><h4><i class="fas fa-users"></i> Capacity</h4><p id="modal-capacity"></p></div>
                    <div class="info-card"><h4><i class="fas fa-wifi"></i> Key Amenities</h4><p id="modal-amenities"></p></div>
                </div>
                
                <div class="info-card">
                    <h4><i class="fas fa-address-book"></i> Contact Information</h4>
                    <p id="modal-contact"></p>
                </div>
                
                <div class="pro-tip">
                    <h3><i class="fas fa-lightbulb"></i> Pro Tip: What to Confirm</h3>
                    <ul>
                        <li><strong>Pricing Model:</strong> Per-person rate vs. flat venue hire? What is included?</li>
                        <li><strong>Catering Packages:</strong> Ask for menus, costs, and dietary accommodation.</li>
                        <li><strong>AV Inclusions:</strong> Confirm if projector, mics, and tech support are included.</li>
                        <li><strong>Contingency Plans:</strong> Does the venue have a generator for load-shedding?</li>
                        <li><strong>Accessibility:</strong> Confirm wheelchair access to all relevant areas.</li>
                        <li><strong>Booking & Cancellation Policy:</strong> Get the deposit and cancellation terms in writing.</li>
                    </ul>
                </div>
            </div>
            <div class="modal-footer">
                <a href="#" target="_blank" rel="noopener noreferrer" class="btn-website" id="modal-website-btn">Visit Website</a>
                <button class="btn-close-modal">Close</button>
            </div>
        </div>
    </div>
    
    <footer>
        <p>Contributed by S Ndlovu</p>
        <p>Last Updated: June 2025</p>
    </footer>

    <script>
        const venues = [
            {
                id: 1, name: "Future Africa Campus (University of Pretoria)", rank: 1, type: "university", location: "Hatfield / Pretoria East",
                vibe: "Cutting-edge, scholarly, and modern", stars: 5,
                capacity: "Flexible spaces: 232-seat auditorium, 50-60 seat conference rooms.",
                amenities: "State-of-the-art AV, Uncapped Eduroam & Guest Wi-Fi, Secure Campus, Free Parking, On-site Catering, On-site Accommodation.",
                contact: "Email: info@futureafrica.science | Phone: +27 (0)12 420 6969",
                website: "https://www.futureafrica.science/our-campus/event-facilities/",
                search_terms: "research hub forward-thinking"
            },
            {
                id: 2, name: "UNISA Senate Hall", rank: 2, type: "university", location: "Muckleneuk, Central Pretoria",
                vibe: "Traditional academic prestige", stars: 5,
                capacity: "Seats up to 230, providing a grand setting for 50 scholars plus dignitaries.",
                amenities: "Integrated conference microphone system, translation booths, full AV support, secure campus.",
                contact: "Phone: 0800 00 1870 (General Enquiries)",
                website: "https://www.unisa.ac.za/sites/corporate/default/Contact-us/Conference-facilities",
                search_terms: "elegant formal wood panelling government district"
            },
            {
                id: 3, name: "The Capital Menlyn Maine", rank: 3, type: "private", location: "Menlyn, Pretoria East",
                vibe: "Modern, upscale, and professional", stars: 5,
                capacity: "Multiple venues, including large conference rooms (up to 300) and smaller boardrooms.",
                amenities: "High-standard AV, High-speed Wi-Fi, Secure paid underground parking, Full accessibility, On-site Catering, Luxury accommodation.",
                contact: "Phone: +27 (0)10 446 8045 | Email: menlyn@thecapital.co.za",
                website: "https://thecapital.co.za/menlyn/",
                search_terms: "corporate hotel"
            },
            {
                id: 4, name: "University of Pretoria - Kya Rosa", rank: 4, type: "university", location: "Hatfield, Main Campus Area",
                vibe: "Historic, intimate, and exclusive", stars: 4.5,
                capacity: "Ideal for smaller, intimate groups of 30-40 people.",
                amenities: "Unique ambiance, secure in-campus location, standard AV and Wi-Fi.",
                contact: "Email: upspace@up.ac.za (UP Venue Hire)",
                website: "https://www.up.ac.za/article/2749493/venues-on-campus",
                search_terms: "victorian house restored welcome reception"
            },
            {
                id: 5, name: "Javett-UP Arts Centre", rank: 5, type: "university", location: "Hatfield, South Campus",
                vibe: "Modern, artistic, and culturally rich", stars: 4.5,
                capacity: "Features a versatile 300-seat multi-purpose hall and gallery spaces.",
                amenities: "Professional AV & lighting, secure campus parking, full accessibility, inspiring backdrop.",
                contact: "Phone: +27 (0)12 420 3960",
                website: "https://javettup.art/",
                search_terms: "gallery museum sophisticated dinner"
            },
            {
                id: 6, name: "Casa Toscana Lodge", rank: 6, type: "private", location: "Lynnwood Manor, Pretoria East",
                vibe: "Elegant, full-service boutique", stars: 4,
                capacity: "Six conference venues that can cater for up to 150 delegates.",
                amenities: "Free high-speed Wi-Fi, secure on-site parking, on-site catering, accommodation.",
                contact: "Phone: +27 (0)12 348 8820 | Email: anette@casatoscana.co.za",
                website: "https://www.casatoscana.co.za/",
                search_terms: "4-star N1 highway"
            },
            {
                id: 7, name: "UNISA Muckleneuk Conference Centre", rank: 7, type: "university", location: "Muckleneuk, Central Pretoria",
                vibe: "Professional, academic, and functional", stars: 4,
                capacity: "Multiple venues including the Great Hall and Kopanong Chambers.",
                amenities: "Experienced catering team, full AV support, secure campus environment.",
                contact: "Phone: 0800 00 1870 (General Enquiries)",
                website: "https://www.unisa.ac.za/sites/corporate/default/Contact-us/Conference-facilities/Muckleneuk-Campus",
                search_terms: "reliable practical"
            },
            {
                id: 8, name: "Southern Sun Pretoria", rank: 8, type: "private", location: "Arcadia, Central Pretoria",
                vibe: "Traditional, formal, and corporate", stars: 4,
                capacity: "Eight flexible venues, from small boardrooms to halls for 500+ guests.",
                amenities: "Full conference services, secure parking, located in the embassy district.",
                contact: "Phone: +27 (0)12 444 5500",
                website: "https://www.southernsun.com/southern-sun-pretoria/meetings-events",
                search_terms: "classic hotel government"
            },
            {
                id: 9, name: "UP High Performance Centre (hpc)", rank: 9, type: "university", location: "Hatfield / Pretoria East",
                vibe: "Dynamic, sports-focused, and functional", stars: 3.5,
                capacity: "Seminar rooms and function venues suitable for corporate events and groups of ~50.",
                amenities: "On-site accommodation & catering, secure campus parking, standard AV facilities.",
                contact: "Phone: +27 (0)12 484 1718 | Email: events@hpc.co.za",
                website: "https://www.hpc.co.za/hospitality-25",
                search_terms: "team-building sports"
            },
            {
                id: 10, name: "Tshwane University of Technology (TUT)", rank: 10, type: "university", location: "Pretoria West",
                vibe: "Standard, functional university campus", stars: 3.5,
                capacity: "A wide variety of lecture halls, seminar rooms, and auditoriums.",
                amenities: "Secure campus, standard academic AV setups, campus Wi-Fi.",
                contact: "Phone: +27 (0)12 382 5911 (Main Switchboard)",
                website: "https://www.tut.ac.za",
                search_terms: "alternative solid practical"
            }
        ];

        const venuesContainer = document.getElementById('venues-container');
        const searchInput = document.getElementById('search-input');
        const filterButtons = document.querySelectorAll('.filter-btn');
        const modal = document.getElementById('venue-modal');
        const closeModalBtn = document.querySelector('.close-modal');
        const closeFooterBtn = document.querySelector('.btn-close-modal');
        let chart = null;

        function renderStars(rating) {
            const fullStars = Math.floor(rating);
            const halfStar = rating % 1 !== 0 ? 1 : 0;
            const emptyStars = 5 - fullStars - halfStar;
            let starsHTML = '';
            for (let i = 0; i < fullStars; i++) starsHTML += '<i class="fas fa-star"></i>';
            if (halfStar) starsHTML += '<i class="fas fa-star-half-alt"></i>';
            for (let i = 0; i < emptyStars; i++) starsHTML += '<i class="far fa-star"></i>';
            return starsHTML;
        }

        function renderVenues(venueList) {
            venuesContainer.innerHTML = '';
            if (venueList.length === 0) {
                venuesContainer.innerHTML = '<p>No venues match your criteria.</p>';
                return;
            }
            venueList.forEach(venue => {
                const card = document.createElement('div');
                card.className = `venue-card ${venue.type}`;
                card.dataset.id = venue.id;
                card.innerHTML = `
                    <div class="card-header">
                        <div class="rank-badge">#${venue.rank}</div>
                        <h3 class="venue-name">${venue.name}</h3>
                        <div class="venue-location">${venue.location}</div>
                        <div class="stars">${renderStars(venue.stars)}</div>
                    </div>
                    <div class="card-body">
                        <div class="vibe-tag">${venue.vibe}</div>
                        <p>${venue.amenities}</p>
                    </div>
                    <div class="card-footer">
                        <button class="details-btn" data-id="${venue.id}">View Details</button>
                    </div>
                `;
                venuesContainer.appendChild(card);
            });
        }

        function openModal(venueId) {
            const venue = venues.find(v => v.id === venueId);
            if (!venue) return;

            document.getElementById('modal-venue-name').textContent = venue.name;
            document.getElementById('modal-stars').innerHTML = renderStars(venue.stars);
            document.getElementById('modal-location').textContent = venue.location;
            document.getElementById('modal-vibe').textContent = venue.vibe;
            document.getElementById('modal-capacity').textContent = venue.capacity;
            document.getElementById('modal-amenities').textContent = venue.amenities;
            document.getElementById('modal-contact').textContent = venue.contact;
            
            const websiteBtn = document.getElementById('modal-website-btn');
            websiteBtn.href = venue.website;
            websiteBtn.style.display = venue.website ? 'inline-block' : 'none';

            const modalHeader = document.querySelector('.modal-header');
            modalHeader.className = 'modal-header';
            if(venue.type === 'university') modalHeader.classList.add('university');
            if(venue.type === 'private') modalHeader.classList.add('private');

            modal.style.display = 'flex';
        }
        
        function handleFilter() {
            const searchTerm = searchInput.value.toLowerCase();
            const activeFilter = document.querySelector('.filter-btn.active').dataset.filter;

            let filteredVenues = venues.filter(venue => {
                const matchesFilter = activeFilter === 'all' || venue.type === activeFilter;
                const matchesSearch = !searchTerm ||
                    venue.name.toLowerCase().includes(searchTerm) ||
                    venue.location.toLowerCase().includes(searchTerm) ||
                    venue.vibe.toLowerCase().includes(searchTerm) ||
                    venue.search_terms.toLowerCase().includes(searchTerm);
                return matchesFilter && matchesSearch;
            });
            renderVenues(filteredVenues);
        }

        function initChart() {
            const ctx = document.getElementById('comparison-chart').getContext('2d');
            const labels = venues.map(v => `#${v.rank} ${v.name}`);
            const ratings = venues.map(v => v.stars);
            
            if (chart) {
                chart.destroy();
            }

            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Star Rating',
                        data: ratings,
                        backgroundColor: venues.map(v => v.type === 'university' ? 'rgba(0, 90, 156, 0.7)' : 'rgba(155, 89, 182, 0.7)'),
                        borderColor: venues.map(v => v.type === 'university' ? 'rgba(0, 90, 156, 1)' : 'rgba(155, 89, 182, 1)'),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 5,
                            title: { display: true, text: 'Rating (out of 5)' }
                        },
                        x: { display: false }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                title: function(context) {
                                    return context[0].label;
                                }
                            }
                        }
                    }
                }
            });
        }
        
        // Event Listeners
        venuesContainer.addEventListener('click', e => {
            if (e.target.closest('.details-btn')) {
                const id = parseInt(e.target.closest('.details-btn').dataset.id);
                openModal(id);
            }
        });

        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                handleFilter();
            });
        });
        
        searchInput.addEventListener('input', handleFilter);
        closeModalBtn.addEventListener('click', () => modal.style.display = 'none');
        closeFooterBtn.addEventListener('click', () => modal.style.display = 'none');
        modal.addEventListener('click', e => {
            if (e.target === modal) modal.style.display = 'none';
        });

        // Initial render
        renderVenues(venues);
        initChart();
    </script>
</body>
</html>



  ''' 



if __name__ == "__main__": 
      app.run(debug=True, host='0.0.0.0', port=5001)
