// Import Supabase CDN helper or initialize directly
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';

const SUPABASE_URL = "https://rppgxoqqvyzmiewzkpxa.supabase.co";
const SUPABASE_KEY = "sb_publishable_WjccgngW8-r7gilAJR3YCg_R5STrIZT";

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

window.addEventListener('DOMContentLoaded', () => {
    syncAndLoadBids();
});

async function syncAndLoadBids() {
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
        // 1. Auto-sync missing tenders
        for (let tender of liveTenders) {
            const { data: existing } = await supabase
                .from('bhel_bids')
                .select('id')
                .eq('bid_number', tender.bid_number);

            if (existing && existing.length === 0) {
                await supabase.from('bhel_bids').insert([tender]);
            }
        }

        // 2. Fetch all bids from Supabase to render
        const { data: bids, error } = await supabase
            .from('bhel_bids')
            .select('*')
            .order('created_at', { ascending: false });

        if (error) {
            console.error("Error fetching bids:", error.message);
            return;
        }

        renderBids(bids);

    } catch (err) {
        console.error("Sync/Load failed:", err);
    }
}

function renderBids(bids) {
    const container = document.getElementById('bids-container');
    if (!container) return;

    container.innerHTML = '';

    if (!bids || bids.length === 0) {
        container.innerHTML = '<p style="padding: 20px; text-align: center; color: #666;">No active BHEL tenders found.</p>';
        return;
    }

    bids.forEach(bid => {
        const card = document.createElement('div');
        card.style.cssText = 'background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; margin: 12px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);';
        
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
}
