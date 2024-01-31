import os
import typing
from typing import Any, Optional, Text, Dict, List, Type

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message

from serpapi import GoogleSearch

# from spellchecker import SpellChecker
# spell = SpellChecker()

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class SpellChecker(Component):
    """A component for correcting common typography errors using SERPAPI"""

    name = "Spell_checker"
    provides = ["message"]
    requires = ["message"]

    # Which components are required by this component.
    # Listed components should appear before the component itself in the pipeline.
    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        """Specify which components need to be present in the pipeline."""

        return []

    # Defines the default configuration parameters of a component
    # these values can be overwritten in the pipeline configuration
    # of the model. The component should choose sensible defaults
    # and should be able to create reasonable results with the defaults.
    defaults = {}

    # Defines what language(s) this component can handle.
    # This attribute is designed for instance method: `can_handle_language`.
    # Default value is None which means it can handle all languages.
    # This is an important feature for backwards compatibility of components.
    supported_language_list = ["en"]

    # Defines what language(s) this component can NOT handle.
    # This attribute is designed for instance method: `can_handle_language`.
    # Default value is None which means it can handle all languages.
    # This is an important feature for backwards compatibility of components.
    not_supported_language_list = None

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Train this component.

        This is the components chance to train itself provided
        with the training data. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`components.Component.pipeline_init`
        of ANY component and
        on any context attributes created by a call to
        :meth:`components.Component.train`
        of components previous to this one."""
        pass

    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message.

        This is the components chance to process an incoming
        message. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`components.Component.pipeline_init`
        of ANY component and
        on any context attributes created by a call to
        :meth:`components.Component.process`
        of components previous to this one."""


        """ Using pyspellchecker will result in correcting Nouns - bigger problem"""
        # print("inside spell checker, before conversion")
        # print(message.data)
        # if "text" in message.data:
        #     text_data = (message.data['text']).split()
        #     print("Before correction :- \n", text_data)
        #     reformed_data = ' '.join(spell.correction(word) for word in text_data)
        #     message.data['text'] = reformed_data
        #     print("After correction :- \n", message.data['text'].split())

        # print("After checking")
        # print(message.data)

        """ 
            SERPAPI - it does a basic google search and replaces the text 
            with google suggested correction 
        """    
        # SERPAPI_API_KEY = os.environ.get('BACKUP_SERPAPI_API_KEY')
        # if "text" in message.data:
        #     text_data = (message.data['text'])
        #     try:
        #         search = GoogleSearch({
        #             "q": text_data, 
        #             "api_key": SERPAPI_API_KEY
        #         })
        #         result = search.get_dict()
        #         corrected_text = result["search_information"]["spelling_fix"]
        #         message.data['text'] = corrected_text
        #     except:
        #         print("Exception occured in spell-checker.py - Continued running the process")
        

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        pass

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Text,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        """Load this component from file."""

        if cached_component:
            return cached_component
        else:
            return cls(meta)
