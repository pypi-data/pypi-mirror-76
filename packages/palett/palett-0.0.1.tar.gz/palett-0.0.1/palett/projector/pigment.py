from palett.presets import PLANET
from palett.projector.projector import to_projector
from palett.projector.utils.bound_to_leap import bound_to_leap
from palett.projector.utils.preset_to_flat import preset_to_flat
from intype import is_numeric


def pigment(bound, preset=PLANET, effects=[]):
    vleap = bound_to_leap(bound)
    prime = preset_to_flat(preset)
    projector = to_projector(vleap, preset, effects)
    return lambda x: projector(x)(x) if is_numeric(x) else prime(x)
