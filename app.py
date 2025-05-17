from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from datetime import datetime
import qrcode
import io
import base64
import json
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'sk-6zXLmwhw-DcQXCkVTOcXN5_kKUdPhXP6ZBQMl3nwiWT3BlbkFJEPTdCVjIKWAMWVQnkCEqQvt8F0yKp96XBvopWVtnMA'  # Required for session management

# Ensure feedback directory exists
FEEDBACK_DIR = Path('feedback')
FEEDBACK_DIR.mkdir(exist_ok=True)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.json
        rating = data.get('rating')
        comment = data.get('comment')
        
        if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'success': False, 'message': 'Invalid rating'})
            
        feedback = {
            'rating': rating,
            'comment': comment,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save feedback to a JSON file
        feedback_file = FEEDBACK_DIR / f'feedback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(feedback_file, 'w') as f:
            json.dump(feedback, f, indent=2)
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


# Sample museum data
museums = [
    {
        'name': 'National Museum, New Delhi',
        'image': 'https://lh3.googleusercontent.com/gps-cs-s/AB5caB-uyrGAqZWe5GJd4dH13_1JInTfwMTm_OztA1k4ZohmQw4cGNIFiNXaIVZoKODgaNixlK0SLO0XCBIo-i-7p9OcEO7RS_kDmog2gw1Rp1inHwQx_-fkb-4MzepZqxcqchU3_bQL=s1360-w1360-h1020',
        'indian_price': 50,
        'foreign_price': 650,
        'location': 'Janpath Road, New Delhi',
        'timing': '10:00 AM - 6:00 PM (Closed on Mondays)'
    },
    {
        'name': 'Salar Jung Museum, Hyderabad',
        'image': 'https://s7ap1.scene7.com/is/image/incredibleindia/salar-jung-museum-hyderabad-secunderabad-telangana-14-musthead-hero?qlt=82&ts=1726653045999',
        'indian_price': 40,
        'foreign_price': 500,
        'location': 'Salar Jung Road, Hyderabad',
        'timing': '10:00 AM - 5:00 PM (Closed on Fridays)'
    },
    {
        'name': 'Indian Museum, Kolkata',
        'image': 'https://indianmuseumkolkata.org/im_cont/uploads/2022/04/banner2.jpg',
        'indian_price': 30,
        'foreign_price': 500,
        'location': 'Park Street Area, Kolkata',
        'timing': '10:00 AM - 5:00 PM (Closed on Mondays)'
    },
    {
        'name': 'Chhatrapati Shivaji Maharaj Vastu Sangrahalaya',
        'image': 'https://s7ap1.scene7.com/is/image/incredibleindia/1-chatrapati-shivaji-maharaj-vastu-sangrahalaya-or-prince-of-wales-museum-mumbai-maharashtra-attr-hero?qlt=82&ts=1727355300214',
        'indian_price': 85,
        'foreign_price': 500,
        'location': 'Mahatma Gandhi Road, Fort, Mumbai',
        'timing': '10:15 AM - 6:00 PM (Open all days)'
    },
    {
        'name': 'Government Museum, Chennai',
        'image': 'https://indiano.travel/wp-content/uploads/2022/04/Beautiful-facade-at-the-Chennai-Government-Museum-Tamil-Nadu-India.jpg',
        'indian_price': 20,
        'foreign_price': 250,
        'location': 'Pantheon Road, Egmore, Chennai',
        'timing': '9:30 AM - 5:00 PM (Closed on Fridays)'
    },
    {
        'name': 'Albert Hall Museum, Jaipur',
        'image': 'https://s7ap1.scene7.com/is/image/incredibleindia/albert-hall-museum-jaipur-rajasthan-3-attr-hero?qlt=82&ts=1726660086518',
        'indian_price': 40,
        'foreign_price': 300,
        'location': 'Ram Niwas Garden, Jaipur',
        'timing': '9:00 AM - 5:00 PM (Open all days)'
    },
    {
        'name': 'Calico Museum of Textiles, Ahmedabad',
        'image': 'https://www.gujarattourism.com/content/dam/gujrattourism/images/museums/the-calico-museum-of-textiles/gallery/Calico-Craft-Centre%20(6).jpg',
        'indian_price': 0,
        'foreign_price': 0,
        'location': 'Shahibag, Ahmedabad',
        'timing': '10:30 AM - 12:30 PM (Closed on Wednesdays)'
    },
    {
        'name': 'Victoria Memorial Hall, Kolkata',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/7/72/Victoria_Memorial_situated_in_Kolkata.jpg',
        'indian_price': 30,
        'foreign_price': 500,
        'location': 'Queen\'s Way, Kolkata',
        'timing': '10:00 AM - 5:00 PM (Closed on Mondays)'
    },
    {
        'name': 'National Rail Museum, New Delhi',
        'image': 'https://travelsetu.com/apps/uploads/new_destinations_photos/destination/2023/12/27/cf2348671e1759431701ef932606187a_1000x1000.jpg',
        'indian_price': 50,
        'foreign_price': 650,
        'location': 'Chanakyapuri, New Delhi',
        'timing': '9:30 AM - 5:30 PM (Closed on Mondays)'
    },
    {
        'name': 'Maharaja Fateh Singh Museum, Vadodara',
        'image': 'https://travelsetu.com/apps/uploads/new_destinations_photos/destination/2023/12/20/e10dc327f45308a88170a1aeb05e8b24_1000x1000.jpg',
        'indian_price': 25,
        'foreign_price': 200,
        'location': 'Lukshmi Vilas Palace Complex, Vadodara',
        'timing': '10:00 AM - 5:30 PM (Open all days)'
    },
    {
        'name': 'Dr. Bhau Daji Lad Mumbai City Museum',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/1/1b/Dr._Bhau_Daji_Lad_Museum%2C_esterno_01.jpg',
        'indian_price': 10,
        'foreign_price': 100,
        'location': 'Byculla East, Mumbai',
        'timing': '10:00 AM - 6:00 PM (Closed on Wednesdays)'
    },
    {
        'name': 'State Museum Lucknow',
        'image': 'https://www.tourmyindia.com/socialimg/state-museum-lucknow.jpg',
        'indian_price': 10,
        'foreign_price': 100,
        'location': 'Banarasi Bagh, Lucknow',
        'timing': '10:30 AM - 4:30 PM (Closed on Mondays)'
    },
    {
        'name': 'Napier Museum, Thiruvananthapuram',
        'image': 'https://keralatourism.travel/images/places-to-visit/headers/napier-museum-trivandrum-tourism-entry-fee-timings-holidays-reviews-header.jpg',
        'indian_price': 20,
        'foreign_price': 100,
        'location': 'LMS Vellayambalam, Thiruvananthapuram',
        'timing': '10:00 AM - 5:00 PM (Closed on Mondays)'
    },
    {
        'name': 'Patna Museum',
        'image': 'https://s7ap1.scene7.com/is/image/incredibleindia/patna-museum-patna-bihar-1-musthead-hero?qlt=82&ts=1726740216293',
        'indian_price': 15,
        'foreign_price': 150,
        'location': 'Buddha Marg, Patna',
        'timing': '10:30 AM - 5:30 PM (Closed on Mondays)'
    },
    {
        'name': 'Archaeological Museum, Hampi',
        'image': 'https://s3.eu-west-2.amazonaws.com/tripspell/EXPERIENCE/archaeological-museum-hampi/archaeological-museum-hampi-0_high',
        'indian_price': 5,
        'foreign_price': 100,
        'location': 'Hampi, Karnataka',
        'timing': '10:00 AM - 5:00 PM (Closed on Fridays)'
    },
    {
        'name': 'Assam State Museum, Guwahati',
        'image': 'https://s7ap1.scene7.com/is/image/incredibleindia/assam-state-meseum-dispur-assam-hero-2?qlt=82&ts=1726741440084',
        'indian_price': 10,
        'foreign_price': 50,
        'location': 'Dighali Pukhuri, Guwahati',
        'timing': '10:00 AM - 5:00 PM (Closed on Mondays)'
    },
    {
        'name': 'City Palace Museum, Udaipur',
        'image': 'https://s7ap1.scene7.com/is/image/incredibleindia/city-palace-udaipur-rajasthan-1-new-attr-hero?qlt=82&ts=1727353238554',
        'indian_price': 30,
        'foreign_price': 200,
        'location': 'City Palace Complex, Udaipur',
        'timing': '9:30 AM - 5:30 PM (Open all days)'
    },
    {
        'name': 'Madhya Pradesh Tribal Museum, Bhopal',
        'image': 'https://cdn.elebase.io/173fe953-8a63-4a8a-8ca3-1bacb56d78a5/8a45764f-15e0-4562-b865-766db2f38293-tribal-gallery-01-michaelturtle.jpg?w=1000&h=500&fit=crop&q=75',
        'indian_price': 10,
        'foreign_price': 100,
        'location': 'Shyamla Hills, Bhopal',
        'timing': '12:00 PM - 7:00 PM (Closed on Mondays)'
    },
    {
        'name': 'Odisha State Museum, Bhubaneswar',
        'image': 'https://bhubaneswartourism.in/images/places-to-visit/headers/odisha-state-museum-bhubaneswar-tourism-entry-fee-timings-holidays-reviews-header.jpg',
        'indian_price': 10,
        'foreign_price': 50,
        'location': 'Lewis Road, Bhubaneswar',
        'timing': '10:00 AM - 5:00 PM (Closed on Mondays)'
    },
    {
        'name': 'Visvesvaraya Industrial Museum, Bangalore',
        'image': 'https://shop.museumsofindia.org/sites/default/files/2017-08/Iconic-1_41.jpg',
        'indian_price': 40,
        'foreign_price': 150,
        'location': 'Kasturba Road, Bangalore',
        'timing': '9:30 AM - 6:00 PM (Closed on Mondays)'
    },
    {
        'name': 'Himachal State Museum, Shimla',
        'image': 'https://shimlatourism.co.in/images/places-to-visit/headers/himachal-state-museum-shimla-tourism-entry-fee-timings-holidays-reviews-header.jpg',
        'indian_price': 10,
        'foreign_price': 50,
        'location': 'Chaura Maidan, Shimla',
        'timing': '10:00 AM - 5:00 PM (Closed on Mondays)'
    },
    {
        'name': 'Don Bosco Museum, Shillong',
        'image': 'https://s7ap1.scene7.com/is/image/incredibleindia/don-bosco-museum-shillong-meghalaya-2-attr-hero?qlt=82&ts=1726666113223',
        'indian_price': 50,
        'foreign_price': 100,
        'location': 'Mawlai, Shillong',
        'timing': '9:00 AM - 4:30 PM (Closed on Sundays)'
    },
    {
        'name': 'Goa State Museum, Panaji',
        'image': 'https://travelsetu.com/apps/uploads/new_destinations_photos/destination/2023/12/29/4d523e14e598498c43f8f582719992dd_1000x1000.jpg',
        'indian_price': 5,
        'foreign_price': 50,
        'location': 'EDC Complex, Patto, Panaji',
        'timing': '9:30 AM - 5:30 PM (Closed on Saturdays and Sundays)'
    },
    {
        'name': 'Baroda Museum and Picture Gallery',
        'image': 'https://www.gujarattourism.com/content/dam/gujrattourism/images/museums/baroda-museum-and-picture-gallery/gallery/Baroda-Museum-And-Picture-Gallery-(7).jpg',
        'indian_price': 15,
        'foreign_price': 200,
        'location': 'Sayajibaug, Vadodara',
        'timing': '10:30 AM - 5:30 PM (Closed on Wednesdays)'
    },
    {
        'name': 'Manipur State Museum, Imphal',
        'image': 'https://shop.museumsofindia.org/sites/default/files/2017-11/_IMG9707.jpg',
        'indian_price': 10,
        'foreign_price': 50,
        'location': 'Imphal West, Manipur',
        'timing': '10:00 AM - 4:30 PM (Closed on Mondays)'
    },
    {
        'name': 'Sikkim State Museum, Gangtok',
        'image': 'https://assets.telegraphindia.com/telegraph/2021/Mar/1616706645_1606159728_24nblttbudha_5col.jpg',
        'indian_price': 10,
        'foreign_price': 50,
        'location': 'MG Marg, Gangtok',
        'timing': '10:00 AM - 4:00 PM (Closed on Thursdays)'
    },
    {
        'name': 'Tripura State Museum, Agartala',
        'image': 'https://tripuratourism.gov.in/images/galleries/1662981378366/2.jpg',
        'indian_price': 5,
        'foreign_price': 50,
        'location': 'Ujjayanta Palace, Agartala',
        'timing': '10:00 AM - 5:00 PM (Closed on Mondays)'
    },
    {
        'name': 'Nagaland State Museum, Kohima',
        'image': 'https://www.kohimamuseum.co.uk/wp-content/uploads/2021/03/1.-Grover-and-Cuneo-corner-1024x768.jpg',
        'indian_price': 10,
        'foreign_price': 50,
        'location': 'Bayavu Hill, Kohima',
        'timing': '10:00 AM - 4:00 PM (Closed on Thursdays)'
    },
    {
        'name': 'Arunachal State Museum, Itanagar',
        'image': 'https://s7ap1.scene7.com/is/image/incredibleindia/jawahar-lal-nehru-museum-itanagar-arunachal-pradesh-attr-about?qlt=82&ts=1726743079331',
        'indian_price': 10,
        'foreign_price': 50,
        'location': 'Jawaharlal Nehru Museum, Itanagar',
        'timing': '10:00 AM - 4:00 PM (Closed on Mondays)'
    },
    {
        'name': 'Mizoram State Museum, Aizawl',
        'image': 'https://mizoculture.mizoram.gov.in/uploads/attachments/f7bd5306047d09f93657ecde394fe11c/dsc-5635.JPG',
        'indian_price': 10,
        'foreign_price': 50,
        'location': 'Zarkawt, Aizawl',
        'timing': '10:00 AM - 4:00 PM (Closed on Saturdays and Sundays)'
    }
]

@app.route('/')
def index():
    return render_template('index.html', museums=museums)

@app.route('/museums')
def show_museums():
    return render_template('museums.html', museums=museums)

@app.route('/chatbot')
def show_chatbot():
    # Clear chat history if requested
    if request.args.get('clear'):
        session.clear()
        return redirect(url_for('show_chatbot'))

    # Initialize chat session if not exists
    if 'chat_history' not in session:
        session['chat_history'] = [{
            'type': 'bot',
            'message': 'Hello! I\'m your AI assistant. To help you book museum tickets, could you please tell me your name?'
        }]
        session['booking_state'] = 'ask_name'
        session['user_data'] = {}

    return render_template('chatbot.html', chat_history=session.get('chat_history', []))

@app.route('/process_message', methods=['POST'])
def process_message():
    try:
        message = request.form.get('message', '').strip()
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        chat_history = session.get('chat_history', [])
        booking_state = session.get('booking_state', 'ask_name')
        
        # Add user message to chat history
        chat_history.append({
            'type': 'user',
            'message': message
        })
        session['chat_history'] = chat_history
        
        # Handle different states of the booking process
        if booking_state == 'ask_name':
            session['user_data']['name'] = message
            response = f'Nice to meet you, {message}! Are you an Indian national or a foreigner? (Please type "Indian" or "Foreigner")'
            session['booking_state'] = 'ask_nationality'

        elif booking_state == 'ask_nationality':
            nationality = message.lower()
            if nationality in ['indian', 'foreigner']:
                session['user_data']['nationality'] = nationality
                response = 'Please provide your 10-digit mobile number for ticket delivery.'
                session['booking_state'] = 'ask_mobile'
            else:
                response = 'Please type either "Indian" or "Foreigner" to proceed.'
        
        elif booking_state == 'ask_mobile':
          if message.isdigit() and len(message) == 10:
            session['user_mobile'] = message
            museum_list = '\n'.join([f"Museum {i+1}: {museum['name']}" for i, museum in enumerate(museums)])
            response = f"Thank you! Here are the available museums:\n\n{museum_list}\n\nPlease select a museum by entering its number (1-{len(museums)})."
            session['booking_state'] = 'select_museum'
          else:
            response = 'Please provide a valid 10-digit mobile number.'

        
        elif booking_state == 'select_museum':
            try:
                museum_index = int(message) - 1
                if 0 <= museum_index < len(museums):
                    selected_museum = museums[museum_index]
                    session['selected_museum'] = selected_museum
                    nationality = session['user_data'].get('nationality', 'indian')
                    price = selected_museum['foreign_price'] if nationality == 'foreigner' else selected_museum['indian_price']
                    response = f"Here are the details for {selected_museum['name']}:\n\nLocation: {selected_museum['location']}\nTiming: {selected_museum['timing']}\nPrice: ₹{price}\n\nHow many tickets would you like to book? (Maximum: 10)"
                    session['booking_state'] = 'select_quantity'
                else:
                    response = f'Please enter a number between 1 and {len(museums)}.'
            except ValueError:
                response = 'Please enter a valid number.'
        
        elif booking_state == 'select_quantity':
            try:
                quantity = int(message)
                if 1 <= quantity <= 10:
                    session['ticket_quantity'] = quantity
                    museum = session['selected_museum']
                    # Calculate total price based on nationality
                    nationality = session['user_data'].get('nationality', 'indian')
                    price = museum['foreign_price'] if nationality == 'foreigner' else museum['indian_price']
                    total_price = price * quantity
                    session['total_price'] = total_price
                    response = f'Total price: ₹{total_price}\nPlease select a payment method:\n1. Credit Card\n2. Debit Card\n3. UPI\n4. Wallets'
                    session['booking_state'] = 'select_payment'
                else:
                    response = 'Please enter a number between 1 and 10.'
            except ValueError:
                response = 'Please enter a valid number.'
        
        elif booking_state == 'select_payment':
            try:
                payment_method = int(message)
                if 1 <= payment_method <= 4:
                    payment_methods = {
                        1: 'credit_card',
                        2: 'debit_card',
                        3: 'upi',
                        4: 'wallet'
                    }
                    selected_method = payment_methods[payment_method]
                    total_price = session.get('total_price', 0)
                    return jsonify({
                        'redirect_to_payment': True,
                        'payment_method': selected_method,
                        'amount': f'₹{total_price}'
                    })
                else:
                    response = 'Please select a valid payment method (1-4).'
            except ValueError:
                response = 'Please enter a valid number for the payment method.'
        
        elif booking_state == 'ask_more_tickets':
            if message.lower() == 'yes':
                # Clear all session data
                session.clear()
                # Initialize new chat session
                session['chat_history'] = [{
                    'type': 'bot',
                    'message': 'Hello! I\'m your AI assistant. To help you book museum tickets, could you please tell me your name?'
                }]
                session['booking_state'] = 'ask_name'
                session['user_data'] = {}
                rendered_html = render_template('chatbot_messages.html', chat_history=session['chat_history'])
                return jsonify({'html': rendered_html})
            elif message.lower() == 'no':
                # Clear session and redirect to index
                session.clear()
                return jsonify({
                    'redirect': True,
                    'url': url_for('index', _external=True)
                })
            else:
                response = 'Please type "yes" to book more tickets or "no" to return to homepage.'
                chat_history.append({
                    'type': 'bot',
                    'message': response
                })
                session['chat_history'] = chat_history
                rendered_html = render_template('chatbot_messages.html', chat_history=chat_history)
                return jsonify({'html': rendered_html})
        
        # Add bot response to chat history
        chat_history.append({
            'type': 'bot',
            'message': response
        })
        
        session['chat_history'] = chat_history
        rendered_html = render_template('chatbot_messages.html', chat_history=chat_history)
        return jsonify({'html': rendered_html})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/book_museum/<museum_name>', methods=['GET'])
def book_museum(museum_name):
    session.clear()
    chat_history = [{
        'type': 'bot',
        'message': f'I can help you book tickets for {museum_name}. How many tickets would you like to book?'
    }]
    session['chat_history'] = chat_history
    session['booking_state'] = 'select_quantity'
    session['selected_museum'] = next((m for m in museums if m['name'] == museum_name), None)
    return render_template('chatbot.html', chat_history=chat_history)

@app.route('/payment')
def payment():
    payment_method = request.args.get('method')
    amount = request.args.get('amount')
    
    if not payment_method or not amount:
        return redirect(url_for('show_chatbot'))
    
    session['payment_method'] = payment_method
    session['total_price'] = amount.replace('₹', '')
    
    return render_template('payment.html', 
                          payment_method=payment_method,
                          amount=amount)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if 'payment_method' not in session or 'selected_museum' not in session or 'ticket_quantity' not in session:
        return jsonify({'error': 'Invalid session. Please try booking again.'}), 400

    payment_method = request.form.get('payment_method')
    if not payment_method:
        return jsonify({'error': 'Payment method is required'}), 400
        
    # Additional validation for wallet payments
    if payment_method == 'wallet':
        wallet_provider = request.form.get('wallet_provider')
        wallet_number = request.form.get('wallet_number')
        
        # Validate wallet provider
        if not wallet_provider:
            return jsonify({'error': 'Please select a wallet provider'}), 400
        valid_providers = ['paytm', 'phonepe', 'gpay', 'amazonpay']
        if wallet_provider not in valid_providers:
            return jsonify({'error': 'Invalid wallet provider selected'}), 400
            
        # Validate mobile number
        if not wallet_number:
            return jsonify({'error': 'Mobile number is required'}), 400
        if not wallet_number.isdigit():
            return jsonify({'error': 'Mobile number should contain only digits'}), 400
        if len(wallet_number) != 10:
            return jsonify({'error': 'Mobile number must be exactly 10 digits'}), 400

    # Ensure chat_history exists and is a list
    if 'chat_history' not in session or not isinstance(session['chat_history'], list):
        session['chat_history'] = []

    try:
        # Generate ticket
        ticket_number = f"TKT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        museum = session['selected_museum']
        quantity = session['ticket_quantity']
        
        # Create QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"Ticket: {ticket_number}\nMuseum: {museum['name']}\nQuantity: {quantity}")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert QR code to base64 string
        buffered = io.BytesIO()
        qr_img.save(buffered, format="PNG")
        qr_code = base64.b64encode(buffered.getvalue()).decode()
        
        # Add ticket confirmation to chat history
        ticket_confirmation = f"""
        <div class='ticket-confirmation'>
            <h4>🎫 Booking Confirmed!</h4>
            <p><strong>Ticket Number:</strong> {ticket_number}</p>
            <p><strong>Museum:</strong> {museum['name']}</p>
            <p><strong>Quantity:</strong> {quantity}</p>
            <p><strong>Location:</strong> {museum['location']}</p>
            <p><strong>Timing:</strong> {museum['timing']}</p>
            <p><strong>Payment Method:</strong> {payment_method.replace('_', ' ').title()}</p>
            <div class='qr-code'>
                <img src='data:image/png;base64,{qr_code}' alt='QR Code'>
            </div>
        </div>
        """
        
        # Store ticket in session
        if 'tickets' not in session:
            session['tickets'] = []
        session['tickets'].append({
            'ticket_number': ticket_number,
            'museum': museum['name'],
            'quantity': quantity,
            'payment_method': payment_method
        })
        
        # Update chat history with ticket confirmation
        session['chat_history'].append({
            'type': 'bot',
            'message': ticket_confirmation,
            'time': datetime.now().strftime('%I:%M %p')
        })
        
        # Add mobile confirmation message
        session['chat_history'].append({
            'type': 'bot', 
            'message': f'📱 Your tickets have been successfully sent to your mobile number {session["user_mobile"]}',
            'time': datetime.now().strftime('%I:%M %p')
        })
        
        # Add prompt for booking more tickets
        session['chat_history'].append({
            'type': 'bot',
            'message': 'Would you like to book more tickets? Type "yes" or "no"',
            'time': datetime.now().strftime('%I:%M %p')
        })
        session['booking_state'] = 'ask_more_tickets'
        
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/payment_success')
def payment_success():
    # Process the payment and generate ticket
    return redirect(url_for('process_payment'), code=307)  # Use 307 to preserve POST method

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)