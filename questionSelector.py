from convokit.text_processing import TextProcessor

BLOCKLIST = ["opinion", "recommendation", "suggestion", "tip", "option", \
             "opinions", "recommendations", "suggestions", "tips", "options", 
             "suggest", "recommend", "please", "hell", "heck"]

VALID_STARTS = {'what','when','why','where','which','who','whom','whose', \
                'how','am','is','are','was','were',\
                'do','does','did','has','have','had',\
                'can','could','shall','should','will','would','may','might','must', \
                'any', 'anyone', 'help', 'advice', 'thoughts'}

class QuestionSelector(TextProcessor):
    
    def __init__(self, output_field=['sel_question', 'sel_question_pos'], \
                 input_field='questions', min_len=5, max_len=20, \
                 word2idf={}, min_score=5, start_set=VALID_STARTS, \
                 input_filter=lambda utt, aux: True, verbosity=0):
    
        # block words
        for word in BLOCKLIST:
            word2idf[word] = 0
            
        aux_input = {'min_len': min_len, 'max_len':max_len, \
                     'word2idf': word2idf, 'min_score':min_score, 'start_set':start_set}

        super().__init__(proc_fn=self._qn_selector, \
                         output_field=output_field, \
                         input_field= input_field, aux_input=aux_input, \
                         input_filter=input_filter, verbosity=verbosity)

    def _qn_selector(self, qns, aux_input):

        min_len, max_len = aux_input['min_len'], aux_input['max_len']
        word2idf, min_score = aux_input['word2idf'], aux_input['min_score']
        start_set = aux_input['start_set']

        curr_max = 0
        sel_qn, sel_pos = None, None

        # qns are inserted sequentially (i.e., sorted by pos)
        for qn, pos in qns:
            qn_toks = qn.split()
            qn_len = len(qn_toks)
            if qn_toks[0] not in start_set or qn_toks[-1] != "?" or qn_len <= min_len or qn_len >= max_len:
                continue
            score = max([word2idf[tok] for tok in qn_toks[1:]])
            if score > curr_max and score > min_score:
                sel_qn, sel_pos = qn, pos
                max_score = score

        return sel_qn, sel_pos