function calculateTotals() {
    let totalKcal = 0;
    let totalCost = 0;

    document.querySelectorAll('.kcal-per-day').forEach(el => {
        const val = parseFloat(el.textContent);
        if (!isNaN(val)) totalKcal += val;
    });

    document.querySelectorAll('.cost-per-day').forEach(el => {
        const val = parseFloat(el.textContent);
        if (!isNaN(val)) totalCost += val;
    });

    document.getElementById('total-kcal').textContent = totalKcal.toFixed(2) + ' kcal';
    document.getElementById('total-cost').textContent = totalCost.toFixed(2) + ' ' + userCurrency;
}

// Run on page load
document.addEventListener('DOMContentLoaded', calculateTotals);

// Run after any HTMX swap (so totals update dynamically)
document.body.addEventListener('htmx:afterRequest', (evt) => {
    // You can check evt.detail.target if needed
    calculateTotals();
});
