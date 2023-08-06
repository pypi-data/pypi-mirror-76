# %%
# %% [markdown]
# https://rasa.com/docs/rasa/api/custom-nlu-components/
# If you create a custom tokenizer you should implement the methods of rasa.nlu.tokenizers.tokenizer.Tokenizer. The train and process methods are already implemented and you simply need to overwrite the tokenize method. train and process will automatically add a special token __CLS__ to the end of list of tokens, which is needed further down the pipeline.

# %%
import re
import os
from typing import Any, Dict, List, Optional, Text, Union, Type

# %%
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.training_data import Message, TrainingData

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

from rasa.nlu.config import RasaNLUModelConfig

import rasa.utils.io as io_utils
from rasa.nlu import utils
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata

# %%
from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer

# %%
import copy
import pickle

import numpy as np
import scipy.sparse

import stanza

# %%

class EntityNormalization(Component):
    def __init__(self, component_config: Dict[Text, Any] = None,) -> None:
        super(EntityNormalization, self).__init__(component_config)

    def normalize(self, message, entities=[]):
    
        tokens = message.get(TOKENS_NAMES[TEXT])

        entities = sorted(entities, key=lambda e:e['start'])

        for token in tokens:
            
            for e in entities:
                startbool = token.start >= e['start']
                endbool = token.end <= e['end']

                if startbool and endbool:
                    assert token.text in e['value']
                    token.text = e['entity'] if 'role' not in e else e['entity'] + '-' +e['role']
                    ## TODO
                    ## if e['start'] != token.start:
                    ## ## e['entity].replace('B-', 'I-')

                    # {'entity': 'B-DURATION',
                    # 'start': 0,
                    # 'end': 1,
                    # 'role': 'YEAR',
                    # 'value': '1',
                    # 'extractor': 'DIETClassifierExtended'},
                    pass

        message.set(TOKENS_NAMES[TEXT], tokens)

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for message in training_data.training_examples:
            entities = message.get('norm_ent')
            self.normalize(message, entities)            

    def process(self, message: Message, **kwargs: Any):

        entities = message.get(ENTITIES, [])
        entities = [e for e in entities if e['extractor'] in ['DIETClassifierExtended', 'DIETClassifier']]
        self.normalize(message, entities)


class EntityManager(Component):

    defaults = {
        "priority_config": {},
    }

    def __init__(
        self,
        component_config: Dict[Text, Any] = None,
    ) -> None:
        super(EntityManager, self).__init__(component_config)
        
        self.priority_config = self.component_config["priority_config"]
        self.priority_config = { float(k):v for k,v in self.priority_config.items()}
        self.priority_config = [self.priority_config[i].split('___',1) for i in sorted (self.priority_config.keys())]

        print('Entity Priority List')
        print(self.priority_config)
        # tempcount = 6
        # for i in range(len(self.priority_config)//tempcount +1):
        #     print(self.priority_config[ i*tempcount: (i+1)*tempcount ])
        pass
        
    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message."""

        if not self.priority_config:
            return

        entities = message.get("entities", [])
        entities_updated = copy.deepcopy(entities)
        
        temp = []
        for priority_i in self.priority_config:
            for entity in entities_updated:

                if [entity['extractor'], entity['entity']] == priority_i:
                    temp.append(entity)
                
        entities_updated = temp
        temp = []

        temp = []
        tempspan = []
        for entity in entities_updated:
            if not (entity['start'] in tempspan or entity['end'] in tempspan):
                temp.append(entity)
                tempspan.append(entity['start'])
                tempspan.append(entity['end'])

        entities_updated = temp
        temp = []
        
        message.set("entities", entities_updated, add_to_output=True)

        