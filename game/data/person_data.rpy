init python:
    person_names = {
        'male': [__('Adolf'), __('Adrian'),__('Alen'),__('Alfons'),__('Aler'),
        __('Ambraus'),__('Anatole'),__('Andrian'),__('Andre'),__('Arman'),
        __('Arno'),__('Astor'),__('Antanas'),__('Basile'),__('Baptist'),
        __('Barnaby'),__('Bastian'),__('Besenet'),__('Bernard'),__('Bleiz'),
        __('Boduen'),__('Boniface'),__('Brees'),__('Valentine'),__('Gay'),
        __('Gaston'),__('Gaspard'),__('Godard'),__('Gilbert'),__('Guilem'),
        __('Gustav'),__('Denis'),__('Jeremy'),__('Joseph'),__('Jory'),
        __('Dominique'),__('Jacque'),__('Jan'),__('Jerom'),__('Jile'),
        __('Jerard'),__('Joffrua'),__('Julian'),__('Ivon'),__('Kamil'),
        __('Klementh'),__('Kolombo'),__('Kristoff'),__('Lasare'),__('Lionel'),
        __('Leonard'),__('Leopold'),__('Lorence'),__('Lotar'),__('Luie'),
        __('Luke'),__('Lucian'),__('Maximilian'),__('Matice'),__('Morrice'),
        __('Nikolas'),__('Nihel'),__('Oberon'),__('Olyvier'),__('Paskal'),
        __('Ogasten'),__('Odrik'),__('Patrice'),__('Parcifale'),__('Raimondo'),
        __('Raul'),__('Renard'),__('Robert'),__('Rojer'),__('Roderik'),
        __('Roland'),__('Sverus'),__('Cesare'),__('Stefano'),__('Theo'),
        __('Tyerri'),__('Fabis'),__('Felix'),__('Fabian'),__('Phillippe'),
        __('Forest'),__('Frank'),__('Hamon'),__('Honor'),__('Chrles'),
        __('Edvard'),__('Emerik'),__('Etien'),__('Judes'),__('Jurben'),
        __('Adelstain'),__('Adler'),__('Albert'),__('Alfonce'),__('Arnold'),
        __('Bertold'),__('Willie'),__('Wolf'),__('Wolfgang'),__('Ganse'),
        __('Gunter'),__('Godric'),__('Genrich'),__('Gerorge'),__('Gottfold'),
        __('Ditrich'),__('Karl'),__('Johan'),__('Kristof'),__('Leopold'),
        __('Markus'),__('Nikolas'),__('Zigberd'),__('Ulrich'),__('Urgen'),
        __('Vito'),__('Gonzalo'),__('Gustavo'),__('Havier'),__('Julian'),
        __('Diego'),__('Dimas'),__('Donato'),__('Domingo'),__('Jose'),
        __('Karlito'),__('Karlos'),__('Krisobal'),__('Luis'),__('Patricio'),
        __('Jacob'), __('Mason'),__('Ethan'),__('Noah'),__('William'),
        __('Liam'),__('Jayden'),__('Michael'),__('Alexander'),__('Aiden'),
        __('Daniel'),__('Matthew'),__('Elijah'),__('James'),__('Anthony'),
        __('Benjamin'),__('Joshua'),__('Andrew'),__('David'),__('Joseph'),
        __('Logan'),__('Jackson'),__('Christopher'),__('Gabriel'),__('Samuel'),
        __('Ryan'),__('Lucas'),__('John'),__('Nathan'),__('Isaac'),
        __('Dylan'),__('Caleb'),__('Christian'),__('Landon'),__('Jonathan'),
        __('Carter'),__('Luke'),__('Owen'),__('Brayden'),__('Gavin'),
        __('Wyatt'),__('Isaiah'),__('Henry'),__('Eli'),__('Hunter'),
        __('Jack'),__('Evan'),__('Jordan'),__('Nicholas'),__('Tyler'),
        __('Aaron'),__('Jeremiah'),__('Julian'),__('Cameron'),__('Levi'),
        __('Brandon'),__('Angel'),__('Austin'),__('Connor'),__('Adrian'),
        __('Robert'),__('Charles'),__('Thomas'),__('Sebastian'),__('Colton'),
        __('Jaxon'),__('Kevin'),__('Zachary'),__('Ayden'),__('Dominic'),
        __('Blake'),__('Jose'),__('Oliver'),__('Justin'),__('Bentley'),
        __('Jason'),__('Chase'),__('Ian'),__('Josiah'),__('Parker'),
        __('Xavier'),__('Adam'),__('Cooper'),__('Nathaniel'),__('Grayson'),
        __('Jace'),__('Carson'),__('Nolan'),__('Tristan'),__('Luis'),
        __('Brody'),__('Juan'),__('Hudson'),__('Bryson'),__('Carlos'),
        __('Easton'),__('Damian'),__('Alex'),__('Kayden'),__('Ryder'), ],

        'female': [__('Abelia'),__('Abel'),__('Avrora'),__('Agnes'),__('Adele'),
        __('Alexandra'),__('Ammaranthe'),__('Anastasia'),__('Angelique'),__('Annete'),
        __('Anette'),__('Aurelie'),__('Barbara'),__('Bernadette'),__('Blanche'),
        __('Brigitte'),__('Valentine'),__('Valerie'),__('Victoria'),__('Virgine'),
        __('Gabriella'),__('Gvinniver'),__('Godelif'),__('Daniela'),__('Dafna'),
        __('Denise'),__('Jine'),__('Jinnet'),__('Joel'),__('Josie'),
        __('Julie'),__('Juliette'),__('Justine'),__('Dominique'),__('Dorotea'),
        __('Jaquline'),__('Jen'),__('Julien'),__('Zoe'),__('Ivette'),
        __('Ivonne'),__('Inesse'),__('Iren'),__('Izidore'),__('Kamilla'),
        __('Karol'),__('Kler'),__('Kolette'),__('Katrine'),__('Kristine'),
        __('Lidy'),__('Lillian'),__('Lulu'),__('Madlene'),__('Megane'),
        __('Melisa'),__('Morgane'),__('Merrion'),__('Nadia'),__('Ninnet'),
        __('Noel'),__('Orabel'),__('Peneloppe'),__('Poline'),__('Polette'),
        __('Rosalie'),__('Sabina'),__('Simonete'),__('Sophie'),__('Stephanie'),
        __('Susette'),__('Felicia'),__('Helen'),__('Khloya'),__('Florette'),
        __('Chantalle'),__('Charlotte'),__('Evette'),__('Evone'),__('Elison'),
        __('Emily'),__('Enn'),__('Estel'),__('Eloise'),__('Elise'),
        __('Abigail'),__('Agate'),__('Alba'),__('Angela'),__('Beatrice'),
        __('Blanka'),__('Veronique'),__('Gracia'),__('Debora'),__('Delphine'),
        __('Dorotea'),__('Isabelle'),__('Konchitta'),__('Luise'),__('Marcelle'),
        __('Miquelle'),__('Monique'),__('Mirabella'),__('Ophelia'),__('Ramona'),
        __('Alina'),__('Alberthine'),__('Belinde'),__('Brunhild'),__('Gretta'),
        __('Zelda'),__('Isolde'),__('Irma'),__('Karoline'),__('Lisa'),
        __('Raphaella'),__('Susie'),__('Ulrike'),__('Franciska'),__('Hilde'),
        __('Sophia'),__('Emma'),__('Isabella'),__('Olivia'),__('Ava'),
        __('Emily'),__('Abigail'),__('Mia'),__('Madison'),__('Elizabeth'),
        __('Chloe'),__('Ella'),__('Avery'),__('Addison'),__('Aubrey'),
        __('Lily'),__('Natalie'),__('Sofia'),__('Charlotte'),__('Zoey'),
        __('Grace'),__('Hannah'),__('Amelia'),__('Harper'),__('Lillian'),
        __('Samantha'),__('Evelyn'),__('Victoria'),__('Brooklyn'),__('Zoe'),
        __('Layla'),__('Hailey'),__('Leah'),__('Kaylee'),__('Anna'),
        __('Aaliyah'),__('Gabriella'),__('Allison'),__('Nevaeh'),__('Alexis'),
        __('Audrey'),__('Savannah'),__('Sarah'),__('Alyssa'),__('Claire'),
        __('Taylor'),__('Riley'),__('Camila'),__('Arianna'),__('Ashley'),
        __('Brianna'),__('Sophie'),__('Peyton'),__('Bella'),__('Khloe'),
        __('Genesis'),__('Alexa'),__('Serenity'),__('Kylie'),__('Aubree'),
        __('Scarlett'),__('Stella'),__('Maya'),__('Katherine'),__('Julia'),
        __('Lucy'),__('Madelyn'),__('Autumn'),__('Makayla'),__('Kayla'),
        __('Mackenzie'),__('Lauren'),__('Gianna'),__('Ariana'),__('Faith'),
        __('Alexandra'),__('Melanie'),__('Sydney'),__('Bailey'),__('Caroline'),
        __('Naomi'),__('Morgan'),__('Kennedy'),__('Ellie'),__('Jasmine'),
        __('Eva'),__('Skylar'),__('Kimberly'),__('Violet'),__('Molly'),
        __('Aria'),__('Jocelyn'),__('Trinity'),__('London'),__('Lydia'),
        __('Madeline'),__('Reagan'),__('Piper'),__('Andrea'),__('Annabelle'),]
    }

    person_genders = ['male', 'female']
    person_genuses = ['human', 'undead', 'canine', 'fairy', 'slime']
    person_ages = ['junior', 'adolescent', 'mature', 'elder']

    core_attributes = {
        'might': {'name': __('Might'), 'low': __('Weak'), 'high': __('Hardy')},
        'subtlety': {'name': __('Subtlety'), 'low': __('Naive'), 'high': __('Subtle')},
        'charisma': {'name': __('Charisma'), 'low': __('Boring'), 'high': __('Charming')},
        'knowledge': {'name': __('Knowledge'), 'low': __('Incompetent'), 'high': __('Competent')},
    }

    core_features = {
        'male': {'slot': 'gender', 'name': __('Male'), 'might': 1, 'subtlety': -1},
        'female': {'slot': 'gender', 'name': __('Female'), 'subtlety': 1, 'might': -1},
    }

    core_age_features = {
        'junior': {
            'slot': 'age',
            'name': __("Junior"),
            'might': -1,
            'knowledge': -1,
            'charisma': 1,
        },
        'elder': {
            'slot': 'age',
            'name': __("Elder"),
            'might': -1,
            'knowledge': 1,
        },
        'adolescent': {
            'slot': 'age',
            'name': __("Adolescent"),
            'knowledge': -1,
            'subtlety': 1,
            'charisma': 1,
        },
        'mature': {
            'slot': 'age',
            'name': __("Mature"),
            'might': 1,
        },
    }

    core_physical_features = {
        'tall': {'slot': 'height', 'name': __('Tall'), 'might': 1, 'subtlety': -1},
        'small': {'slot': 'height', 'name': __('Small'), 'might': -1, 'subtlety': 1},
        'subtle': {'slot': 'constitution', 'name': __('Subtle'), 'might': -1, 'subtlety': 1},
        'brawny': {'slot': 'constitution', 'name': __('Brawny'), 'might': 1, 'subtlety': -1},
        'husky_voice': {'slot': 'voice', 'name': __('Husky voice'), 'might': 1, 'charisma': -1},
        'clear_voice': {'slot': 'voice', 'name': __('Clear voice'), 'might': -1, 'charisma': 1},
        'seductive_smile': {'slot': 'smile', 'name': __('Seductive smile'), 'subtlety': 1, 'might': -1},
        'coarse_grin': {'slot': 'smile', 'name': __('Coarse grin'), 'might': 1, 'charisma': -1},
        'giggly': {'slot': 'smile', 'name': __('Giggly'), 'charisma': 1, 'knowledge': -1},
        'inexpressive_face': {'slot': 'smile', 'name': __('Inexpressive face'), 'charisma': -1, 'knowledge': 1},
        'thick_skin': {'slot': 'skin', 'name': __('Thick skin'), 'might': 1, 'charisma': -1},
        'smooth_skin': {'slot': 'skin', 'name': __('Smooth skin'), 'might': -1, 'charisma': 1},
        'leery_eyes': {'slot': 'eyes', 'name': __('Leery eyes'), 'subtlety': 1},
        'firm_gaze': {'slot': 'eyes', 'name': __('Firm gaze'), 'might': 1},
        'bright_eyes': {'slot': 'eyes', 'name': __('Bright eyes'), 'charisma': 1},
        'enigmatic_gaze': {'slot': 'eyes', 'name': __('Enigmatic gaze'), 'knowledge': 1},
        'flat_chest': {'slot': 'boobs', 'name': __('Flat chest'), 'charisma': -1, 'subtlety': 1},
        'gazongas': {'slot': 'boobs', 'name': __('Gazongas'), 'charisma': 1, 'subtlety': -1},
        'small_wiener': {'slot': 'dick', 'name': __('Small wiener'), 'might': -1, 'subtlety': 1},
        'big_dick': {'slot': 'boobs', 'name': __('Big dick'), 'might': 1, 'subtlety': -1},
    }

    core_alignment_features = {
        'gluttonous': {'slot': 'nutrition', 'name': __('Gluttonous'), 'charisma': 1},
        'temperate': {'slot': 'nutrition', 'name': __('Temperate'), 'knowledge': 1},
        'proud': {'slot': 'authority', 'name': __('Proud'), 'might': 1},
        'humble': {'slot': 'authority', 'name': __('Humble'), 'knowledge': 1},
        'slothful': {'slot': 'comfort', 'name': __('Slothful'), 'knowledge': 1},
        'diligent': {'slot': 'comfort', 'name': __('Diligent'), 'might': 1},
        'cruel': {'slot': 'communication', 'name': __('Cruel'), 'might': 1},
        'merciful': {'slot': 'communication', 'name': __('Merciful'), 'charisma': 1},
        'lustful': {'slot': 'eros', 'name': __('Lustful'), 'subtlety': 1},
        'chaste': {'slot': 'eros', 'name': __('Chaste'), 'knowledge': 1},
        'envious': {'slot': 'ambition', 'name': __('Envious'), 'subtlety': 1},
        'kind': {'slot': 'ambition', 'name': __('Kind'), 'charisma': 1},
        'greedy': {'slot': 'prosperity', 'name': __('Greedy'), 'knowledge': 1},
        'charitable': {'slot': 'prosperity', 'name': __('Charitable'), 'charisma': 1},
        'coward': {'slot': 'safety', 'name': __('Coward'), 'subtlety': 1},
        'zealous': {'slot': 'safety', 'name': __('Zealous'), 'might': 1},
    }

    core_homeworld_features = {
        'prehistoric': {'slot': 'homeworld', 'name': __('Prehistoric world'), 'might': 1, 'knowledge': -1},
        'industrial': {'slot': 'homeworld', 'name': __('Industrial world'), 'might': -1, 'knowledge': 1},
        'postapoc': {'slot': 'homeworld', 'name': __('Postapocalyptic world'), 'subtlety': 1, 'charisma': -1},
        'utopia': {'slot': 'homeworld', 'name': __('Utopic world'), 'subtlety': -1, 'charisma': 1},
    }

    core_family_features = {
        'orphan': {'slot': 'family', 'name': __('Orphan'), 'subtlety': 1, 'knowledge': -1},
        'matrial': {'slot': 'family', 'name': __('Matrial'), 'might': 1, 'subtlety': -1},
        'intelligent': {'slot': 'family', 'name': __('Intelligent'), 'might': -1, 'knowledge': 1},
        'highborn': {'slot': 'family', 'name': __('Highborn'), 'subtlety': -1, 'charisma': 1},
        'lowborn': {'slot': 'family', 'name': __('Lowborn'), 'subtlety': 1, 'charisma': -1},
    }

    core_profession_features = {
        'warrior': {'slot': 'profession', 'name': __('Warrior'), 'attribute': 'might', 'might': 1, 'knowledge': -1},
        'servant': {'slot': 'profession', 'name': __('Servant'), 'attribute': 'subtlety', 'subtlety': 1, 'charisma': -1},
        'scholar': {'slot': 'profession', 'name': __('Scholar'), 'attribute': 'knowledge', 'knowledge': 1, 'subtlety': -1},
        'artist': {'slot': 'profession', 'name': __('Artist'), 'attribute': 'charisma', 'charisma': 1, 'might': -1},
    }

    core_souls = {
        0: __('darksoul'),
        1: __('dimsoul'),
        2: __('firesoul'),
        3: __('soulblaze'),
        4: __('hellfire'),
        5: __('infernal'),
    }

    core_soul_weights = {
        5: 1,
        4: 2,
        3: 4,
        2: 8,
        1: 16
    }
