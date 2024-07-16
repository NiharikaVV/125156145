from flask import Flask, jsonify
import requests
import logging

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
NUMBERS_API_URLS = {
    'p': "http://20.244.56.144/test/primes",
    'f': "http://20.244.56.144/test/fibo",
    'e': "http://20.244.56.144/test/even",
    'r': "http://20.244.56.144/test/rand"
}
QUALIFIED_IDS = ['p', 'f', 'e', 'r']
stored_numbers = []

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Fetch numbers from third-party server with timeout handling
def fetch_numbers(number_id):
    url = NUMBERS_API_URLS[number_id]
    logging.debug(f"Fetching numbers from {url}")
    try:
        response = requests.get(url, timeout=0.5)
        logging.debug(f"Received response: {response.status_code} - {response.text}")
        if response.status_code == 200:
            return response.json().get('numbers', [])
    except requests.RequestException as e:
        logging.error(f"Error fetching numbers: {e}")
    return []

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in QUALIFIED_IDS:
        return jsonify({"error": "Invalid number ID"}), 400

    global stored_numbers
    prev_state = list(stored_numbers)

    new_numbers = fetch_numbers(number_id)
    for number in new_numbers:
        if number not in stored_numbers:
            stored_numbers.append(number)
            if len(stored_numbers) > WINDOW_SIZE:
                stored_numbers.pop(0)

    curr_state = list(stored_numbers)
    avg = sum(stored_numbers) / len(stored_numbers) if stored_numbers else 0.0

    return jsonify({
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": new_numbers,
        "avg": round(avg, 3)
    })

if __name__ == '__main__':
    app.run(port=9876)
