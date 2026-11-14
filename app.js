// Initialize Supabase Client with your real credentials
const SUPABASE_URL = 'https://rppgxoqqvyzmiewzkpxa.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_WjccgngW8-r7gilAJR3YCg_R5STrIZT';

const _supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function fetchBids() {
    const bidListEl = document.getElementById('bidList');
    const bidCountEl = document.getElementById('bidCount');

    bidListEl.innerHTML = `<div class="text-center py-6 text-slate-400 text-sm">Fetching live BHEL tenders from cloud...</div>`;

    // Query data from your Supabase table
    let { data: bids, error } = await _supabase
        .from('bhel_bids')
        .select('*')
        .order('end_date', { ascending: true });

    if (error) {
        bidListEl.innerHTML = `<div class="text-center text-red-500 text-sm py-4">Failed to load live data. Check credentials.</div>`;
        console.error('Supabase Error:', error);
        return;
    }

    bidCountEl.textContent = `${bids.length} Active Bids Found`;
    renderBids(bids);
}

function renderBids(bids) {
    const bidListEl = document.getElementById('bidList');
    if (!bids || bids.length === 0) {
        bidListEl.innerHTML = `<p class="text-center text-slate-400 text-sm py-6">No matching BHEL bids found.</p>`;
        return;
    }

    bidListEl.innerHTML = bids.map(bid => `
        <div class="card space-y-2">
            <div class="flex justify-between items-start">
                <span class="text-xs font-semibold bg-blue-50 text-blue-700 px-2 py-0.5 rounded">${bid.bhel_unit || 'BHEL Unit'}</span>
                <span class="text-xs text-red-600 font-medium">Ends: ${bid.end_date ? new Date(bid.end_date).toLocaleDateString() : 'N/A'}</span>
            </div>
            <h2 class="text-sm font-bold text-slate-800">${bid.bid_number}</h2>
            <p class="text-xs text-slate-600">${bid.title}</p>
            <div class="pt-2 flex justify-end">
                <a href="https://gem.gov.in" target="_blank" class="text-xs bg-blue-600 text-white px-3 py-1 rounded-lg font-medium inline-block">View on GeM</a>
            </div>
        </div>
    `).join('');
}

// Client-side search filtering
document.getElementById('searchInput').addEventListener('input', async (e) => {
    const query = e.target.value.toLowerCase();
    
    let { data: bids, error } = await _supabase
        .from('bhel_bids')
        .select('*')
        .or(`bid_number.ilike.%${query}%,title.ilike.%${query}%,bhel_unit.ilike.%${query}%`)
        .order('end_date', { ascending: true });

    if (!error) {
        document.getElementById('bidCount').textContent = `${bids.length} Active Bids Found`;
        renderBids(bids);
    }
});

// Run on load
fetchBids();
