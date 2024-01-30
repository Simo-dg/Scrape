fetch('/price-trend', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
})
.then(response => response.json())
.then(data => {
    if (Array.isArray(data.result)) {  // Verifica se data è un array
        let ctx = canvas.getContext('2d');
        let chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.result.map(item => item.date),
                datasets: [{
                    label: 'Price',
                    data: data.result.map(item => item.price),
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            parser: 'YYYY-MM-DD'
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Price'
                        }
                    }
                }
            }
        });
    } else {
        console.error('Data is not an array:', data.result);
    }
})