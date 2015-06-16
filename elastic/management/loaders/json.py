''' Loader for JSON data. '''
import json
from elastic.management.loaders.loader import JSONLoader
from elastic.management.loaders.mapping import MappingProperties


class JsonManager(JSONLoader):
    ''' Assumes the 'mapping' is given and there is a list of 'docs'.
    {
       "mapping": {"properties": {...}},
       "docs": [...]
    }
    '''

    def load_json(self, **options):
        ''' Create index mapping and load data '''
        idx_name = self.get_index_name(**options)
        idx_type = self.get_index_type('marker', **options)

        with open(options['indexJson']) as data_file:
            json_data = json.load(data_file)

        self._create_json_mapping(idx_type, json_data["mapping"], **options)
        self.load(json_data["docs"], idx_name, idx_type)

    def _create_json_mapping(self, idx_type, mapping, **options):
        ''' Create the mapping for indexing '''
        props = MappingProperties(idx_type)
        props.mapping_properties[idx_type].update(mapping)
        self.mapping(props, idx_type, **options)
