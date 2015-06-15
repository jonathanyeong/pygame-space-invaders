import csv
import os
from datetime import date
import sys

class ScoreTracker:
    def __init__(self):
        pass

    def top_five(self):
        scores = self.read_score()
        if scores is None:
            return scores
        scores = map(int, scores)
        if scores.count < 5:
            return scores
        scores.sort(reverse=True)
        return scores[:5]

    def save_score(self, score):
        # Save score to text file/database?
        f = open('high_scores.csv', 'a')
        print "writing score"
        try:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow((score, date.today()))
        finally:
            f.close()
        print "finished writing score"
    
    def read_score(self):
        score_list = []
        if os.path.isfile('high_scores.csv'):
            f = open('high_scores.csv', 'r')
            try:
                reader = csv.reader(f)
                for row in reader:
                    score_list.append(row[0])
            finally:
                f.close()
        else:
            score_list = None
        return score_list
