// Automatically check and insert official tenders on page load
window.addEventListener('DOMContentLoaded', () => {
    syncOfficialTenders();
});

async function syncOfficialTenders() {
    // Official BHEL tender items to track
    const officialTenders = [
        {
            "bid_number": "GEM/2026/B/8274636",
            "title": "W97311422302 DRG: 21142211054 REV - BHEL Haridwar",
            "bhel_unit": "BHEL Haridwar",
            "end_date": "2026-05-15T18:00:00Z"
        }
    ];

    try {
        for (let tender of officialTenders) {
            // Check if tender already exists in your Supabase table
            const { data: existing, error: fetchError } = await window.supabaseClient
                .from('bhel_bids')
                .select('id')
                .eq('bid_number', tender.bid_number);

            if (fetchError) {
                console.error("Error checking existing bid:", fetchError.message);
                continue;
            }

            // If it doesn't exist, insert it
            if (existing && existing.length === 0) {
                const { error: insertError } = await window.supabaseClient
                    .from('bhel_bids')
                    .insert([tender]);

                if (insertError) {
                    console.error("Insert error:", insertError.message);
                } else {
                    console.log("Successfully synced tender:", tender.bid_number);
                }
            }
        }

        // Refresh your website UI list if function exists
        if (typeof loadBids === 'function') {
            loadBids();
        }
    } catch (err) {
        console.error("Sync process failed:", err);
    }
}
