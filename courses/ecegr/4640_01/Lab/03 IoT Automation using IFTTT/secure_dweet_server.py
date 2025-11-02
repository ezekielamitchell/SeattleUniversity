from flask import Flask, request, jsonify, abort
from datetime import datetime
import json
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# storage for dweets
dweets = {}

# allowed thing names
ALLOWED_THINGS = ['2406874e']

# rate limiting counter
request_counts = {}

def is_allowed_thing(thing_name):
    return thing_name in ALLOWED_THINGS

def rate_limit_check(client_ip):
    current_time = datetime.now().timestamp()
    
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    
    # remove old requests
    request_counts[client_ip] = [
        ts for ts in request_counts[client_ip] 
        if current_time - ts < 60
    ]
    
    # max 30 per minute
    if len(request_counts[client_ip]) >= 30:
        return False
    
    request_counts[client_ip].append(current_time)
    return True

@app.before_request
def security_check():
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ['REMOTE_ADDR'])
    
    if not rate_limit_check(client_ip):
        logger.warning(f"Rate limit exceeded for {client_ip}")
        abort(429)

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
    try:
        if not is_allowed_thing(thing_name):
            logger.warning(f"Unauthorized thing name attempted: {thing_name}")
            abort(403)
        
        content = dict(request.args)
        
        # convert lists to strings
        for key, value in content.items():
            if isinstance(value, list) and len(value) == 1:
                content[key] = value[0]
        
        dweet_entry = {
            "thing": thing_name,
            "created": datetime.utcnow().isoformat() + "Z",
            "content": content
        }
        
        dweets[thing_name] = dweet_entry
        
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ['REMOTE_ADDR'])
        logger.info(f"Dweet from {client_ip} for {thing_name}: {content}")
        
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
    try:
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
    
    app.run(host='0.0.0.0', port=5000, debug=False)