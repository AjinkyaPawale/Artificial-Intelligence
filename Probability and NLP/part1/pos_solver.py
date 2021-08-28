###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids: Ajinkya-Chaitanya-Shivani, ajpawale-cdeshpa-svogiral
#
# (Based on skeleton code by D. Crandall)
#


import random
from collections import Counter
import math



# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    def __init__(self):
        # transition probability
        self.dictionary_trans_prob = {}
        # emission probability
        self.dictionary_emmission_prob = {}
        # dictionary of word and pos
        self.dictionary_pos = {}
        # dictionary of word, pos and probability
        self.dict_bay_prob = {}
        # dictionary of word and pos , probability
        self.dict_rev_pos = {}
        # initiail probability
        self.initial_prob = {}
        # pos count in training data
        self.pos_count = {}
        # word count in training data
        self.word_count = {}
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            post_prb = 0.0
            for i in range(len(sentence)):
                if (sentence[i], label[i]) in self.dictionary_emmission_prob:
                    p = self.dictionary_emmission_prob[(sentence[i], label[i])]
                    post_prb += math.log(p)
                else:
                    post_prb += math.log(1e-24)
            return post_prb

        elif model == "HMM":
            posterior_prob = 0.0
            for i in range(len(sentence)):
                if (sentence[i], label[i]) in self.dictionary_emmission_prob:
                    p = self.dictionary_emmission_prob[(sentence[i], label[i])]
                    posterior_prob += math.log(p)
                else:
                    posterior_prob += math.log(1e-24)

            previous_pos = label[0]
            for i in range(1, len(label)):
                p = self.dictionary_trans_prob[(previous_pos, label[i])]
                posterior_prob += math.log(p)
                previous_pos = label[i]

            return posterior_prob

        elif model == "Complex":
            posterior_prob = 0.0

            for i in range(len(sentence)):
                if (sentence[i], label[i]) in self.dictionary_emmission_prob:
                    p = self.pos_count[label[i]] * self.dictionary_emmission_prob[(sentence[i], label[i])]
                    posterior_prob += math.log(p)
                else:
                    posterior_prob += math.log(1e-24)

            previous_pos = label[0]
            for i in range(1, len(label)):
                p = self.dictionary_trans_prob[(previous_pos, label[i])]
                posterior_prob += math.log(p)
                previous_pos = label[i]
            return posterior_prob
        else:
            print("Unknown algo!")

    # Do the training!
    def train(self, data):
        self.dictionary_pos = {'adj': [],
                         'adv': [],
                         'adp': [],
                         'conj': [],
                         'det': [],
                         'noun': [],
                         'num': [],
                         'pron': [],
                         'prt': [],
                         'verb': [],
                         'x': [],
                         '.': []}
        self.initial_prob = {'adj': 0,
                          'adv': 0,
                          'adp': 0,
                          'conj': 0,
                          'det': 0,
                          'noun': 0,
                          'num': 0,
                          'pron': 0,
                          'prt': 0,
                          'verb': 0,
                          'x': 0,
                          '.': 0}
        self.dictionary_trans_prob = {}

        self.pos_count = {'adj': 0,
                          'adv': 0,
                          'adp': 0,
                          'conj': 0,
                          'det': 0,
                          'noun': 0,
                          'num': 0,
                          'pron': 0,
                          'prt': 0,
                          'verb': 0,
                          'x': 0,
                          '.': 0}

        count = 0

        for mod in data:
            for pos in mod[1]:
                self.pos_count[pos] += 1
                count += 1
            for word in mod[0]:
                if word in self.word_count:
                    self.word_count[word] += 1
                else:
                    self.word_count[word] = 1

        for pos in self.pos_count:
            self.pos_count[pos] /=count

        for word in self.word_count:
            self.word_count[word] /=count


        for mod in data :
            if len( mod[ 1 ] ) > 1 :
                for i in range(0,len( mod[ 1 ])-1) :
                    prev = mod[ 1 ][ i ]
                    nextt = mod[ 1 ][ i + 1 ]
                    self.initial_prob[ prev ] += 1
                    if ( prev , nextt ) not in self.dictionary_trans_prob:
                        self.dictionary_trans_prob.update( { ( prev , nextt ) : 1 } )
                    else:
                        self.dictionary_trans_prob[ ( prev , nextt ) ] += 1
                    self.dictionary_pos[ mod[ 1 ][ i ] ].append( mod[ 0 ][ i ] )
                self.initial_prob[mod[1][i + 1]] += 1
                self.dictionary_pos[mod[1][i + 1]].append(mod[0][i + 1])

        total_init_prob = sum(self.initial_prob.values())

        for mod in self.initial_prob.keys():
            self.initial_prob[mod] /= total_init_prob

        for mod in data:
            for i in range(len(mod[0])):
                if mod[0][i] not in self.dict_rev_pos:
                    self.dict_rev_pos[mod[0][i]] = [mod[1][i]]
                else:
                    self.dict_rev_pos[mod[0][i]].append(mod[1][i])

        total = sum(self.dictionary_trans_prob.values())
        for i in self.dictionary_trans_prob:
            self.dictionary_trans_prob[i] = (float(self.dictionary_trans_prob[i] / total))

        for pos, words in self.dictionary_pos.items():
            total = 0
            count = Counter(words)
            count = Counter(th for th in count.elements())
            for elem, co in count.items():
                total += co
            for elem, co in count.items():
                self.dictionary_emmission_prob.update({(elem, pos): co / total})

        for word, pos in self.dict_rev_pos.items():
            total = 0
            counts = Counter(pos)
            counts = Counter(th for th in counts.elements())
            for elem, co in counts.items():
                total += co
            for elem, co in counts.items():
                if word not in self.dict_bay_prob:
                    self.dict_bay_prob.update({word: [[co / total, elem]]})
                else:
                    self.dict_bay_prob[word].append([co / total, elem])
        pos = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']

        tem = []
        for j in pos:
            for i in pos:
                tem.append((i,j))
        lis = list(self.dictionary_trans_prob)
        diff = list(set(tem)-set(lis))
        tp_min = min(self.dictionary_trans_prob.values())
        for i in diff:
            self.dictionary_trans_prob[i] = tp_min/20.0
        pass



    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    def simplified(self, sentence):
        res = []
        for word in list(sentence):
            if word in self.dict_rev_pos:
                tem = []
                for mod in self.dict_bay_prob[word]:
                    tem.append(mod[0])
                res.append(self.dict_bay_prob[word][tem.index(max(tem))][1])
            else:
                res.append('x')
        return res

    def hmm_viterbi(self, sentence):
        cur_dist  = {'adj': [],
                     'adv': [],
                     'adp': [],
                     'conj': [],
                     'det': [],
                     'noun': [],
                     'num': [],
                     'pron': [],
                     'prt': [],
                     'verb': [],
                     'x': [],
                     '.': []}

        pos     = ['adj',
                  'adv',
                  'adp',
                  'conj',
                  'det',
                  'noun',
                  'num',
                  'pron',
                  'prt',
                  'verb',
                  'x',
                  '.']

        res = []
        previous_pos = ''

        z = {'adj': None,
             'adv': None,
             'adp': None,
             'conj': None,
             'det': None,
             'noun': None,
             'num': None,
             'pron': None,
             'prt': None,
             'verb': None,
             'x': None,
             '.': None}
        word = list(sentence)[0]
        p=0.0

        for mod in pos:
            if (word, mod) in self.dictionary_emmission_prob:
                p = self.dictionary_emmission_prob[(word, mod)] * self.initial_prob[mod]
                cur_dist[mod].append(("noun", p))
            else:
                cur_dist[mod].append(("noun", 1e-8))

        res.append(previous_pos)

        for word in list(sentence)[1:]:
            t = z
            for mod in pos:
                max_p = 0.0
                for previous_pos, prev_prob in cur_dist.items():
                    if (word, mod) in self.dictionary_emmission_prob:
                        tem = prev_prob[-1][1] * self.dictionary_emmission_prob[(word, mod)] * self.dictionary_trans_prob[(previous_pos, mod)]
                        if max_p < tem:
                            max_p = tem
                            new_pos = previous_pos
                if max_p == 0.0:
                    for previous_pos, prev_prob in cur_dist.items():
                        tem = prev_prob[-1][1] * self.dictionary_trans_prob[(previous_pos, mod)] * 5e-7
                        if max_p < tem:
                            max_p = tem
                            new_pos = previous_pos
                t[mod] = (new_pos, max_p)
            for i, j in t.items():
                cur_dist[i].append(j)

        max_p = 0.0
        t_pos = ""
        temp = ""
        for mod, word in cur_dist.items():
            if (max_p < word[-1][1]):
                max_p = word[-1][1]
                t_pos = word[-1][0]
                temp = mod

        max_p = 0.0
        res = []
        if not temp:
            temp = 'noun'
        res.append(temp)
        if not t_pos:
            max_p = 0.0
            for mod in pos:
                if max_p < self.dictionary_trans_prob[(res[-1], mod)]:
                    max_p = self.dictionary_trans_prob[(res[-1], mod)]
                    t_pos = mod

        res.append(t_pos)

        for i in range(len(sentence) - 2, 0, -1):
            if t_pos:
                t_pos = cur_dist[t_pos][i][0]
            else:
                max_p = 0.0
                for mod in pos:
                    if max_p < self.dictionary_trans_prob[res[-1]][mod]:
                        max_p = self.dictionary_trans_prob[res[-1]][mod]
                        t_pos = pos

            res.append(t_pos)
        res.reverse()
        return res[:len(sentence)]

    def complex_mcmc(self, sentence):
        res = ["noun"] * len(sentence)
        pos = ['adj',
                  'adv',
                  'adp',
                  'conj',
                  'det',
                  'noun',
                  'num',
                  'pron',
                  'prt',
                  'verb',
                  'x',
                  '.']
        bias_prob = []

        for word in list(sentence):
            temp = []
            for mod in pos:
                if (word, mod) in self.dictionary_emmission_prob:
                    temp.append(self.dictionary_emmission_prob[(word, mod)])
                else:
                    temp.append(2.0)

            min_temp = min(temp)

            for i in range(len(temp)):
                if temp[i] == 2.0:
                    temp[i] = min_temp * 1e-12
            total = sum(temp)

            for i in range(len(temp)):
                temp[i] /= total
            x = 0.0
            for i in range(len(temp)):
                x += temp[i]
                temp[i] = x
            bias_prob.append(temp)

        res = []

        l = 0
        for l in range(len(sentence)):
            j = 20000
            res.append([])
            while (j > 0):
                j -= 1
                ran = random.random()
                for i in range(12):
                    if (ran <= bias_prob[l][i]):
                        res[l].append(pos[i])
                        break

        sol = []
        for mod in res:
            sol.append(mod[-1])
            # sol.append( max([(elem.count(chr),chr) for chr in set(elem)])[ 1 ] )
        return sol



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
