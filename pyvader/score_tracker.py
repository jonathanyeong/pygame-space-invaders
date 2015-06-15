import csv
from datetime import date
import sys

class ScoreTracker:
    def __init__(self):
        pass

    def top_five(self):
        # Top five scores
        pass
    
    def save_score(self, score):
        # Save score to text file/database?
        f = open('high_scores.csv', 'w+')
        print "writing score"
        try:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(('Score', 'Date'))
            writer.writerow((score, date.today()))
        finally:
            f.close()
        print "finished writing score"
    
    def read_score(self):
        # Read score is probably going to be used for
        # showing the top five scores
        pass
