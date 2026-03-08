#!/usr/bin/env python3
import base64
import json

# Read and encode the hero image
with open('/home/node/.openclaw/workspace/uk-energy-grants/hero.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

# Read the comprehensive grants data
with open('/home/node/.openclaw/workspace/fleet-downloads/uk-energy-grants-data.json', 'r') as f:
    grants_data = json.load(f)

# Convert Python data to JS format for embedding
grants_json = json.dumps(grants_data, indent=2)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UK Energy Grants Checker</title>
    <meta name="description" content="Find energy efficiency grants for your UK home. Check eligibility for GBIS, Boiler Upgrade Scheme, ECO4, and more.">
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div id="root"></div>
    
    <script type="text/babel">
        const {{ useState, useMemo }} = React;
        
        // Comprehensive grants data from scout's research
        const grantsDatabase = {grants_json};
        
        function App() {{
            const [formData, setFormData] = useState({{
                propertyType: '',
                epcRating: '',
                region: '',
                benefits: false,
                isOwner: true,
                offGasGrid: false,
                councilTaxBand: ''
            }});
            
            const [showResults, setShowResults] = useState(false);
            
            // Calculate eligible grants based on user input
            const eligibleGrants = useMemo(() => {{
                if (!showResults) return [];
                
                return grantsDatabase.grants.filter(grant => {{
                    // Check location eligibility
                    if (formData.region && !grant.eligibility.location.countries.includes(formData.region)) {{
                        return false;
                    }}
                    
                    // Check EPC rating if required
                    if (grant.eligibility.propertyType.epcRating && formData.epcRating) {{
                        if (!grant.eligibility.propertyType.epcRating.includes(formData.epcRating)) {{
                            return false;
                        }}
                    }}
                    
                    // Check income/benefits requirements
                    const hasIncomeMatch = grant.eligibility.income.some(req => {{
                        if (req.type === 'universal') return true;
                        if (req.type === 'benefit-based' && formData.benefits) return true;
                        if (req.type === 'general') return true; // Council tax band logic handled separately
                        if (req.type === 'eco4-flex') return formData.benefits; // Simplified
                        return false;
                    }});
                    
                    if (!hasIncomeMatch) return false;
                    
                    // Check property type (simplified - all property types accepted)
                    const propertyMatch = formData.propertyType && 
                        grant.eligibility.propertyType.eligible.some(type => 
                            type.toLowerCase().includes(formData.propertyType.toLowerCase())
                        );
                    
                    if (formData.propertyType && !propertyMatch) return false;
                    
                    // Check tenure/ownership
                    const ownershipMatch = grant.eligibility.tenure.eligible.some(t => 
                        (formData.isOwner && t === 'Owner-occupied') ||
                        (!formData.isOwner && (t.includes('rented') || t.includes('Social housing')))
                    );
                    
                    if (!ownershipMatch) return false;
                    
                    // Special checks for specific grants
                    if (grant.id === 'home-upgrade-grant' && !formData.offGasGrid) {{
                        return false;
                    }}
                    
                    return true;
                }});
            }}, [formData, showResults]);
            
            const handleSubmit = (e) => {{
                e.preventDefault();
                setShowResults(true);
            }};
            
            const resetForm = () => {{
                setFormData({{
                    propertyType: '',
                    epcRating: '',
                    region: '',
                    benefits: false,
                    isOwner: true,
                    offGasGrid: false,
                    councilTaxBand: ''
                }});
                setShowResults(false);
            }};
            
            return (
                React.createElement('div', {{ className: "min-h-screen" }},
                    // Hero section with embedded image
                    React.createElement('div', {{ className: "relative bg-gradient-to-br from-green-700 to-blue-700 text-white overflow-hidden" }},
                        React.createElement('div', {{ className: "absolute inset-0 opacity-30" }},
                            React.createElement('img', {{
                                src: "data:image/png;base64,{img_b64}",
                                alt: "UK Home with Solar Panels",
                                className: "w-full h-full object-cover"
                            }})
                        ),
                        React.createElement('div', {{ className: "relative max-w-6xl mx-auto px-4 py-20 text-center" }},
                            React.createElement('h1', {{ className: "text-4xl md:text-6xl font-bold mb-6" }},
                                "UK Energy Grants Checker"
                            ),
                            React.createElement('p', {{ className: "text-xl md:text-2xl opacity-95 max-w-3xl mx-auto" }},
                                "Find energy efficiency grants and schemes for your home. Save money, reduce bills, and help the environment."
                            ),
                            React.createElement('p', {{ className: "text-sm md:text-base opacity-80 mt-4" }},
                                `Last updated: ${{grantsDatabase.lastUpdated}}`
                            )
                        )
                    ),
                    
                    // Main content
                    React.createElement('div', {{ className: "max-w-6xl mx-auto px-4 py-12" }},
                        !showResults ? (
                            // Form
                            React.createElement('div', {{ className: "bg-white rounded-xl shadow-xl p-8 md:p-12" }},
                                React.createElement('h2', {{ className: "text-3xl font-bold text-gray-900 mb-8 text-center" }},
                                    "Check Your Eligibility"
                                ),
                                React.createElement('form', {{ onSubmit: handleSubmit, className: "space-y-6 max-w-2xl mx-auto" }},
                                    // Property Type
                                    React.createElement('div', null,
                                        React.createElement('label', {{ className: "block text-sm font-semibold text-gray-700 mb-2" }},
                                            "Property Type *"
                                        ),
                                        React.createElement('select', {{
                                            value: formData.propertyType,
                                            onChange: (e) => setFormData({{...formData, propertyType: e.target.value}}),
                                            className: "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-gray-900",
                                            required: true
                                        }},
                                            React.createElement('option', {{ value: "" }}, "Select property type"),
                                            React.createElement('option', {{ value: "house" }}, "House"),
                                            React.createElement('option', {{ value: "flat" }}, "Flat"),
                                            React.createElement('option', {{ value: "bungalow" }}, "Bungalow")
                                        )
                                    ),
                                    
                                    // EPC Rating
                                    React.createElement('div', null,
                                        React.createElement('label', {{ className: "block text-sm font-semibold text-gray-700 mb-2" }},
                                            "EPC Rating *"
                                        ),
                                        React.createElement('select', {{
                                            value: formData.epcRating,
                                            onChange: (e) => setFormData({{...formData, epcRating: e.target.value}}),
                                            className: "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-gray-900",
                                            required: true
                                        }},
                                            React.createElement('option', {{ value: "" }}, "Select EPC rating"),
                                            React.createElement('option', {{ value: "A" }}, "A (Most efficient)"),
                                            React.createElement('option', {{ value: "B" }}, "B"),
                                            React.createElement('option', {{ value: "C" }}, "C"),
                                            React.createElement('option', {{ value: "D" }}, "D"),
                                            React.createElement('option', {{ value: "E" }}, "E"),
                                            React.createElement('option', {{ value: "F" }}, "F"),
                                            React.createElement('option', {{ value: "G" }}, "G (Least efficient)")
                                        )
                                    ),
                                    
                                    // Region
                                    React.createElement('div', null,
                                        React.createElement('label', {{ className: "block text-sm font-semibold text-gray-700 mb-2" }},
                                            "Region *"
                                        ),
                                        React.createElement('select', {{
                                            value: formData.region,
                                            onChange: (e) => setFormData({{...formData, region: e.target.value}}),
                                            className: "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-gray-900",
                                            required: true
                                        }},
                                            React.createElement('option', {{ value: "" }}, "Select region"),
                                            React.createElement('option', {{ value: "England" }}, "England"),
                                            React.createElement('option', {{ value: "Scotland" }}, "Scotland"),
                                            React.createElement('option', {{ value: "Wales" }}, "Wales")
                                        )
                                    ),
                                    
                                    // Benefits
                                    React.createElement('div', {{ className: "bg-blue-50 p-4 rounded-lg" }},
                                        React.createElement('div', {{ className: "flex items-start" }},
                                            React.createElement('input', {{
                                                type: "checkbox",
                                                id: "benefits",
                                                checked: formData.benefits,
                                                onChange: (e) => setFormData({{...formData, benefits: e.target.checked}}),
                                                className: "w-5 h-5 text-green-600 focus:ring-green-500 border-gray-300 rounded mt-1"
                                            }}),
                                            React.createElement('label', {{ htmlFor: "benefits", className: "ml-3 text-sm text-gray-700" }},
                                                React.createElement('span', {{ className: "font-semibold" }}, "I receive qualifying benefits"),
                                                React.createElement('p', {{ className: "text-xs mt-1 text-gray-600" }},
                                                    "e.g., Universal Credit, Pension Credit, Child Benefit, Income Support, ESA, JSA"
                                                )
                                            )
                                        )
                                    ),
                                    
                                    // Ownership
                                    React.createElement('div', null,
                                        React.createElement('label', {{ className: "block text-sm font-semibold text-gray-700 mb-2" }},
                                            "Tenure *"
                                        ),
                                        React.createElement('select', {{
                                            value: formData.isOwner ? 'owner' : 'renter',
                                            onChange: (e) => setFormData({{...formData, isOwner: e.target.value === 'owner'}}),
                                            className: "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-gray-900",
                                            required: true
                                        }},
                                            React.createElement('option', {{ value: "owner" }}, "I own my home"),
                                            React.createElement('option', {{ value: "renter" }}, "I rent (private or social housing)")
                                        )
                                    ),
                                    
                                    // Off gas grid
                                    React.createElement('div', {{ className: "flex items-start" }},
                                        React.createElement('input', {{
                                            type: "checkbox",
                                            id: "offGasGrid",
                                            checked: formData.offGasGrid,
                                            onChange: (e) => setFormData({{...formData, offGasGrid: e.target.checked}}),
                                            className: "w-5 h-5 text-green-600 focus:ring-green-500 border-gray-300 rounded mt-1"
                                        }}),
                                        React.createElement('label', {{ htmlFor: "offGasGrid", className: "ml-3 text-sm text-gray-700" }},
                                            React.createElement('span', {{ className: "font-semibold" }}, "My property is off the gas grid"),
                                            React.createElement('p', {{ className: "text-xs mt-1 text-gray-600" }},
                                                "Heated by oil, LPG, electricity, or other non-mains gas"
                                            )
                                        )
                                    ),
                                    
                                    // Submit
                                    React.createElement('button', {{
                                        type: "submit",
                                        className: "w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-bold py-4 px-8 rounded-lg transition duration-200 shadow-lg text-lg"
                                    }},
                                        "Find My Grants"
                                    )
                                )
                            )
                        ) : (
                            // Results
                            React.createElement('div', null,
                                React.createElement('div', {{ className: "text-center mb-8" }},
                                    React.createElement('h2', {{ className: "text-3xl font-bold text-gray-900 mb-4" }},
                                        eligibleGrants.length > 0 
                                            ? `You're eligible for ${{eligibleGrants.length}} grant${{eligibleGrants.length === 1 ? '' : 's'}}!`
                                            : "No exact matches found"
                                    ),
                                    React.createElement('button', {{
                                        onClick: resetForm,
                                        className: "text-green-600 hover:text-green-700 font-semibold"
                                    }},
                                        "← Start over"
                                    )
                                ),
                                
                                eligibleGrants.length > 0 ? (
                                    React.createElement('div', {{ className: "space-y-6" }},
                                        eligibleGrants.map(grant => 
                                            React.createElement('div', {{ 
                                                key: grant.id, 
                                                className: "bg-white rounded-xl shadow-lg p-8 border-l-4 border-green-500 hover:shadow-xl transition-shadow"
                                            }},
                                                React.createElement('div', {{ className: "flex items-start justify-between mb-4" }},
                                                    React.createElement('div', null,
                                                        React.createElement('h3', {{ className: "text-2xl font-bold text-gray-900 mb-2" }}, grant.name),
                                                        React.createElement('p', {{ className: "text-gray-600 text-lg" }}, grant.shortDescription),
                                                        React.createElement('span', {{ 
                                                            className: grant.status.includes('Active') 
                                                                ? "inline-block mt-2 px-3 py-1 bg-green-100 text-green-800 text-sm font-semibold rounded-full"
                                                                : "inline-block mt-2 px-3 py-1 bg-yellow-100 text-yellow-800 text-sm font-semibold rounded-full"
                                                        }}, grant.status)
                                                    )
                                                ),
                                                
                                                grant.statusNote && React.createElement('div', {{ className: "bg-blue-50 p-4 rounded-lg mb-4" }},
                                                    React.createElement('p', {{ className: "text-sm text-blue-800" }}, grant.statusNote)
                                                ),
                                                
                                                React.createElement('div', {{ className: "bg-green-50 p-4 rounded-lg mb-6" }},
                                                    React.createElement('p', {{ className: "text-sm font-semibold text-gray-700 mb-1" }}, "Potential Savings:"),
                                                    React.createElement('p', {{ className: "text-2xl font-bold text-green-700" }}, grant.potentialSavings.annual),
                                                    React.createElement('p', {{ className: "text-xs text-gray-600 mt-1" }}, grant.potentialSavings.notes)
                                                ),
                                                
                                                React.createElement('div', {{ className: "mb-6" }},
                                                    React.createElement('h4', {{ className: "font-bold text-gray-900 mb-2" }}, "What's Covered:"),
                                                    React.createElement('div', {{ className: "flex flex-wrap gap-2" }},
                                                        grant.coverage.measures.slice(0, 6).map((measure, idx) =>
                                                            React.createElement('span', {{ 
                                                                key: idx,
                                                                className: "px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full"
                                                            }}, measure)
                                                        )
                                                    ),
                                                    grant.coverage.measures.length > 6 && 
                                                        React.createElement('p', {{ className: "text-sm text-gray-500 mt-2" }},
                                                            `+ ${{grant.coverage.measures.length - 6}} more measures`
                                                        )
                                                ),
                                                
                                                React.createElement('div', {{ className: "mb-6" }},
                                                    React.createElement('h4', {{ className: "font-bold text-gray-900 mb-2" }}, "How to Apply:"),
                                                    React.createElement('p', {{ className: "text-gray-700 mb-3" }}, grant.applicationProcess.howToApply),
                                                    React.createElement('ol', {{ className: "list-decimal list-inside space-y-1 text-sm text-gray-600" }},
                                                        grant.applicationProcess.steps.slice(0, 3).map((step, idx) =>
                                                            React.createElement('li', {{ key: idx }}, step)
                                                        )
                                                    )
                                                ),
                                                
                                                React.createElement('div', {{ className: "border-t pt-4" }},
                                                    React.createElement('h4', {{ className: "font-bold text-gray-900 mb-2" }}, "Official Resources:"),
                                                    React.createElement('div', {{ className: "space-y-2" }},
                                                        grant.applicationProcess.officialLinks.map((link, idx) =>
                                                            React.createElement('a', {{ 
                                                                key: idx,
                                                                href: link.url,
                                                                target: "_blank",
                                                                rel: "noopener noreferrer",
                                                                className: "block text-blue-600 hover:text-blue-800 text-sm underline"
                                                            }}, `→ ${{link.title}}`)
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                ) : (
                                    React.createElement('div', {{ className: "bg-yellow-50 border-l-4 border-yellow-400 p-8 rounded-lg" }},
                                        React.createElement('h3', {{ className: "text-xl font-bold text-yellow-800 mb-4" }},
                                            "No exact matches, but don't give up!"
                                        ),
                                        React.createElement('p', {{ className: "text-yellow-800 mb-4" }},
                                            "Grant eligibility can be complex. You may still qualify through:"
                                        ),
                                        React.createElement('ul', {{ className: "list-disc list-inside space-y-2 text-yellow-800 mb-6" }},
                                            React.createElement('li', null, "Local authority ECO4 Flex schemes (extended income criteria)"),
                                            React.createElement('li', null, "Energy supplier direct schemes"),
                                            React.createElement('li', null, "Council-specific programs"),
                                            React.createElement('li', null, "Changing circumstances (e.g., EPC improvements)")
                                        ),
                                        React.createElement('div', {{ className: "bg-white p-4 rounded-lg mt-4" }},
                                            React.createElement('h4', {{ className: "font-bold mb-2" }}, "Next Steps:"),
                                            grantsDatabase.generalResources.map((resource, idx) =>
                                                React.createElement('a', {{ 
                                                    key: idx,
                                                    href: resource.url,
                                                    target: "_blank",
                                                    rel: "noopener noreferrer",
                                                    className: "block text-blue-600 hover:text-blue-800 text-sm underline mb-2"
                                                }}, `→ ${{resource.title}}`)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    
                    // Footer
                    React.createElement('footer', {{ className: "bg-gray-800 text-white py-12 mt-20" }},
                        React.createElement('div', {{ className: "max-w-6xl mx-auto px-4" }},
                            React.createElement('div', {{ className: "text-center mb-8" }},
                                React.createElement('h3', {{ className: "text-2xl font-bold mb-4" }}, "Important Disclaimer"),
                                React.createElement('p', {{ className: "text-gray-300 max-w-3xl mx-auto" }},
                                    "This tool provides general guidance based on publicly available information. Eligibility criteria can change, and final eligibility must be confirmed by the grant administrators. Always check official government sources and consult with accredited energy advisors for personalized advice."
                                )
                            ),
                            React.createElement('div', {{ className: "text-center border-t border-gray-700 pt-8" }},
                                React.createElement('p', {{ className: "text-sm text-gray-400" }},
                                    `Data last updated: ${{grantsDatabase.lastUpdated}} | Built with AI assistance`
                                ),
                                React.createElement('div', {{ className: "mt-4 space-x-4" }},
                                    grantsDatabase.generalResources.slice(0, 3).map((resource, idx) =>
                                        React.createElement('a', {{ 
                                            key: idx,
                                            href: resource.url,
                                            target: "_blank",
                                            rel: "noopener noreferrer",
                                            className: "text-green-400 hover:text-green-300 text-sm"
                                        }}, resource.title)
                                    )
                                )
                            )
                        )
                    )
                )
            );
        }}
        
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(React.createElement(App));
    </script>
</body>
</html>"""

# Write the generated HTML
with open('/home/node/.openclaw/workspace/uk-energy-grants/index.html', 'w') as f:
    f.write(html)

print("✓ Built index.html with embedded hero image and comprehensive grants data")
print(f"  - Hero image: {len(img_b64)} bytes (base64)")
print(f"  - Grants data: {len(grants_data['grants'])} programs")
print(f"  - Last updated: {grants_data['lastUpdated']}")
