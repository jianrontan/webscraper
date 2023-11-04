fetch('/get_graph_data')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const groupedData = data.reduce((acc, tuple) => {
            const datetime = new Date(tuple[2]);
            datetime.setSeconds(0, 0)
            const price = tuple[1];
            const dateString = datetime.toISOString();

            if (!acc[dateString]) {
                acc[dateString] = [];
            }

            acc[dateString].push(price);

            return acc;
        }, {});

        const timeData = [];
        const priceData = [];

        for (const datetime in groupedData) {
            const prices = groupedData[datetime];
            const averagePrice = prices.reduce((a, b) => a + b, 0) / prices.length;

            timeData.push(new Date(datetime));
            priceData.push(averagePrice);
        }

        const ctx = document.getElementById('lineGraph').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: timeData,
                datasets: [{
                    label: 'Average Price',
                    data: priceData,
                    borderColor: 'black',
                    fill: true
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day'
                        },
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Price'
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error: ', error));