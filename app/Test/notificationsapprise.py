import apprise

# Create an Apprise instance
apobj = apprise.Apprise()

# Create an Config instance
config = apprise.AppriseConfig()

# Add a configuration source:
config.add('/opt/tachiyomimangaexporter/apprise.yml')

# Make sure to add our config into our apprise object
apobj.add(config)


apobj.notify(
    body='what a great notification service!',
    title='my notification title',
    tag='ok',
)

# Tagging allows you to specifically target only specific notification
# services you've loaded:
apobj.notify(
    body='send a notification to our admin group',
    title='Attention Admins',
    # notify any services tagged with the 'admin' tag
    tag='fallo',
)

# If you want to notify absolutely everything (reguardless of whether
# it's been tagged or not), just use the reserved tag of 'all':
apobj.notify(
    body='send a notification to our admin group',
    title='Attention Admins todos',
    # notify absolutely everything loaded, reguardless on wether
    # it has a tag associated with it or not:
    tag='all',
)