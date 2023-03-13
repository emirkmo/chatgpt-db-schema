from pydantic import Field
from pydantic.dataclasses import dataclass

from idd_ai.contracts import make_contract


@dataclass
class AddStats:
    add_detections: int = Field(
        description="total number of audio distortions detected."
    )
    add_detection_class: str = Field(description="Audo distortion detected class.")
    add_classes: str = Field(
        description="comma separated list of distortion classes. For example: 'Transients, Spikes'."
    )
    add_transients_count: int = Field(
        description="Total number of Transients detected, in counts."
    )
    add_spikes_count: float = Field(
        description="Total number of spikes detected, in counts."
    )


contract = make_contract(
    AddStats.__pydantic_model__,  # type: ignore
    description="Audio distortion detection stats from the microphones of our cameras.",
)


@dataclass
class AudioDistortionDetectionStats:
    total_distortion_detections: int = Field(
        description="total number of audio distortions detected."
    )
    distortion_detection_class: str = Field(
        description="Audo distortion detected class."
    )
    distortion_classes: str = Field(
        description="Comma separated list of distortion classes. For example: 'Transients, Spikes'."
    )
    total_transients_count: int = Field(
        description="Total number of Transients detected, in counts."
    )
    total_spikes_count: int = Field(
        description="Total number of spikes detected, in counts."
    )
    timestamp: str = Field(
        description="String formatteed timestamp at date and time of the distortion detection."
    )
    camera_id: int = Field(
        description="ID of the camera that generated the audio data."
    )


fixed_contract = make_contract(
    AudioDistortionDetectionStats.__pydantic_model__,  # type: ignore
    description="Audio distortion detection stats from the microphones of our cameras.",
)
