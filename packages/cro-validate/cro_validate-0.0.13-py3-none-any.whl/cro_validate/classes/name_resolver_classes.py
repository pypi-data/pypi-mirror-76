

class DefaultNameResolver:
	def resolve(self, namespace, name):
		if name in namespace:
			return name
		import traceback
		traceback.print_stack()
		return None