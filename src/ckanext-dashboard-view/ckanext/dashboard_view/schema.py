schema = {
    "columns": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "column_name": {"type": "string"},
                "visualization_type": {
                    "enum": ["pie", "bar", "scatter", "number"]
                },
                "width": {
                    "type": "string",
                    "enum": ["25%", "50%", "75%", "100%"],
                    "default": "100%",
                },
                "options": {
                    "type": "object",
                    "oneOf": [
                        {
                            "properties": {
                                "group_by": {"type": "string"},
                                "value_type": {
                                    "enum": ["percentage", "total"]
                                },
                            },
                            "required": ["group_by", "value_type"],
                        },
                        {
                            "properties": {
                                "x_axis": {"type": "string"},
                                "y_axis": {"type": "string"},
                            },
                            "required": ["x_axis", "y_axis"],
                        },
                        {
                            "properties": {
                                "aggregation_type": {
                                    "enum": ["min", "max", "total", "average"]
                                }
                            },
                            "required": ["aggregation_type"],
                        },
                    ],
                },
            },
            "required": [
                "column_name",
                "visualization_type",
                "width",
                "options",
            ],
        },
    }
}
