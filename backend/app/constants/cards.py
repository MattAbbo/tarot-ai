MAJOR_ARCANA_MAP = {
    'The Fool': '00-TheFool.jpg',
    'The Magician': '01-TheMagician.jpg',
    'The High Priestess': '02-TheHighPriestess.jpg',
    'The Empress': '03-TheEmpress.jpg',
    'The Emperor': '04-TheEmperor.jpg',
    'The Hierophant': '05-TheHierophant.jpg',
    'The Lovers': '06-TheLovers.jpg',
    'The Chariot': '07-TheChariot.jpg',
    'Strength': '08-Strength.jpg',
    'The Hermit': '09-TheHermit.jpg',
    'Wheel of Fortune': '10-WheelOfFortune.jpg',
    'Justice': '11-Justice.jpg',
    'The Hanged Man': '12-TheHangedMan.jpg',
    'Death': '13-Death.jpg',
    'Temperance': '14-Temperance.jpg',
    'The Devil': '15-TheDevil.jpg',
    'The Tower': '16-TheTower.jpg',
    'The Star': '17-TheStar.jpg',
    'The Moon': '18-TheMoon.jpg',
    'The Sun': '19-TheSun.jpg',
    'Judgement': '20-Judgement.jpg',
    'The World': '21-TheWorld.jpg'
}

NUMBER_MAP = {
    'Ace': '01', 'Two': '02', 'Three': '03', 'Four': '04', 'Five': '05',
    'Six': '06', 'Seven': '07', 'Eight': '08', 'Nine': '09', 'Ten': '10',
    'Page': '11', 'Knight': '12', 'Queen': '13', 'King': '14'
}

SUITS = ['Wands', 'Cups', 'Swords', 'Pentacles']
NUMBERS = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
COURTS = ['Page', 'Knight', 'Queen', 'King']

def generate_minor_arcana_map():
    minor_arcana = {}
    for suit in SUITS:
        for value in NUMBERS + COURTS:
            card_name = f"{value} of {suit}"
            filename = f"{suit}{NUMBER_MAP[value]}.jpg"
            minor_arcana[card_name] = filename
    return minor_arcana

MINOR_ARCANA_MAP = generate_minor_arcana_map()
ALL_CARDS = list(MAJOR_ARCANA_MAP.keys()) + list(MINOR_ARCANA_MAP.keys())