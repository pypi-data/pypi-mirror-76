from .errors import NotConnectedError


class GenericTree:
    def __init__(self, backend):
        """
        Creates an empty tree
        """
        self._backend = backend

        self._keys = set()  # Set of all keys
        self._parents = {}  # Dictionary {child key -> parent key}
        self._transforms = {}  # Dictionary {(from key, to key) -> 4x4 np.array}

    def hasFrame(self, key):
        """
        Checks if there is a frame `key`
        """
        return key in self._keys

    def setTransform(self, transform, from_key, to_key):
        """
        Sets a transform between `from_key` and `to_key` if this does not create a cycle
        """
        if (from_key, to_key) in self._transforms or (
            to_key,
            from_key,
        ) in self._transforms:
            self._transforms.pop((to_key, from_key), None)
            self._transforms[(from_key, to_key)] = transform
        else:
            has_from_key = from_key in self._parents.keys()
            has_to_key = to_key in self._parents.keys()
            if has_from_key and has_to_key:
                from_root = self._getAncestry(from_key)
                to_root = self._getAncestry(to_key)

                if from_root == to_root:
                    raise NotConnectedError(from_key, to_key)

                # Connect the trees by making to_key the root of its tree
                raise NotImplementedError  # TODO
            elif has_to_key:
                # Reverse the order since `to_key` already has a parent
                self._keys.add(from_key)
                self._parents[from_key] = to_key
                self._transforms[(from_key, to_key)] = transform
            else:
                self._keys.add(to_key)
                self._parents[to_key] = from_key
                self._transforms[(from_key, to_key)] = transform

    def _getAncestry(self, key):
        """
        Gets path from `key` to the tree root (including `key`)
        """
        path = []
        while key is not None:
            path.append(key)
            key = self._parents.get(key, None)
        return path

    def _getRoot(self, key):
        """
        Gets root of tree containing `key`
        """
        return self._getAncestry(key)[-1]

    def _getDirectTransform(self, from_key, to_key):
        """
        If `from_key` and `to_key` are directly connected, get the transformation
        """
        ret = self._transforms.get((from_key, to_key), None)
        if ret is not None:
            return ret

        ret = self._transforms.get((to_key, from_key), None)
        if ret is not None:
            return self._backend.invert(ret)

        return None

    def getPath(self, from_key, to_key):
        """
        Gets the shortest path between `from_key` and `to_key`
        """
        if from_key == to_key:
            return [from_key]

        from_root_path = self._getAncestry(from_key)
        to_root_path = self._getAncestry(to_key)
        if from_root_path[-1] != to_root_path[-1]:
            # Not connected
            return None

        i = 0
        for from_path_node, to_path_node in zip(
            reversed(from_root_path), reversed(to_root_path)
        ):
            if from_path_node != to_path_node:
                break
            i += 1

        # +1 on from_path to include connecting node
        from_path = from_root_path[: len(from_root_path) - i + 1]
        to_path = to_root_path[: len(to_root_path) - i]
        return from_path + list(reversed(to_path))

    def getTransform(self, from_key, to_key):
        """
        Calculates the composite transform between `from_key` and `to_key`
        """
        path = self.getPath(from_key, to_key)
        if path is None:
            raise NotConnectedError(from_key, to_key)

        return self._getTransformFromPath(path)

    def _getTransformFromPath(self, path):
        """
        Calculates the composition of transforms along a path
        """
        if len(path) < 2:
            return self._backend.identity()

        T = self._backend.identity()
        for from_key, to_key in zip(path, path[1:]):
            this_transform = self._getDirectTransform(from_key, to_key)
            T = self._backend.compose(T, this_transform)

        return T


class Tree(GenericTree):
    def __init__(self, *args):
        from .backends.numpy_backend import NumpyBackend

        super().__init__(*args, backend=NumpyBackend)
