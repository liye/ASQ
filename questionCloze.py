import sys
sys.path.append("/home/liye/github/Cornell-Conversational-Analysis-Toolkit/")

from convokit.text_processing import TextProcessor

QN_STARTS = {'why', 'how', 'am', 'is','are', 
             'do', 'does', 'did', 
             'can', 'could', 'should', 'would'}

class QuestionCloze(TextProcessor):
    """
    Transformer that separates questions from the utterances, 
    Returns the question-masked text and the identifid questions (with their position in the utterance). 
    
    This transformer can be configured with any custom question identification function that takes a sentence (or its parse) as input
    and outputs whether the sentence being a question.
    
    :param output_fields: name of attribute to output to, default to ['masked_text', 'questions']
    :param input_field: name of field to use as input. 
    :param qn_checker: an optional function to check for questions.  
    :param input_filter: a boolean function of signature `input_filter(utterance, aux_input)`. 
        Transformation will only be computed for utterances where `input_filter` returns `True`. 
        By default, will always return `True`.
    :param verbosity: frequency of status messages.
    """
    
    def __init__(self, output_field=['masked_text', 'questions'], \
                 input_field='parsed', qn_checker=None, \
                 input_filter=lambda utt, aux: True, verbosity=0):
    
        aux_input = {'qn_checker': qn_checker}

        super().__init__(proc_fn=self._seperate_qn_from_text, \
                         output_field=output_field, input_field=input_field, \
                         aux_input=aux_input, input_filter=input_filter, verbosity=verbosity)
    
    def _seperate_qn_from_text(self, text_entry, aux_input):
        
        is_question = aux_input['qn_checker'] if aux_input['qn_checker'] else qn_checker
        
        rest, qns = [], []
        for i, sent_parse in enumerate(text_entry):
            if is_question(sent_parse):
                qns.append((join_toks(sent_parse), i))
            else:
                rest.append(join_toks(sent_parse))
                
        return " ".join(rest), qns
    
    
def join_toks(sent_parse):
    return " ".join([tok['tok'] for tok in sent_parse['toks']])

def qn_checker(sent_parse, include_starts=QN_STARTS):
    
    if include_starts:
        if sent_parse['toks'][0]['tok'].lower() in include_starts:
            return True
        
    return sent_parse['toks'][-1]['tok']== "?"