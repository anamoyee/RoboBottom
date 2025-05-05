import re as regex
from collections import defaultdict, deque
from collections.abc import Iterable

from tcrutils.import_ import load_package_dynamically

from common.errors import ThisError
from common.models import Mod
from prelude import *

MOD_ALLOWED_NAME = r"^[A-Za-z0-9_]+$"
DEPENDENCIES_FILE_NAME = "dependencies.txt"

MODS: dict[str, Mod] = {}
"""Global containing currently loaded mods. Should be .updated(), not overwritten."""

logger = get_logger("mod_loader")


class ModDependencyError(ThisError):  # Not ModError since the error originates from the mod loader, not a mod itself
	"""There was an issue ordering mods to load by their dependencies because one or multiple mods have their dependencies misconfigured."""


def sorted_by_dependency(paths: Iterable[p.Path], dependencies: dict[str, list[str]]) -> list[p.Path]:
	"""Sort mod load order based on their dependencies using graph and an in-degree count for Kahn's algorithm."""
	path_dict = {path.name: path for path in paths}

	graph = defaultdict(list)
	in_degree = defaultdict(int)

	for path in path_dict:
		in_degree[path] = 0

	for module, deps in dependencies.items():
		for dep in deps:
			if dep in path_dict:
				graph[dep].append(module)
				in_degree[module] += 1

	zero_in_degree_queue = deque([node for node in in_degree if in_degree[node] == 0])
	sorted_modules = []

	while zero_in_degree_queue:
		node = zero_in_degree_queue.popleft()
		sorted_modules.append(node)

		for neighbor in graph[node]:
			in_degree[neighbor] -= 1
			if in_degree[neighbor] == 0:
				zero_in_degree_queue.append(neighbor)

	if len(sorted_modules) != len(in_degree):
		raise ModDependencyError("A cycle was detected in the dependencies")

	return [path_dict[module] for module in sorted_modules]


async def load_mods_from_directory(path: p.Path) -> dict[str, Mod]:
	mods_dict = {}

	dependencies: dict[str, set[str]] = {}

	for item in path.iterdir():
		if not regex.match(MOD_ALLOWED_NAME, item.name.removesuffix(".py")):
			continue

		dependencies_path = item / DEPENDENCIES_FILE_NAME

		if dependencies_path.is_file():
			deps = set(dependencies_path.read_text().strip().split("\n"))
		else:
			deps = set()

		if item.name != "_":
			deps.add("_")

		for dep in deps:
			if not regex.match(MOD_ALLOWED_NAME, dep):
				raise ModDependencyError(f"Invalid dependency syntax: Mod {item.name!r} contains invalid dependency: {dep!r}")

		dependencies[item.name] = deps

	for mod_name, deps in dependencies.items():
		for dep in deps:
			if dep not in dependencies:
				raise ModDependencyError(f"Mod {mod_name!r} has a dependency on {dep!r} which does not exist")

	paths = path.iterdir()
	paths = sorted_by_dependency(paths, dependencies)

	for item in paths:
		if not regex.match(MOD_ALLOWED_NAME, item.name.removesuffix(".py")):
			if not item.name.startswith("#"):  # Intentional comment character
				logger.warning(f'ignoring mod {item.name!r} since it does not follow the naming schema: r"{MOD_ALLOWED_NAME}". to intentionally temporarily disable this mod, prefix it with #, for example: {("#" + item.name)!r}')
			else:
				logger.info(f"skipping commented mod {item.name!r}")
			continue

		mod_name = item.name.removesuffix(".py")

		try:
			pymodule = load_package_dynamically(item)

			sys.modules[mod_name] = pymodule

			if hasattr(pymodule, "load") and callable(pymodule.load):
				loaded_mod = Mod(pymodule=pymodule, name=mod_name)

			await pymodule.load()

			if hasattr(pymodule, "loaded_print") and callable(pymodule.loaded_print):
				text = await pymodule.loaded_print()
			else:
				text = f"loaded successfully"
		except Exception:
			logger.exception(f"Failed to load mod: {mod_name!r}, propagating exception...")
			raise

		if text is not None:
			get_logger(mod_name).info(text)

		mods_dict[mod_name] = loaded_mod

	return mods_dict
