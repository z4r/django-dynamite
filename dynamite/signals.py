from django import dispatch

dynamic_model_changed = dispatch.Signal(providing_args=['entity'])
dynamic_model_deleted = dispatch.Signal(providing_args=['entity'])