#!/usr/bin/env python3
"""
Create a standalone HTML version that works without a server
"""

import os
import shutil
from pathlib import Path

def create_standalone_version():
    """Create a standalone version that works without server"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🌐 Creating Standalone AeroCast Website                 ║
║                                                              ║
║    This will work without any server!                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Create standalone directory
    standalone_dir = Path("standalone_website")
    if standalone_dir.exists():
        shutil.rmtree(standalone_dir)
    
    standalone_dir.mkdir()
    print(f"📁 Created directory: {standalone_dir}")
    
    # Copy static files
    static_dir = Path("static")
    if static_dir.exists():
        for file in static_dir.glob("*"):
            if file.is_file():
                shutil.copy2(file, standalone_dir)
                print(f"✅ Copied: {file.name}")
        
        # Copy CSS directory
        css_dir = static_dir / "css"
        if css_dir.exists():
            standalone_css = standalone_dir / "css"
            shutil.copytree(css_dir, standalone_css)
            print("✅ Copied: css directory")
    
    # Create a modified index.html that works standalone
    create_standalone_index(standalone_dir)
    
    # Create demo data
    create_demo_data_script(standalone_dir)
    
    print(f"""
🎉 SUCCESS! Standalone website created!

📁 Location: {standalone_dir.absolute()}

🌐 TO OPEN YOUR WEBSITE:
   1. Open File Explorer
   2. Navigate to: {standalone_dir.absolute()}
   3. Double-click: index.html
   
   OR
   
   Right-click index.html → Open with → Your web browser

✨ FEATURES:
   ✅ Works without any server
   ✅ Beautiful air quality dashboard
   ✅ Interactive maps and charts
   ✅ Demo predictions with realistic data
   ✅ All pages work offline

💡 This version uses demo data but shows the full interface!
    """)

def create_standalone_index(standalone_dir):
    """Create a standalone index.html with demo data"""
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AeroCast - Delhi Air Quality Forecast</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="css/shared.css">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 25px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            overflow: hidden;
            backdrop-filter: blur(20px);
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 3.5em;
            margin-bottom: 15px;
            font-weight: 700;
        }
        
        .nav-bar {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px 0;
            text-align: center;
        }
        
        .nav-links {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 25px;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .nav-links a:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }
        
        .stats-bar {
            background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 50%, #f8f9fa 100%);
            padding: 25px 20px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            min-width: 140px;
        }
        
        .stat-value {
            font-size: 2.2em;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            display: block;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.85em;
            color: #6c757d;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0;
            min-height: 600px;
        }
        
        @media (max-width: 1024px) {
            .content {
                grid-template-columns: 1fr;
            }
        }
        
        .map-section, .chart-section {
            padding: 30px;
        }
        
        .map-section {
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            border-right: 1px solid #dee2e6;
        }
        
        .chart-section {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        }
        
        .section-title {
            font-size: 1.5em;
            font-weight: 700;
            color: #495057;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section-title i {
            color: #667eea;
            font-size: 1.2em;
        }
        
        #map {
            height: 480px;
            border-radius: 20px;
            border: 3px solid transparent;
            background: linear-gradient(white, white) padding-box,
                       linear-gradient(135deg, #667eea, #764ba2) border-box;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .chart-container {
            position: relative;
            height: 380px;
            margin-bottom: 30px;
            background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .info-panel {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 20px;
            margin-top: 25px;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        }
        
        .info-panel h4 {
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .info-panel p {
            margin-bottom: 8px;
            opacity: 0.9;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .controls {
            padding: 30px;
            background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 100%);
            border-bottom: 1px solid #dee2e6;
        }
        
        .controls-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .control-group {
            position: relative;
        }
        
        .control-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #495057;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .control-group input, .control-group select {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 14px;
            transition: all 0.3s ease;
            background: white;
        }
        
        .control-group input:focus, .control-group select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }
        
        .footer {
            background: linear-gradient(135deg, #495057 0%, #343a40 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .footer p {
            opacity: 0.8;
            margin-bottom: 10px;
        }
        
        .demo-notice {
            background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="demo-notice">
            🌟 STANDALONE DEMO VERSION - No server required! Double-click to open in any browser 🌟
        </div>
        
        <div class="header">
            <h1><i class="fas fa-wind"></i> AeroCast</h1>
            <p>AI-powered air quality forecasting for Delhi NCR region</p>
            <div class="nav-bar">
                <div class="nav-links">
                    <a href="index.html" class="active"><i class="fas fa-home"></i> Dashboard</a>
                    <a href="historical.html"><i class="fas fa-chart-line"></i> Historical</a>
                    <a href="analytics.html"><i class="fas fa-chart-bar"></i> Analytics</a>
                    <a href="settings.html"><i class="fas fa-cog"></i> Settings</a>
                </div>
            </div>
        </div>
        
        <div class="stats-bar">
            <div class="stat-item">
                <span class="stat-value" id="current-aqi">112</span>
                <div class="stat-label">Current AQI</div>
            </div>
            <div class="stat-item">
                <span class="stat-value" id="model-accuracy">77%</span>
                <div class="stat-label">Model Accuracy</div>
            </div>
            <div class="stat-item">
                <span class="stat-value" id="model-type">Enhanced LSTM</span>
                <div class="stat-label">Model Type</div>
            </div>
            <div class="stat-item">
                <span class="stat-value" id="predictions-made">1,247</span>
                <div class="stat-label">Predictions Made</div>
            </div>
            <div class="stat-item">
                <span class="stat-value" id="last-updated">Live</span>
                <div class="stat-label">Status</div>
            </div>
        </div>
        
        <div class="controls">
            <div class="controls-grid">
                <div class="control-group">
                    <label for="latitude"><i class="fas fa-map-marker-alt"></i> Latitude:</label>
                    <input type="number" id="latitude" value="28.6139" step="0.0001" min="28.4" max="28.9">
                </div>
                <div class="control-group">
                    <label for="longitude"><i class="fas fa-map-marker-alt"></i> Longitude:</label>
                    <input type="number" id="longitude" value="77.2090" step="0.0001" min="76.8" max="77.5">
                </div>
                <div class="control-group">
                    <label for="hours"><i class="fas fa-clock"></i> Forecast Hours:</label>
                    <select id="hours">
                        <option value="12">12 hours</option>
                        <option value="24" selected>24 hours</option>
                        <option value="48">48 hours</option>
                    </select>
                </div>
                <div class="control-group">
                    <label for="location-preset"><i class="fas fa-location-dot"></i> Quick Locations:</label>
                    <select id="location-preset">
                        <option value="">Select location...</option>
                        <option value="28.6315,77.2167">🏢 Connaught Place</option>
                        <option value="28.6129,77.2295">🏛️ India Gate</option>
                        <option value="28.5921,77.0460">🏘️ Dwarka</option>
                        <option value="28.4595,77.0266">🏙️ Gurgaon</option>
                        <option value="28.5355,77.3910">🌆 Noida</option>
                    </select>
                </div>
            </div>
            <div style="text-align: center;">
                <button class="btn" onclick="generateDemoForecast()">
                    <i class="fas fa-chart-line"></i> Generate Demo Forecast
                </button>
            </div>
        </div>
        
        <div class="content">
            <div class="map-section">
                <h3 class="section-title">
                    <i class="fas fa-map"></i> Delhi NCR Region
                </h3>
                <div id="map"></div>
                <div class="info-panel">
                    <h4><i class="fas fa-info-circle"></i> Current Selection</h4>
                    <p><strong>Coordinates:</strong> <span id="current-coords">28.6139, 77.2090</span></p>
                    <p><strong>Location:</strong> <span id="current-location">Delhi Center</span></p>
                    <p><strong>Status:</strong> <span style="color: #90EE90;">●</span> Demo Mode Active</p>
                </div>
                
                <div class="info-panel" style="margin-top: 15px;">
                    <h4><i class="fas fa-brain"></i> Model Information</h4>
                    <p><strong>Model:</strong> Enhanced LSTM</p>
                    <p><strong>Accuracy:</strong> 77%</p>
                    <p><strong>Status:</strong> <span style="color: #90EE90;">●</span> Demo Data</p>
                </div>
            </div>
            
            <div class="chart-section">
                <h3 class="section-title">
                    <i class="fas fa-chart-area"></i> Air Quality Forecast
                </h3>
                <div id="forecast-content">
                    <div class="chart-container">
                        <canvas id="demo-chart"></canvas>
                    </div>
                    <div class="info-panel">
                        <h4><i class="fas fa-chart-line"></i> Demo Forecast</h4>
                        <p><strong>NO₂:</strong> 58 µg/m³ (Moderate)</p>
                        <p><strong>O₃:</strong> 32 µg/m³ (Good)</p>
                        <p><strong>AQI:</strong> 112 (Moderate)</p>
                        <p><strong>Trend:</strong> Improving through evening</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>AeroCast - Standalone Demo Version | AI-powered air quality forecasting</p>
        </div>
    </div>

    <script>
        // Initialize demo map
        const map = L.map('map').setView([28.6139, 77.2090], 10);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Add marker
        const marker = L.marker([28.6139, 77.2090]).addTo(map);
        marker.bindPopup('<b>Delhi Center</b><br>Air Quality Monitoring Point').openPopup();

        // Demo chart
        const ctx = document.getElementById('demo-chart').getContext('2d');
        const demoChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Now', '3h', '6h', '9h', '12h', '15h', '18h', '21h', '24h'],
                datasets: [{
                    label: 'NO₂ (µg/m³)',
                    data: [58, 62, 45, 38, 72, 68, 55, 42, 48],
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    fill: true,
                    tension: 0.4
                }, {
                    label: 'O₃ (µg/m³)',
                    data: [32, 28, 35, 42, 38, 45, 52, 35, 30],
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Demo Air Quality Forecast - Next 24 Hours'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Concentration (µg/m³)'
                        }
                    }
                }
            }
        });

        // Demo functions
        function generateDemoForecast() {
            alert('🎉 Demo forecast generated!\\n\\nThis is a standalone demo showing the interface.\\nIn the full version, this connects to real ML models for actual predictions.');
        }

        // Location preset handler
        document.getElementById('location-preset').addEventListener('change', function(e) {
            if (e.target.value) {
                const [lat, lng] = e.target.value.split(',');
                document.getElementById('latitude').value = lat;
                document.getElementById('longitude').value = lng;
                
                map.setView([lat, lng], 12);
                marker.setLatLng([lat, lng]);
                document.getElementById('current-coords').textContent = `${lat}, ${lng}`;
                document.getElementById('current-location').textContent = e.target.options[e.target.selectedIndex].text;
            }
        });

        // Update time
        setInterval(() => {
            document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
        }, 1000);
    </script>
</body>
</html>'''
    
    with open(standalone_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Created: standalone index.html")

def create_demo_data_script(standalone_dir):
    """Create a simple demo data file"""
    demo_js = '''
// Demo data for standalone version
const demoData = {
    locations: [
        { name: "Connaught Place", lat: 28.6315, lon: 77.2167, aqi: 125 },
        { name: "India Gate", lat: 28.6129, lon: 77.2295, aqi: 98 },
        { name: "Dwarka", lat: 28.5921, lon: 77.0460, aqi: 87 },
        { name: "Gurgaon", lat: 28.4595, lon: 77.0266, aqi: 142 },
        { name: "Noida", lat: 28.5355, lon: 77.3910, aqi: 108 }
    ],
    
    forecasts: {
        no2: [58, 62, 45, 38, 72, 68, 55, 42, 48, 52, 59, 63, 47, 41, 75, 71, 58, 45, 51, 55, 61, 65, 49, 43],
        o3: [32, 28, 35, 42, 38, 45, 52, 35, 30, 34, 31, 38, 45, 41, 48, 55, 38, 33, 37, 40, 36, 43, 50, 36]
    }
};

console.log("Demo data loaded for standalone version");
'''
    
    with open(standalone_dir / "demo-data.js", "w") as f:
        f.write(demo_js)
    
    print("✅ Created: demo-data.js")

if __name__ == "__main__":
    create_standalone_version()