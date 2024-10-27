from app import app
from flask_wtf import CSRFProtect

csrf = CSRFProtect(app)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)