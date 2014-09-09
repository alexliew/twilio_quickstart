from flask import Flask, render_template, request
from twilio.util import TwilioCapability
import twilio.twiml

import re

app = Flask(__name__)

# Add a Twilio phone number of number verified with Twilio as the caller ID
caller_id = "+14152179350"

# Put default Twilio client name here, for when a phone number isn't given
default_client = "jenny"

@app.route('/voice', methods=['GET', 'POST'])
def voice():
	dest_number = request.values.get('PhoneNumber', None)

	resp = twilio.twiml.Response()

	# Nest <Client> TwiML inside of a <Dial> verb
	with resp.dial(callerId=caller_id) as r:
		# If we havea number, and it looks like a phone number
		if dest_number and re.search('^[\d\(\)\- \+]+$', dest_number):
			r.number(dest_number)
		else:
			r.client(dest_number)

	return str(resp)

@app.route("/client", methods=['GET', 'POST'])
def client():
	"""Respond to incoming requests."""

	client_name = request.values.get('client', None) or "jenny"

	account_sid = "ACdb17aa016cef6c07c6cc64c90bfff660"
	auth_token = "33e489cbe322c5c3eab7e0b42bfb2950"

	capability = TwilioCapability(account_sid, auth_token)

	# This is a special Quickstart application sid
	application_sid = "APabe7650f654fc34655fc81ae71caa3ff"
	capability.allow_client_outgoing(application_sid)
	# I love you Jenn-ey
	capability.allow_client_incoming(client_name)
	token = capability.generate()

	return render_template('client.html', token=token, client_name=client_name)

if __name__ == "__main__":
    app.run(debug=True)
