from typing import Any, Dict, List, Optional, Text, Tuple, Union, Type, NamedTuple

from rasa.nlu.constants import INTENT
from rasa.utils.tensorflow.constants import ENTITY_RECOGNITION
from rasa.nlu.training_data import TrainingData
from rasa.nlu.training_data import Message
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.classifiers.diet_classifier import DIETClassifier

class DIETClassifierExtended(DIETClassifier):

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
    
        ## FILTER START
        intent_filters = self.component_config['intent_filters']
        print(f'Filter intents : {intent_filters}')
        
        if intent_filters:
            backup_training_data_training_examples = training_data.training_examples
            filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) in intent_filters]
            training_data.training_examples = filtered_training_examples

            print(f'    All example size : {len(backup_training_data_training_examples)}')
            print(f'    Filtered example size : {len(filtered_training_examples)}')
        ## FILTER END

        super().train(training_data, config, **kwargs)
        
        ## FILTER RECOVER START
        if intent_filters:
            training_data.training_examples = backup_training_data_training_examples

        ## FILTER RECOVER END

        ## GET ENTITY PREDICTIONS
        
        if self.component_config[ENTITY_RECOGNITION]:
            print('Predict entities for normalization.')
            for message in training_data.training_examples:
                out = self._predict(message)
                entities = self._predict_entities(out, message)

                # message.set(ENTITIES, entities, add_to_output=True)
                message.set('norm_ent', entities, )