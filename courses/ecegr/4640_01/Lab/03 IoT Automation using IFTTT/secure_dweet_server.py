# my personal configuration of lab 03 dweet_led.py file
from flask import Flask, request, jsonify, abort
from datetime import datetime
import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory storage for dweets
dweets = {}

# Simple security - allowed thing names
ALLOWED_THINGS = ['2406874e']  # Only your thing name

# Rate limiting - simple in-memory counter
request_counts = {}

def is_allowed_thing(thing_name):
    """Check if thing name is allowed"""
    return thing_name in ALLOWED_THINGS

def rate_limit_check(client_ip):
    """Simple rate limiting"""
    current_time = datetime.now().timestamp()
    
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    
    # Remove requests older than 1 minute
    request_counts[client_ip] = [
        ts for ts in request_counts[client_ip] 
        if current_time - ts < 60
    ]
    
    # Check if too many requests (max 30 per minute)
    if len(request_counts[client_ip]) >= 30:
        return False
    
    request_counts[client_ip].append(current_time)
    return True

@app.before_request
def security_check():
    """Basic security checks"""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ['REMOTE_ADDR'])
    
    # Rate limiting
    if not rate_limit_check(client_ip):
        logger.warning(f"Rate limit exceeded for {client_ip}")
        abort(429)  # Too Many Requests

@app.route('/')
def home():
    return jsonify({
        "this": "succeeded",
        "message": "Raspberry Pi Dweet Server - External Access",
        "endpoints": {
            "send_dweet": "/dweet/for/{thing_name}?param=value",
            "get_latest": "/get/latest/dweet/for/{thing_name}",
        },
        "security": "Rate limited, filtered thing names"
    })

@app.route('/dweet/for/<thing_name>')
def send_dweet(thing_name):
    """Send a dweet (with security)"""
    try:
        # Security check
        if not is_allowed_thing(thing_name):
            logger.warning(f"Unauthorized thing name attempted: {thing_name}")
            abort(403)
        
        # Get all query parameters as the dweet content
        content = dict(request.args)
        
        # Convert single-item lists to strings
        for key, value in content.items():
            if isinstance(value, list) and len(value) == 1:
                content[key] = value[0]
        
        # Create dweet entry
        dweet_entry = {
            "thing": thing_name,
            "created": datetime.utcnow().isoformat() + "Z",
            "content": content
        }
        
        # Store the dweet
        dweets[thing_name] = dweet_entry
        
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ['REMOTE_ADDR'])
        logger.info(f"Dweet from {client_ip} for {thing_name}: {content}")
        
        # Return dweet.io compatible response
        return jsonify({
            "this": "succeeded",
            "by": "dweeting",
            "the": "dweet",
            "with": [dweet_entry]
        })
        
    except Exception as e:
        logger.error(f"Error processing dweet: {e}")
        return jsonify({
            "this": "failed",
            "by": "exception", 
            "because": str(e)
        }), 500

@app.route('/get/latest/dweet/for/<thing_name>')
def get_latest_dweet(thing_name):
    """Get the latest dweet for a thing"""
    try:
        # Security check
        if not is_allowed_thing(thing_name):
            abort(403)
            
        if thing_name in dweets:
            dweet_entry = dweets[thing_name]
            logger.info(f"Latest dweet requested for {thing_name}")
            
            return jsonify({
                "this": "succeeded",
                "by": "getting",
                "the": "dweets",
                "with": [dweet_entry]
            })
        else:
            return jsonify({
                "this": "succeeded", 
                "by": "getting",
                "the": "dweets",
                "with": []
            })
            
    except Exception as e:
        logger.error(f"Error getting dweet: {e}")
        return jsonify({
            "this": "failed",
            "by": "exception",
            "because": str(e)
        }), 500

if __name__ == '__main__':
    print("🌐 Starting Secure Dweet Server for External Access...")
    print("🔒 Security Features:")
    print("   - Rate limiting (30 req/min per IP)")
    print("   - Thing name filtering")
    print("   - Request logging")
    print("\n📡 External URLs (after port forwarding):")
    print("   LED ON:  http://73.221.143.79:5000/dweet/for/2406874e?state=on")
    print("   LED OFF: http://73.221.143.79:5000/dweet/for/2406874e?state=off")
    print("   Status:  http://73.221.143.79:5000/get/latest/dweet/for/2406874e")
    print("\n🏠 Local URLs:")
    print("   LED ON:  http://10.0.0.71:5000/dweet/for/2406874e?state=on")
    print("   LED OFF: http://10.0.0.71:5000/dweet/for/2406874e?state=off")
    
    # Run the server
    app.run(host='0.0.0.0', port=5000, debug=False)  # debug=False for security