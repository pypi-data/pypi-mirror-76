from typing import List
from functools import reduce


SOIL_TEXTURE_IDS = ['sandContent', 'siltContent', 'clayContent']


def group_measurements_depth(measurements: List[dict]):
    def group_by(group: dict, measurement: dict):
        key = measurement['depthUpper'] + measurement['depthLower'] \
            if 'depthUpper' in measurement and 'depthLower' in measurement else 'default'
        if key not in group:
            group[key] = []
        group[key].extend([measurement])
        return group

    return reduce(group_by, measurements, {})


def validate_soilTexture(measurements: List[dict]):
    def validate(values):
        values = list(filter(lambda v: v['term']['@id'] in SOIL_TEXTURE_IDS, values))
        terms = list(map(lambda v: v['term']['@id'], values))
        return len(set(terms)) != len(SOIL_TEXTURE_IDS) or 99.5 < sum(map(lambda v: v['value'], values)) < 100.5 or {
            'level': 'error',
            'key': 'measurements',
            'message': 'The sum of Sand, Silt, and Clay content should equal 100% for each soil depth interval.'
        }

    results = list(map(validate, group_measurements_depth(measurements).values()))
    return next((x for x in results if x is not True), True)


def validate_site(site: dict):
    return [
        validate_soilTexture(site['measurements'])
    ]
