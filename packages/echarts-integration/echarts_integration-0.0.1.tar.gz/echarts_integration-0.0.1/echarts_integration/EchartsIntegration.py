# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class EchartsIntegration(Component):
    """An EchartsIntegration component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- option (dict; optional)
- notMerge (boolean; default False)
- notRefreshImmediately (boolean; default False)
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, onInit=Component.UNDEFINED, option=Component.UNDEFINED, notMerge=Component.UNDEFINED, notRefreshImmediately=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'option', 'notMerge', 'notRefreshImmediately', 'style']
        self._type = 'EchartsIntegration'
        self._namespace = 'echarts_integration'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'option', 'notMerge', 'notRefreshImmediately', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(EchartsIntegration, self).__init__(**args)
