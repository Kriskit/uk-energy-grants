#!/usr/bin/env python3
import base64

# Read and encode the hero image
with open('/home/node/.openclaw/workspace/hero-small.jpg', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UK Energy Grants Checker</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div id="root"></div>
    
    <script type="text/babel">
        const {{ useState }} = React;
        
        const grantsData = [
            {{
                id: 'gbis',
                name: 'Great British Insulation Scheme (GBIS)',
                description: 'Cavity, loft, and solid wall insulation',
                savings: '£200-600/yr',
                criteria: {{
                    epc: ['D', 'E'],
                    benefits: true,
                    regions: ['England', 'Scotland', 'Wales']
                }},
                details: 'Available for households with EPC D-E rating who receive benefits or live in low council tax bands.'
            }},
            {{
                id: 'boiler',
                name: 'Boiler Upgrade Scheme',
                description: 'Heat pump installation grants',
                savings: '£5,000-7,500 voucher',
                criteria: {{
                    epc: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    regions: ['England', 'Wales']
                }},
                details: 'Vouchers for air source heat pumps (£7,500) or ground source heat pumps (£7,500). Valid EPC required.'
            }},
            {{
                id: 'eco4',
                name: 'ECO4',
                description: 'Insulation and heating upgrades',
                savings: '£300-1,000/yr',
                criteria: {{
                    epc: ['D', 'E', 'F', 'G'],
                    benefits: true,
                    regions: ['England', 'Scotland', 'Wales']
                }},
                details: 'Free or subsidized insulation and heating for low-income households receiving eligible benefits.'
            }},
            {{
                id: 'hug',
                name: 'Home Upgrade Grant',
                description: 'Off-gas property upgrades',
                savings: '£10,000-25,000 grant',
                criteria: {{
                    epc: ['D', 'E', 'F', 'G'],
                    regions: ['England']
                }},
                details: 'For off-gas properties with household income under £36,000. Covers insulation and low-carbon heating.'
            }},
            {{
                id: 'solar',
                name: 'Solar Together',
                description: 'Group-buying solar PV scheme',
                savings: '£300-500/yr',
                criteria: {{
                    epc: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    regions: ['Selected regions']
                }},
                details: 'Group-buying scheme for solar panels. Available in selected council areas. Check your local authority.'
            }}
        ];
        
        function App() {{
            const [formData, setFormData] = useState({{
                propertyType: 'house',
                epc: '',
                region: '',
                benefits: false
            }});
            
            const [results, setResults] = useState(null);
            
            const handleSubmit = (e) => {{
                e.preventDefault();
                
                const eligible = grantsData.filter(grant => {{
                    // Check EPC rating
                    if (formData.epc && !grant.criteria.epc.includes(formData.epc)) {{
                        return false;
                    }}
                    
                    // Check region
                    if (formData.region && grant.criteria.regions) {{
                        if (!grant.criteria.regions.includes(formData.region) && 
                            !grant.criteria.regions.includes('Selected regions')) {{
                            return false;
                        }}
                    }}
                    
                    // Check benefits requirement
                    if (grant.criteria.benefits && !formData.benefits) {{
                        return false;
                    }}
                    
                    return true;
                }});
                
                setResults(eligible);
            }};
            
            return (
                React.createElement('div', {{ className: "min-h-screen" }},
                    React.createElement('div', {{ className: "relative bg-gradient-to-br from-green-600 to-blue-600 text-white overflow-hidden" }},
                        React.createElement('div', {{ className: "absolute inset-0 opacity-20" }},
                            React.createElement('img', {{
                                src: "data:image/jpeg;base64,{img_b64}",
                                alt: "UK Home",
                                className: "w-full h-full object-cover"
                            }})
                        ),
                        React.createElement('div', {{ className: "relative max-w-4xl mx-auto px-4 py-16 text-center" }},
                            React.createElement('h1', {{ className: "text-4xl md:text-5xl font-bold mb-4" }},
                                "UK Energy Grants Checker"
                            ),
                            React.createElement('p', {{ className: "text-xl md:text-2xl opacity-90" }},
                                "Find out which energy grants you're eligible for"
                            )
                        )
                    ),
                    React.createElement('div', {{ className: "max-w-4xl mx-auto px-4 py-12" }},
                        React.createElement('div', {{ className: "bg-white rounded-lg shadow-lg p-8" }},
                            React.createElement('form', {{ onSubmit: handleSubmit, className: "space-y-6" }},
                                React.createElement('div', null,
                                    React.createElement('label', {{ className: "block text-sm font-medium text-gray-700 mb-2" }},
                                        "Property Type"
                                    ),
                                    React.createElement('select', {{
                                        value: formData.propertyType,
                                        onChange: (e) => setFormData({{...formData, propertyType: e.target.value}}),
                                        className: "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent",
                                        required: true
                                    }},
                                        React.createElement('option', {{ value: "house" }}, "House"),
                                        React.createElement('option', {{ value: "flat" }}, "Flat"),
                                        React.createElement('option', {{ value: "bungalow" }}, "Bungalow")
                                    )
                                ),
                                React.createElement('div', null,
                                    React.createElement('label', {{ className: "block text-sm font-medium text-gray-700 mb-2" }},
                                        "EPC Rating"
                                    ),
                                    React.createElement('select', {{
                                        value: formData.epc,
                                        onChange: (e) => setFormData({{...formData, epc: e.target.value}}),
                                        className: "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent",
                                        required: true
                                    }},
                                        React.createElement('option', {{ value: "" }}, "Select EPC Rating"),
                                        React.createElement('option', {{ value: "A" }}, "A (Most efficient)"),
                                        React.createElement('option', {{ value: "B" }}, "B"),
                                        React.createElement('option', {{ value: "C" }}, "C"),
                                        React.createElement('option', {{ value: "D" }}, "D"),
                                        React.createElement('option', {{ value: "E" }}, "E"),
                                        React.createElement('option', {{ value: "F" }}, "F"),
                                        React.createElement('option', {{ value: "G" }}, "G (Least efficient)")
                                    )
                                ),
                                React.createElement('div', null,
                                    React.createElement('label', {{ className: "block text-sm font-medium text-gray-700 mb-2" }},
                                        "Region"
                                    ),
                                    React.createElement('select', {{
                                        value: formData.region,
                                        onChange: (e) => setFormData({{...formData, region: e.target.value}}),
                                        className: "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent",
                                        required: true
                                    }},
                                        React.createElement('option', {{ value: "" }}, "Select Region"),
                                        React.createElement('option', {{ value: "England" }}, "England"),
                                        React.createElement('option', {{ value: "Scotland" }}, "Scotland"),
                                        React.createElement('option', {{ value: "Wales" }}, "Wales"),
                                        React.createElement('option', {{ value: "Northern Ireland" }}, "Northern Ireland")
                                    )
                                ),
                                React.createElement('div', {{ className: "flex items-center" }},
                                    React.createElement('input', {{
                                        type: "checkbox",
                                        id: "benefits",
                                        checked: formData.benefits,
                                        onChange: (e) => setFormData({{...formData, benefits: e.target.checked}}),
                                        className: "w-4 h-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                                    }}),
                                    React.createElement('label', {{ htmlFor: "benefits", className: "ml-2 text-sm text-gray-700" }},
                                        "I receive eligible benefits (e.g., Universal Credit, Pension Credit)"
                                    )
                                ),
                                React.createElement('button', {{
                                    type: "submit",
                                    className: "w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200"
                                }},
                                    "Check Eligibility"
                                )
                            )
                        ),
                        results !== null && React.createElement('div', {{ className: "mt-8" }},
                            React.createElement('h2', {{ className: "text-2xl font-bold mb-4" }}, "Your Eligible Grants"),
                            results.length > 0 ? 
                                React.createElement('div', {{ className: "space-y-4" }},
                                    results.map(grant => 
                                        React.createElement('div', {{ key: grant.id, className: "bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500" }},
                                            React.createElement('h3', {{ className: "text-xl font-semibold text-gray-900 mb-2" }}, grant.name),
                                            React.createElement('p', {{ className: "text-gray-600 mb-2" }}, grant.description),
                                            React.createElement('p', {{ className: "text-green-600 font-semibold mb-3" }}, 
                                                "Potential Savings: " + grant.savings
                                            ),
                                            React.createElement('p', {{ className: "text-sm text-gray-500" }}, grant.details)
                                        )
                                    )
                                ) :
                                React.createElement('div', {{ className: "bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg" }},
                                    React.createElement('p', {{ className: "text-yellow-800" }},
                                        "Based on your criteria, you may not be eligible for these grants. However, eligibility criteria can be complex - we recommend contacting your local authority or an energy advisor for personalized advice."
                                    )
                                )
                        )
                    ),
                    React.createElement('footer', {{ className: "bg-gray-800 text-white py-8 mt-16" }},
                        React.createElement('div', {{ className: "max-w-4xl mx-auto px-4 text-center" }},
                            React.createElement('p', {{ className: "text-sm opacity-75" }},
                                "This tool provides general guidance only. For official eligibility confirmation, please contact the grant administrators or consult with an accredited energy advisor."
                            )
                        )
                    )
                )
            );
        }}
        
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>"""

# Write the generated HTML
with open('/home/node/.openclaw/workspace/uk-energy-grants/index.html', 'w') as f:
    f.write(html)

print("✓ Built index.html with embedded hero image")
