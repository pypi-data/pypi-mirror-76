from typing import Any, Dict, List, Optional, Text, Tuple, Union, Type, NamedTuple

import tensorflow as tf

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
            prediction_batch_size = self.component_config['prediction_batch_size']
            print(f'  Number of batches to be executed : {len(training_data.training_examples)//prediction_batch_size +1}')

            print_example_count = 5

            for i in range(len(training_data.training_examples)//prediction_batch_size +1):
                if i == len(training_data.training_examples)//prediction_batch_size:
                    print(f'  Last batch. Batch idx : {i}')
                elif i % 20 == 0:
                    print(f'  Batch idx : {i}')
                

                batch_data = training_data.training_examples[ i*prediction_batch_size: (i+1)*prediction_batch_size ]
                model_data = self._create_model_data(batch_data, training=False)
                batch_in = model_data.prepare_batch()
                out = self.model.batch_predict(batch_in)

                for k in out:
                    out[k] = out[k].numpy()

                for j, message in enumerate(batch_data):
                    outj = {k:tf.constant([out[k][j,:]]) for k in out}
                    entities = self._predict_entities(outj, message)
                    message.set('norm_ent', entities, )

                    if print_example_count != 0:
                        
                        # out = self._predict(message)
                        temp_model_data = self._create_model_data([message], training=False)
                        temp_out = self.model.predict(temp_model_data)
                        temp_entities = self._predict_entities(temp_out, message)

                        if entities != []:
                            print_example_count -= 1

                            print(message.text)
                            print()

                            print({k:outj[k].numpy() for k in outj})
                            print({k:temp_out[k].numpy() for k in temp_out})
                            print()

                            print(entities)
                            print(temp_entities)
                            print()

                    