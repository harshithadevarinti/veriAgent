from agents.decomposer import decompose

samples = [
    "Marie Curie won two Nobel Prizes and was born in Warsaw in 1867.",
    "The Eiffel Tower, which is in Paris, was completed in 1889. I think it's beautiful.",
    "Albert Einstein developed the theory of relativity. He also won the Nobel Prize in 1921.",
    "Python is a great language. It was created by Guido van Rossum.",
]

for s in samples:
    print("INPUT:", s)
    for c in decompose(s):
        print("  -", c)
    print()