COMMONS = """
2	Fox: 474
3	Koala: 42
4	Beetle: 39
5	Giraffe: 37
6	Frog: 37
7	Fish: 37
8	Pig: 37
9	Turkey: 36
10	Parrot: 35
11	Duck: 35
12	Penguin: 35
13	Chick: 34
14	Lizard: 34
15	Worm: 34
16	Spider: 34
17	Leopard: 33
18	Crab: 33
19	Whale: 33
20	Squid: 32
21	Skunk: 32
22	Deer: 31
23	Dove: 30
24	Cricket: 29
25	Hippo: 29
26	Crocodile: 29
27	Mouse: 29
28	Beaver: 28
29	Horse: 27
30	Shrimp: 26
31	Hedgehog: 26
32	Sheep: 25
33	Hamster: 25
34	Ox: 24
35	Seal: 23
36	Dog: 22
37	Sloth: 21
38	Elephant: 21
39	Gorilla: 21
40	Bat: 14
41	Zebra: 13
42	Bear: 12
43	Fly: 11
44	Rabbit: 10
45	Caterpillar: 9
46	Snail: 9
47	Dinosaur: 9
48	Camel: 9
49	Cow: 9
50	Chicken: 7
51	Cat: 5""".strip()

RARES = """
54	Rooster: 5
55	Bee: 5
56	Snake: 5
57	Owl: 4
58	Bactrian Camel: 4
59	Wolf: 3 (+quest)
60	Unicorn: 3
61	Dragon: 3
62	Ram: 2
63	Poodle: 2
64	Chipmunk: 2
65	Kangaroo: 2
66	Llama: 2
67	Dodo: 2
68	Monkey: 2
69	Bird: 2
70	Eagle: 2
71	Lion: 2
72	Butterfly: 2
73	Cockroach: 2
74	Ladybug: 2
75	Turtle: 2
76	Peacock: 2
77	Mosquito: 2
78	Jellyfish: 2
79	Swan: 2
80	Otter: 2
81	Lobster: 2
82	Flamingo: 2
83	Octopus: 2
84	Shark: 2
85	Rhino: 2
86	Pufferfish: 2
87	Dolphin: 2
88	Rat: 2
89	Scorpion: 2
90	Badger: 2
91	Moose: 2
92	Polar Bear: 2
93	Donkey: 2
94	Bunny: 2
95	Mammoth: 2
96	Orangutan: 2
97	Boar: 2
98	Bison: 2
99	Panda: 2
100	Goat: 2
101	Raccoon: 1
102	T-Rex: 1""".strip()

COMMONS = [x.split("\t")[1].split(":")[0].replace(":", "") for x in COMMONS.split("\n")]
RARES = [x.split("\t")[1].split(":")[0].replace(":", "") for x in RARES.split("\n")]

commons2 = [f"Animal(name={x.lower()!r}, displayname={x!r}, emoji=..., rare=False,)" for x in COMMONS]
rares2 = [f"Animal(name={x.lower()!r}, displayname={x!r}, emoji=..., rare=True,)" for x in RARES]

print(",\n".join(commons2))
print("------------------")
print(",\n".join(rares2))
