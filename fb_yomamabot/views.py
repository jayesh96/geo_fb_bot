# yomamabot/fb_yomamabot/views.py
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "EAADKGhPh2u0BACAJ6hCHArGbnukjVNQdZAVOmZC1aNuxCtqzuFlM1Shzjn95VdvEkIHvEwaY1OcipuOxKbDRxZBgfczBH7pDVgLy6vFcJGr5322M4dMGrHoVP0PgWGBSfLVcIkZCk8XigZBt2ZAUvBl69ZAtTBfl0q5D1QPoNlbRgZDZD"
VERIFY_TOKEN = "2318934571"


# Helper function
def post_facebook_message(fbid, latitude, longitude):
    # Remove all punctuations, lower case the text and split it based on space
    string = str(latitude) + " , " + str(longitude)
    print (string)

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json() 
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps(
    				{
    					"recipient":
    						{
    							"id":fbid
    						}, 
    					"message":
    						{
    							"text":string
    						}
    						})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

# Create your views here.
class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)   
  	                # post_facebook_message(message['sender']['id'], message['message']['text'])      
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    if 'attachments' in message['message']:
                    	str =  message['message']['attachments']
                    	print ("$$$$$$$$$$$$$$$$$$$$")
                    	for json_i in str:
                    		content_type = json_i['type']
                    		if content_type == 'location':
                    			message_coordinates = json_i['payload']['coordinates']
                    			latitude = message_coordinates['lat']
                    			longitude = message_coordinates['long']
                    			print (latitude, longitude)
                    			post_facebook_message(message['sender']['id'], latitude, longitude)
                    		if content_type == 'image':
                    			print("Image collected")
                    else:
                    	print(message['message']['text'])

        return HttpResponse()    






# {u'message':
# 	 {u'attachments':
# 	 	 [{u'payload': 
# 	 	 	{u'coordinates': 
# 	 	 		{u'lat': 28.69694,
#                 u'long': 77.189583
#                 }
#             },
#        u'title': u"Jayesh's Location",
#        u'type': u'location',
#        u'url': u'https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.bing.com%2Fmaps%2Fdefault.aspx%3Fv%3D2%26pc%3DFACEBK%26mid%3D8100%26where1%3D28.69694%252C%2B77.189583%26FORM%3DFBKPL1%26mkt%3Den-US&h=ATPHC_07DXGXz94-MYaLuhRp9Trn6deVvusyzzoZU91wB7umR5JduyV9vgysBQJ3PJPWx26wsWni0X3f1cUUwjhMWKrhhynzlxyT_RRGCJaeQLrQglbphkbOGMUFxGKAsHDN_mk&s=1&enc=AZPWTgyIBzM-cMgUjjhDVfd4kHOHoUPjHYPqiAfmT9tkNx5j-Ig4MQR6U4RdsVyIoJKKsGqu0IzdtQD6l14mSEQc'
#		}],
#   u'mid': u'mid.1485969512107:43be98ba56',
#   u'seq': 99601},
#  u'recipient': {u'id': u'1664819267163136'},
#  u'sender': {u'id': u'1290682247622958'},
#  u'timestamp': 1485969512107}


# {
# 	u'message': 
# 		{
# 		u'mid': u'mid.1485970133711:f51478c063',
#         u'seq': 99613,
#         u'text': u'G'
#         },
#  	u'recipient': {
#  			u'id': u'1664819267163136'
#  			},
#  	u'sender': {
#  		u'id': u'1290682247622958'
#  		},
#  	u'timestamp': 1485970133711
#  }


# {
#   "sender":{
#     "id":"USER_ID"
#   },
#   "recipient":{
#     "id":"PAGE_ID"
#   },
#   "timestamp":1458692752478,
#   "message":{
#     "mid":"mid.1458696618141:b4ef9d19ec21086067",
#     "seq":51,
#     "attachments":[
#       {
#         "type":"image",
#         "payload":{
#           "url":"IMAGE_URL"
#         }
#       }
#     ]
#   }
# }    