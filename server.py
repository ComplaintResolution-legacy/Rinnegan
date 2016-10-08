import os
from Rinnegan import app

PORT = int(os.getenv('PORT', 8000))

if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=PORT
    )