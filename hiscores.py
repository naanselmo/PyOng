class Hiscores:
    TOKEN = ';;'

    def __init__(self, filename):
        self.filename = filename
        self.scores = None

    def add_score(self, name, score):
        # Write in cache
        if self.scores is not None:
            self.scores.append(Score(name, score))
            self.scores.sort(key=lambda score: score.score, reverse=True)

        # Write in file
        hiscores_file = open(self.filename, 'a+')
        hiscores_file.write('\n' + name + Hiscores.TOKEN + str(score))
        hiscores_file.close()

    def get_scores(self, limit):
        # If not cached, fetch it and cache it
        if self.scores is None:
            hiscores_file = open(self.filename, 'a+')
            self.scores = []
            for line in hiscores_file.readlines():
                name, score = line.split(Hiscores.TOKEN)
                self.scores.append(Score(name, int(score)))
            hiscores_file.close()
            self.scores.sort(key=lambda score: score.score, reverse=True)

        if not self.scores:
            self.create_hiscores()

        return self.scores[:limit]

    def get_hiscore(self):
        return self.get_scores(1)[0]

    def create_hiscores(self):
        # Open the file
        hiscores_file = open(self.filename, 'a+')

        first = True
        for p in [Score("Linus Torvalds", 100),
        Score("Richard Stallman", 50),
        Score("Grace Hopper", 40),
        Score("Alan Turing", 30),
        Score("Dennis Ritchie", 25),
        Score("Ada Lovelace", 20),
        Score("Ken Thompson", 15),
        Score("Nuno Anselmo", 10),
        Score("Andre Mendes", 10)]:

            if self.scores is not None:
                self.scores.append(Score(p.name, p.score))
                self.scores.sort(key=lambda score: score.score, reverse=True)

            if first:
                hiscores_file.write(p.name + Hiscores.TOKEN + str(p.score))
                first = False
            else:
                hiscores_file.write('\n' + p.name + Hiscores.TOKEN + str(p.score))

        hiscores_file.close()

class Score:
    def __init__(self, name, score):
        self.name = name
        self.score = score
