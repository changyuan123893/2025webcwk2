
from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("FilmHub Web Application")
    print("Starting the server...")
    print("=" * 50)
    print("Access address: http://127.0.0.1:5000")
    print("Test account: testuser / password123")
    print("press Ctrl+C Stop the server")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)
