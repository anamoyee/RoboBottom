COMMONS = """
🦊 474⨯ Fox
🪱 34⨯ Worm
🪲 39⨯ Beetle
🦎 34⨯ Lizard
🐟 37⨯ Fish
🐸 37⨯ Frog
🦒 37⨯ Giraffe
🐨 42⨯ Koala
🐷 37⨯ Pig
🦃 36⨯ Turkey
🦆 35⨯ Duck
🦜 35⨯ Parrot
🐧 35⨯ Penguin
🐥 34⨯ Chick
🕷️ 34⨯ Spider
🦀 33⨯ Crab
🐆 33⨯ Leopard
🐳 33⨯ Whale
🐴 27⨯ Horse
🦨 32⨯ Skunk
🦑 32⨯ Squid
🦌 31⨯ Deer
🕊️ 30⨯ Dove
🦗 29⨯ Cricket
🐊 29⨯ Crocodile
🦛 29⨯ Hippo
🐭 29⨯ Mouse
🦫 28⨯ Beaver
🦔 26⨯ Hedgehog
🦐 26⨯ Shrimp
🐹 25⨯ Hamster
🐑 25⨯ Sheep
🦇 14⨯ Bat
🐂 24⨯ Ox
🐌 9⨯ Snail
🦭 23⨯ Seal
🐔 7⨯ Chicken
🐶 22⨯ Dog
🐘 21⨯ Elephant
🦍 21⨯ Gorilla
🦥 21⨯ Sloth
🐪 9⨯ Camel
🦓 13⨯ Zebra
🐻 12⨯ Bear
🪰 11⨯ Fly
🐰 10⨯ Rabbit
🐛 9⨯ Caterpillar
🐄 9⨯ Cow
🦕 9⨯ Dinosaur
🐱 5⨯ Cat
""".strip()  # noqa: RUF001

RARES = """
🐺 3⨯ Wolf
🐍 5⨯ Snake
🐞 2⨯ Ladybug
🐲 3⨯ Dragon
🪼 2⨯ Jellyfish
🐢 2⨯ Turtle
🦘 2⨯ Kangaroo
🦝 1⨯ Raccoon
🐗 2⨯ Boar
🦤 2⨯ Dodo
🦢 2⨯ Swan
🦚 2⨯ Peacock
🐻‍❄️ 2⨯ Polar Bear
🐦 2⨯ Bird
🦂 2⨯ Scorpion
🦞 2⨯ Lobster
🦁 2⨯ Lion
🦈 2⨯ Shark
🦄 3⨯ Unicorn
🦡 2⨯ Badger
🐙 2⨯ Octopus
🫎 2⨯ Moose
🦅 2⨯ Eagle
🪳 2⨯ Cockroach
🐡 2⨯ Pufferfish
🦏 2⨯ Rhino
🐀 2⨯ Rat
🦦 2⨯ Otter
🫏 2⨯ Donkey
🦩 2⨯ Flamingo
🐿️ 2⨯ Chipmunk
🐏 2⨯ Ram
🦉 4⨯ Owl
🦬 2⨯ Bison
🐝 5⨯ Bee
🐬 2⨯ Dolphin
🐓 5⨯ Rooster
🐩 2⨯ Poodle
🦣 2⨯ Mammoth
🦧 2⨯ Orangutan
🐒 2⨯ Monkey
🐫 4⨯ Bactrian Camel
🦙 2⨯ Llama
🐼 2⨯ Panda
🦟 2⨯ Mosquito
🐇 2⨯ Bunny
🦋 2⨯ Butterfly
🐐 2⨯ Goat
🦖 1⨯ T-Rex
🐯 1⨯ Tiger
""".strip()  # noqa: RUF001

COMMONS = [x.split("⨯")[1].strip() for x in COMMONS.split("\n")]  # noqa: RUF001
RARES = [x.split("⨯")[1].strip() for x in RARES.split("\n")]  # noqa: RUF001

from tcrutils.console import c

d = dict(zip(COMMONS, RARES, strict=True))

s = ",\n".join(f"ANIMAL_{common.upper()}: ANIMAL_{rare.upper().replace('-', '')}" for common, rare in d.items())

print(s)
