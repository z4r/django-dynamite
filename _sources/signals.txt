Signals
=======

Dynamite comes with two signals that you can subscribe to:

.. currentmodule:: dynamite.signals

.. attribute:: dynamic_model_changed

	The ``dynamic_model_changed`` signal is fired every time an entity
	is created or updated. The signal handler should accept two arguments.

	::

		from dynamite import signals

		def changed_handler(sender, entity, **kwargs):
		    print sender, created

		signals.dynamic_model_changed.connect(changed_handler)


.. attribute:: dynamic_model_deleted

	The ``dynamic_model_deleted`` signal is fired every time an entity
	is deleted. The signal handler should accept two arguments.

	::

		from dynamite import signals

		def delete_handler(sender, entity, **kwargs):
		    print sender, entity

		signals.dynamic_model_deleted.connect(delete_handler)