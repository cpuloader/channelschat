# channelschat

Simple dating site with frontend on Angular 4 (webpacked here) and backend on Django, for media hosting Cloudinary.

Built-in chat works with WebSockets, I used parts from https://github.com/jacobian/channels-example/ Django Channels example.

Authentication by token with djangorestframework-jwt.

Settings for Cloudinary:
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': '<your cloud name>',
    'API_KEY': '<your key>',
    'API_SECRET': '<your secret>'
}
(or CLOUDINARY_URL)
and
YOUR_CLOUDINARY_NAME = '<your cloud name>'

For default profile picture upload two jpgs on Cloudinary with names default_profile and default_profile_mini,
its path should be 'https://res.cloudinary.com/<YOUR_CLOUDINARY_NAME>/image/upload/v1/media/default_profile'
and 'https://res.cloudinary.com/<YOUR_CLOUDINARY_NAME>/image/upload/media/default_profile_mini'

