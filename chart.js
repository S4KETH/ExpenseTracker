document.addEventListener('DOMContentLoaded', () => {
  const el = document.getElementById('expenseChart');
  const raw = el.dataset.expenses;
  const expenses = JSON.parse(raw);
  const totals = {};
  expenses.forEach(e => {
    totals[e.category] = (totals[e.category] || 0) + parseFloat(e.amount);
  });
  new Chart(el, {
    type: 'pie',
    data: {
      labels: Object.keys(totals),
      datasets: [{ data: Object.values(totals), backgroundColor: [
        '#6366F1','#3B82F6','#10B981','#F59E0B','#EF4444','#8B5CF6'
      ] }]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'bottom' } }
    }
  });
});
