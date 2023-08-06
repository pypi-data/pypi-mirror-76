# AA Discord Ping Formatter

App for formatting pings for Discord in Alliance Auth

## Contents

- [Installation](#installation)
- [Updating](#updating)
- [Screenshots](#screenshots)
- [Configuration](#configuration)
- [Change Log](CHANGELOG.md)

## Installation

**Important**: This app is a plugin for Alliance Auth. If you don't have Alliance Auth running already, please install it first before proceeding. (see the official [AA installation guide](https://allianceauth.readthedocs.io/en/latest/installation/allianceauth.html) for details)

### Step 1 - Install app

Make sure you are in the virtual environment (venv) of your Alliance Auth installation. Then install the latest version:

```bash
pip install aa-discord-ping-formatter
```

### Step 2 - Update your AA settings

Configure your AA settings (`local.py`) as follows:

- Add `'discordpingformatter',` to `INSTALLED_APPS`


### Step 3 - Finalize the installation

Run migrations & copy static files

```bash
python manage.py collectstatic
python manage.py migrate
```

Restart your supervisor services for AA

### Step 4 - Setup permissions

Now you can setup permissions in Alliance Auth for your users. Add ``discordpingformatter | aa discord ping formatter | Can access this app`` to the states and/or groups you would like to have access.

## Updating

To update your existing installation of AA Discord Ping Formatter first enable your virtual environment.

Then run the following commands from your AA project directory (the one that contains `manage.py`).

```bash
pip install -U aa-discord-ping-formatter
```

```bash
python manage.py collectstatic
```

```bash
python manage.py migrate
```

Finally restart your AA supervisor services.

## Screenshots

### View in Alliance Auth

![AA View](https://raw.githubusercontent.com/ppfeufer/aa-discord-ping-formatter/master/discordpingformatter/docs/aa-view.jpg)

### Discord Ping

![Discord Ping Examples](https://raw.githubusercontent.com/ppfeufer/aa-discord-ping-formatter/master/discordpingformatter/docs/ping-examples.jpg)

_(Example for embedded ping (top) and non embedded ping (bottom))_

## Configuration

### Embed Webhook Pings

You have the option to embed your webhook pings. To do so you can enable it via:

```python
## AA Discord Ping Formatter
AA_DISCORDFORMATTER_WEBHOOK_EMBED_PING = True
```

### Adding Ping Targets

Per default you have 2 ping targets you can select from. That's `@everyone` and `@here`. If you need more than these 2, you can add them to your `local.py` and override the default behaviour that way.

Open your `local.py` in an editor of your choice and add the following at the end.

```python
## AA Discord Ping Formatter
AA_DISCORDFORMATTER_ADDITIONAL_PING_TARGETS = [
    {
        'roleId': 'xxxxxxxxxxxxxxxxxx',
        'roleName': 'Member'
    },
    {
        # restricted to "Capital FCs" (GroupID 5) and "Super Capital FCs" (GroupID 7)
        'restrictedToGroup': [
            5,
            7,
        ],
        'roleId': 'xxxxxxxxxxxxxxxxxx',
        'roleName': 'Capital Pilots'
    },
]
```

To get the `roleId` go to your Discord Server Settings » Roles and right click the role you need and copy the ID. You might need to activate the Developer Mode for your Discord account in order to do so. You activate the Developmer Mode in your account settings under Appearance » Advanced » Developer Mode.

**Important:** Both, `roleId` and `roleName` need to be without the `@`, it will be added automatically. `roleName` needs to be spelled exactly as it is on Discord.

### Adding Fleet Types
Per default you have 4 fleet types you can select from. That's `Roam`, `Home Defense`, `StratOP` and `CTA`. If you need more than these 4, you can add them to your `local.py` and override the default behaviour that way.

Open your `local.py` in an editor of your choice and add the following at the end.

```python
## AA Discord Ping Formatter
AA_DISCORDFORMATTER_ADDITIONAL_FLEET_TYPES = [
    # example for embedded webhook pings
    {
        'fleetType': 'Mining',
        'embedColor': '#4F545C' # can be empty but needs to be set. Needs to be #hex and 6 digits
    },

    # example for non embedded webhook pings
    'Ratting',
]
```

Both examples will work, no matter if you have `AA_DISCORDFORMATTER_WEBHOOK_EMBED_PING` enabled or not. But keep in mind, to set a custom color for your embed, it needs to be defined like in the first example. The color needs to be your standard hex color code like you define it in (for example) CSS as well. Pre-defined fleet types are by default: Roam = green, Home Defense = yellow, StratOP = orange, CTA = red

### Adding Ping Channels
Per default, your ping will just be formatted for you to copy and paste. But, if your FCs are too lazy even for that, you can configure webhooks. One for each channel you might want to ping.

Open your `local.py` in an editor of your choice and add the following at the end.

```python
## AA Discord Ping Formatter
AA_DISCORDFORMATTER_ADDITIONAL_PING_WEBHOOKS = [
    {
        'discordChannelName': 'Fleet Pings (#fleet-pings)',
        'discordWebhookUrl': 'https://discordapp.com/api/webhooks/xxxxxxxxxxxxxxxxxx/yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
    },
    {
        'discordChannelName': 'Pre Pings (#pre-pings)',
        'discordWebhookUrl': 'https://discordapp.com/api/webhooks/xxxxxxxxxxxxxxxxxx/yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
    },
    {
        # restricted to "Capital FCs" (GroupID 5) and "Super Capital FCs" (GroupID 7)
        'restrictedToGroup': [
            5,
            7,
        ],
        'discordChannelName': 'Capital Pings (#capital-pings)',
        'discordWebhookUrl': 'https://discordapp.com/api/webhooks/xxxxxxxxxxxxxxxxxx/yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
    }
]
```

### Fleet Comms, Formup Location and Doctrine

Values for Fleet Comms, Formup Location and Doctrine can be pre-defined as suggestions, so your FCs have a quick selection of the most used comms, stagings and doctrines to select from. These are not fixed values in the form, since we use a combination of input and select fields here. So FCs are absolutely free to something completely different in those 3 fields than the pre-defined suggestions.

To define these 3 fields, open your `local.py` in an editor of your choice and add the following:

Fleet Comms
```python
## AA Discord Ping Formatter
AA_DISCORDFORMATTER_FLEET_COMMS = [
    'Alliance Mumble',
    'Coalition Mumble',
    'Spy Account Mumble' # :-P
]
```

Fleet Staging
```python
## AA Discord Ping Formatter
AA_DISCORDFORMATTER_FLEET_FORMUP_LOCATIONS = [
    'Alliance Staging System',
    'Coalition Staging System'
]
```

Doctrine
```python
## AA Discord Ping Formatter
AA_DISCORDFORMATTER_FLEET_DOCTRINES = [
    'Battle Skiffs',
    'Combat Nereus',
    'Attack Corvettes'
]
```
