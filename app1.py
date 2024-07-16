from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

base_url = 'http://20.244.56.144/test/'

# Example token, replace with your actual authorization token if needed
authorization_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIxMTM1NzYwLCJpYXQiOjE3MjExMzU0NjAsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjZjODYxNTIwLWYxOGMtNDhmZi1iOGJlLTMzZTUwNjE2YmYyYSIsInN1YiI6IjEyNTE1NjE0NUBzYXN0cmEuYWMuaW4ifSwiY29tcGFueU5hbWUiOiJTYXN0cmEiLCJjbGllbnRJRCI6IjZjODYxNTIwLWYxOGMtNDhmZi1iOGJlLTMzZTUwNjE2YmYyYSIsImNsaWVudFNlY3JldCI6InpzdG9pc2x3blBPSVl5dlkiLCJvd25lck5hbWUiOiJWZW5rYW1zZXR0eSBWZW5rYXRhIE5paGFyaWthIiwib3duZXJFbWFpbCI6IjEyNTE1NjE0NUBzYXN0cmEuYWMuaW4iLCJyb2xsTm8iOiIxMjUxNTYxNDUifQ.1v1rMTfldPlsUFejPQ10_uK54HFrk3veXaGpbYsgllk'

@app.route('/numbers/<numberid>', methods=['POST'])
def calculate_average(numberid):
    window_size = 10
    window_numbers = []

    api_endpoints = {
        'p': 'primes',
        'f': 'fibo',
        'e': 'even',
        'r': 'rand'
    }

    if numberid not in api_endpoints:
        return jsonify({'error': 'Invalid number ID'}), 400

    api_url = base_url + api_endpoints[numberid]
    headers = {
        'Authorization': authorization_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if 'numbers' not in data:
            return jsonify({'error': 'Invalid data format from external API'}), 500

        new_numbers = data['numbers']

        prev_window = []
        avg = 0.0

        for num in new_numbers:
            if num not in window_numbers:
                if len(window_numbers) >= window_size:
                    window_numbers.pop(0)
                window_numbers.append(num)

        prev_window = window_numbers.copy()

        if window_numbers:
            avg = sum(window_numbers) / len(window_numbers)

        response_data = {
            'windowPrevState': prev_window,
            'windowCurrState': window_numbers,
            'numbers': new_numbers,
            'avg': avg
        }

        return jsonify(response_data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__== '_main_':
    app.run(debug=True)