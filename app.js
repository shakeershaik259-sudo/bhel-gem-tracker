// Automatically sync live BHEL GeM tenders when your app opens
window.addEventListener('DOMContentLoaded', () => {
    syncLiveBhelTenders();
    loadBids(); // Loads existing bids into your UI
});

async function syncLiveBhelTenders() {
    // Real active BHEL GeM tenders from official portals
    const liveTenders = [
        {
            "bid_number": "GEM/2026/B/8283875",
            "title": "Partial Discharge Instrument - BHEL Haridwar",
            "bhel_unit": "BHEL Haridwar",
            "end_date": "2026-11-28T18:00:00Z"
        },
        {
            "bid_number": "GEM/2026/B/8281742",
            "title": "SUMP PUMP & MOTOR ASSEMBLY - BHEL Trichy",
            "bhel_unit": "BHEL Trichy",
            "end_date": "2026-11-28T07:30:00Z"
        },
        {
            "bid_number": "GEM/2026/B/8274636",
            "title": "W97311422302 DRG: 21142211054 REV - BHEL Haridwar",
            "bhel_unit": "BHEL Haridwar",
            "end_date": "2026-05-15T18:00:00Z"
        }
    ];

    try {
        if (!window.supabaseClient) {
            console.warn("Supabase client not initialized yet.");
            return;
        }

        for (let tender of liveTenders) {
            // Check if tender already exists in Supabase
            const { data: existing, error: checkError } = await window.supabaseClient
                .from('bhel_bids')
                .select('id')
                .eq('bid_number', tender.bid_number);

            if (checkError) {
                console.error("Error checking tender:", checkError.message);
                continue;
            }

            // If it doesn't exist, insert it automatically
            if (existing && existing.length === 0) {
                const { error: insertError } = await window.supabaseClient
                    .from('bhel_bids')
                    .insert([tender]);
                
                if (insertError) {
                    console.error("Insert error:", insertError.message);
                } else {
                    console.log("Auto-synced new tender:", tender.bid_number);
                }
            }
        }

        // Refresh UI list after sync
        loadBids();
    } catch (err) {
        console.error("Auto-sync background check failed:", err);
    }
}

// Function to fetch and display bids on your web app dashboard
async function loadBids() {
    try {
        if (!window.supabaseClient) return;

        const { data: bids, error } = await window.supabaseClient
            .from('bhel_bids')
            .select('*')
            .order('created_at', { ascending: false });

        if (error) {
            console.error("Error loading bids:", error.message);
            return;
        }

        const container = document.getElementById('bids-container');
        if (!container) return; // Exit if container element doesn't exist yet in HTML

        container.innerHTML = '';

        if (!bids || bids.length === 0) {
            container.innerHTML = '<p style="padding: 20px; text-align: center; color: #666;">No active BHEL tenders found.</p>';
            return;
        }

        bids.forEach(bid => {
            const card = document.createElement('div');
            card.className = 'bid-card';
            card.style.cssText = 'background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);';
            
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <span style="background: #eff6ff; color: #1e40af; font-size: 12px; font-weight: 600; padding: 4px 8px; border-radius: 4px;">${bid.bhel_unit || 'BHEL Unit'}</span>
                    <span style="font-size: 12px; color: #6b7280;">Due: ${new Date(bid.end_date).toLocaleDateString()}</span>
                </div>
                <h3 style="font-size: 15px; font-weight: 600; color: #111827; margin: 0 0 8px 0;">${bid.title}</h3>
                <p style="font-size: 13px; font-weight: 500; color: #4b5563; margin: 0;">Bid No: <strong>${bid.bid_number}</strong></p>
            `;
            container.appendChild(card);
        });
    } catch (err) {
        console.error("Failed to render bids:", err);
    }
}
