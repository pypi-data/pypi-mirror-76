import inspect

class EventHandler:
    def __init__(self, event_names):
        self._events = {
            event_name: Event(event_name)
            for event_name in event_names
        }
        self._function_tag_name = '_events'
    
    def run(self, event_name):
        event = self._get_event(event_name)
        event.run()
        
    def subscribe_tagged_methods(self, object):
        for method_name in dir(object):
            method = getattr(object, method_name)
            event_names = getattr(method, self._function_tag_name, [])
            for event_name in event_names:
                self._get_event(event_name).subscribe_function(method)
    
    def __getattr__(self, event_name): # decorator function
        if self._event_exists(event_name):
            return self._get_event_function_subscriber_decorator(event_name)
        else:
            raise AttributeError(f'No event with name {event_name}')
            
            
    def _event_exists(self, event_name):
        return event_name in self._events
    
    def _get_event_function_subscriber_decorator(self, event_name):
        event = self._get_event(event_name)
        def decorator(function):
            wrapped_function = FunctionWrapper(function)
            self._handle_decorator_function_subscription(event, wrapped_function)
            return wrapped_function.function
        return decorator
        
    def _get_event(self, event_name):
        return self._events[event_name]
        
    def _handle_decorator_function_subscription(self, event, wrapped_function):
        if wrapped_function.has_no_parameters():
            event.subscribe_function(wrapped_function.function)
        elif wrapped_function.has_one_parameter():
            wrapped_function.tag_for_later_subscription(self._function_tag_name, event.name)
        else:
            raise TypeError(f'{wrapped_function.get_name()}() was added to {event_name} event but had too many parameters')



class Event:
    def __init__(self, name):
        self.name = name
        self._functions = set()
        
    def run(self):
        for function in self._functions:
            function()
        
    def subscribe_function(self, function):
        self._functions.add(function)
        
    def subscribe_function_if_has_no_parameters(self, wrapped_function):
        if wrapped_function.has_no_parameters():
            self.subscribe_function(function)

        
        
class FunctionWrapper:
    def __init__(self, function):
        self.function = function
        
    def get_name(self):
        return self.function.__name__
        
    def tag_for_later_subscription(self, attribute_name, event_name):
        list_of_event_names = getattr(self.function, attribute_name, [])
        list_of_event_names.append(event_name)
        setattr(self.function, attribute_name, list_of_event_names)
        
    def has_no_parameters(self):
        return self.number_of_parameters() == 0
        
    def has_one_parameter(self):
        return self.number_of_parameters() == 1
        
    def number_of_parameters(self):
        return len(inspect.signature(self.function).parameters)
