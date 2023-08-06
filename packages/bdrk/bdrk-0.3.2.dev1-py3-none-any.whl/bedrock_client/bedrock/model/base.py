import json
from abc import abstractmethod
from typing import AnyStr, BinaryIO, List, Mapping, Optional, Union


class BaseModel:
    """
    All Models declared in serve.py should inherit from BaseModel.
    """

    def __init__(self, config: Optional[Mapping[str, str]] = None):
        # self.config contains logging and other settings
        self.config = config

    def pre_process(
        self, http_body: AnyStr, files: Optional[Mapping[str, BinaryIO]] = None
    ) -> List[float]:
        """
        Converts http_body (or files) to something that can be passed into predict()
        """
        array = json.loads(http_body)
        return [float(x) for x in array]

    def post_process(self, scores: Union[float, List[float]]) -> Union[float, List[float]]:
        """
        Any postprocessing of output from predict()
        """
        return scores

    @abstractmethod
    def predict(self, features: List[float]) -> Union[float, List[float]]:
        """
        Generate prediction based on self.model
        """
        raise NotImplementedError

    def validate(self, sample):
        """
        Checks that self.model is initialized.
        Run through all three steps and throws errors
        if anything is wrong.
        Also does type checking (might move to mypy).
        """
        processed_sample = self.pre_process(sample)
        # Check processed_sample is List[float]
        # Can also be List[List[float]] but assume former for now
        assert isinstance(processed_sample, list) and all(
            isinstance(f, float) for f in processed_sample
        ), "self.pre_process() should output List[float]"
        prediction = self.predict(processed_sample)

        if all(isinstance(f, float) for f in processed_sample):
            # If features is List[float], then prediction is Union[float, List[float]]
            assert isinstance(prediction, float) or (
                isinstance(prediction, list) and all(isinstance(p, float) for p in prediction)
            ), "self.predict() should output float or List[float]"
            processed_prediction = self.post_process(prediction)
            assert isinstance(processed_prediction, float) or (
                isinstance(processed_prediction, list)
                and all(isinstance(p, float) for p in processed_prediction)
            ), "self.post_process() should output float or List[float]"
        # TODO add assert for features of type List[List[float]]
