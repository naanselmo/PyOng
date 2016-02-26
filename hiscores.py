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
            hiscores_file = open(self.filename)
            self.scores = []
            for line in hiscores_file.readlines():
                name, score = line.split(Hiscores.TOKEN)
                self.scores.append(Score(name, int(score)))
            hiscores_file.close()
            self.scores.sort(key=lambda score: score.score, reverse=True)
        return self.scores[:limit]

    def get_hiscore(self):
        return self.get_scores(1)[0]


class Score:
    def __init__(self, name, score):
        self.name = name
        self.score = score
