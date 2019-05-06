

acquisition_schema = {
    '$schema': 'http://json-schema.org/schema#',
    '$id': 'RSoXS Acquisition',
    'type': 'object',
    'properties': {
        'plan_name': {'type': 'string'},
        'detectors': {'type': 'array',
                       'items': [{'type': 'string'}]},
        'motors': {'type': 'array',
                    'items': [{'type': 'string'}]},
        'positions': {'type': 'array',
                       'items': [{'type': 'number'}]},
        'display': {'type': 'string','enum': ["private", "public"]},
        'favorite': {'type': 'boolean'},
        'creator_ID': {'type': 'number'}
    },
    'required': ['plan_name', 'motors', 'positions', 'display', 'favorite']
}

configuration_schmea = {
    '$schema': 'http://json-schema.org/schema#',
    '$id': 'RSoXS configuration',
    'type': 'object',
    'properties': {
        'plan_name': {'type': 'string'},
        'motors': {'type': 'array',
                   'items': [{'type': 'string'}]},
        'positions': {'type': 'array',
                      'items': [{'type': 'number'}]},
        'display': {'type': 'string','enum': ["private", "public"]},
        'favorite': {'type': 'boolean'},
        'creator_ID': {'type': 'number'}
    },
    'required': ['plan_name', 'motors', 'positions', 'display', 'favorite']
}

location_schema = {
    '$schema': 'http://json-schema.org/schema#',
    '$id': 'RSoXS location',
    'type': 'object',
    'properties': {
        'location_list': {'type':'array',
                          'items': [{'type': 'object',
                                     'properties': {'motor_name': {'type': 'string'},
                                                  'position': {'type': 'number'}
                                                  },
                                     'required': ['motor_name', 'position']
                                     }
                                    ],
                          'minItems': 1
                          },
        'display': {'type': 'string', 'enum': ["private", "public"]},
        'favorite': {'type': 'boolean'},
        'creator_ID': {'type': 'number'}
    },
    'required': ['location_list', 'display', 'favorite']
}

sample_schema = {
    '$schema': 'http://json-schema.org/schema#',
    '$id': 'RSoXS Sample',
    'type': 'object',

    'properties': {
        'sample_name': {'type': 'string'},
        'sample_desc': {'type': 'string'},
        'date_created': {'type': 'string', 'format': 'date'},
        'user_id': {'type': 'number'},
        'project_name': {'type': 'string'},
        'institution_id': {'type': 'number'},
        'composition': {'type': 'array'},
        'density': {'type': 'number'},
        'thickness': {'type': 'number'},
        'notes': {'type': 'string'},
        'state': {'type': 'string','enum': ["loaded", "fresh", "broken", "lost", "unloaded"]},
        'current_bar_id': {'type': 'number'},
        'current_slot_name': {'type': 'string'},
        'past_bar_ids':{'type': 'array'},
        'location': {'$ref': '#/definitions/location'},
        'collections': {'type': 'array',
                        'uniqueItems': True,
                        'items': [{'type': 'object',
                                   'properties': {'configuration': {'$ref': 'RSoXS configuration'},
                                                  'acquisition': {'$ref': 'RSoXS acquisition'},
                                                  'location': {'$ref': 'RSoXS location'}
                                                  },
                                   'required': ['configuration', 'acquisition']
                                   }
                                  ]
                        }
        },
    'required': ['sample_name',
                 'date_created',
                 'user_id',
                 'project_name',
                 'institution_id',
                 'notes',
                 'state',
                 'location',
                 'current_bar_id',
                 'current_slot_name',
                 'collections']
    }

holder_schema = {
    '$schema': 'http://json-schema.org/schema#',
    '$id': 'RSoXS holder',
    'type': 'object',

    'properties': {
        'holder_id': {'type': 'number'},
        'primary_user_id': {'type': 'number'},
        'primary_institution_id': {'type': 'number'},
        'primary_proposal_id': {'type': 'number'},
        'date_loaded_list': {'type': 'array', 'items': [{'type': 'string', 'format': 'date'}]},
        'notes': {'type': 'string'},
        'slots': {'type': 'array',
                  'uniqueItems': True,
                  'items': [{'type': 'object',
                             'properties': {'location': {'$ref': 'RSoXS location'},
                                            'slot_name': {'type': 'string'},
                                            },
                             'required': ['location', 'slot_name']
                             }
                            ]
                  }
        },
    'required': ['holder_id',
                 'primary_user_id',
                 'primary_institution_id',
                 'primary_proposal_id',
                 'date_loaded_list',
                 'notes',
                 'location',
                 'slots']
    }

user_schema = {
    '$schema': 'http://json-schema.org/schema#',
    '$id': 'RSoXS User',
    'type': 'object',

    'properties': {
        'user_id': {'type': 'number'},
        'username': {'type': 'string'},
        'last_checkin': {'type': 'string','format': 'date'},
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string'},
        'phone': {'type': 'string'},
        'institution_id': {'type': 'number'},
        'proposal_id': {'type': 'number'},
        'date_checkin_list': {'type': 'array', 'items': [{'type': 'string', 'format': 'date'}]},
        'past_institutions': {'type' : 'array', 'items': [{'type': 'number'}]},
        'past_proposals': {'type': 'array', 'items': [{'type': 'number'}]},
        'notes': {'type': 'string'},
    },
    'required': ['user_id',
                 'username',
                 'email',
                 'first_name',
                 'last_name',
                 'last_checkin',
                 'institution_id',
                 'proposal_id',
                 'date_checkin_list',
                 'past_institutions']
}

Institution_schema = {
    '$schema': 'http://json-schema.org/schema#',
    '$id': 'RSoXS Institution',
    'type': 'object',

    'properties': {
        'institution_id': {'type': 'number'},
        'full_name': {'type': 'string'},
        'short_name': {'type': 'string'},
        'notes': {'type': 'string'},
    },
    'required': ['institution_id',
                 'full_name',
                 'short_name']
}
