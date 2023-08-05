# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Keyboard(Component):
    """A Keyboard component.
The Keyboard component listens for keyboard events.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- eventProps (list of strings; default ["key", "altKey", "ctrlKey", "shiftKey","metaKey", "repeat"]): The event properties to forward to dash, see https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent.
- captureKeys (list of strings; optional): The keys to capture. Defaults to all keys.
- keydown (dict; optional): The ID used to identify this component in Dash callbacks."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, eventProps=Component.UNDEFINED, captureKeys=Component.UNDEFINED, keydown=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'eventProps', 'captureKeys', 'keydown']
        self._type = 'Keyboard'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'eventProps', 'captureKeys', 'keydown']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Keyboard, self).__init__(**args)
