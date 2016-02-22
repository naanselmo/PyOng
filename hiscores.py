import operator


class Hiscores:
    TOKEN = ';;'

    def __init__(self, filename):
        self.filename = filename

    def add_score(self, name, score):
        hiscores_file = open(self.filename, 'a+')
        hiscores_file.write('\n' + name + Hiscores.TOKEN + str(score))
        hiscores_file.close()

    def get_scores(self, limit):
        hiscores_file = open(self.filename)
        scores = []
        for line in hiscores_file.readlines():
            name, score = line.split(Hiscores.TOKEN)
            scores.append((name, int(score)))
        hiscores_file.close()
        scores.sort(key=operator.itemgetter(1), reverse=True)
        return scores[:limit]

    def get_hiscore(self):
        return self.get_scores(1)[0]
