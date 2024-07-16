const windowSize = 10;
let windowNumbers = [];

document.getElementById('fetchButton').addEventListener('click', async function() {
    const numberType = document.getElementById('numberType').value;
    const apiUrlMap = {
        'p': 'http://20.244.56.144/test/primes',
        'f': 'http://20.244.56.144/test/fibo',
        'e': 'http://20.244.56.144/test/even',
        'r': 'http://20.244.56.144/test/rand'
    };

    const url = apiUrlMap[numberType];
    const responseElement = document.getElementById('response');

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('API Response:', data);

        if (!Array.isArray(data.numbers)) {
            throw new Error('Invalid data format received from API');
        }

        const newNumbers = data.numbers;

        const prevWindow = [...windowNumbers];
        
        for (const num of newNumbers) {
            if (!windowNumbers.includes(num)) {
                if (windowNumbers.length >= windowSize) {
                    windowNumbers.shift();
                }
                windowNumbers.push(num);
            }
        }

        const avg = windowNumbers.length > 0 
            ? windowNumbers.reduce((acc, val) => acc + val, 0) / windowNumbers.length 
            : 0;

        const result = {
            windowPrevState: prevWindow,
            windowCurrState: windowNumbers,
            numbers: newNumbers,
            avg: avg.toFixed(2)
        };

        responseElement.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        console.error('Error:', error);
        responseElement.textContent = 'Error: ' + error.message;
    }
});
