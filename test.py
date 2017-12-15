from urllib.request import urlretrieve

#url = "https://api.twilio.com/2010-04-01/Accounts/AC9c66e37e40c41409070dd8da2ca8be78/Messages/MM8e3a0a27170f1bcd87324b50963eff06/Media/ME95e1359149ff2a5dffb5891d7fca4388"

url = "https://image.slidesharecdn.com/xiquftatrgqotn6fspqr-signature-196ed891eeb4cbd064931f46c5574c792e4c4febe826d5d853512d748fc7f015-poli-151209165441-lva1-app6892/95/python-workshop-80-638.jpg?cb=1449681455"
#user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46'
#urlretrieve(Request(str(url), data=None, headers={'User-Agent': user_agent}))

urlretrieve(url, "file_name")

print('done')