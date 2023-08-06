from typing import Union, Optional
from copy import deepcopy

import numpy as np
from sklearn.metrics import pairwise_distances

from whatlies.common import handle_2d_plot


class Embedding:
    """
    This object represents a word embedding. It contains a vector and a name.

    Arguments:
        name: the name of this embedding, includes operations
        vector: the numerical representation of the embedding
        orig: original name of embedding, is left alone

    Usage:

    ```python
    from whatlies.embedding import Embedding

    foo = Embedding("foo", [0.1, 0.3])
    bar = Embedding("bar", [0.7, 0.2])

    foo | bar
    foo - bar + bar
    ```
    """

    def __init__(self, name, vector, orig=None):
        self.orig = name if not orig else orig
        self.name = name
        self.vector = np.array(vector)

    def add_property(self, name, func):
        result = Embedding(name=self.name, vector=self.vector, orig=self.orig,)
        setattr(result, name, func(result))
        return result

    def __add__(self, other) -> "Embedding":
        """
        Add two embeddings together.

        Usage:

        ```python
        from whatlies.embedding import Embedding

        foo = Embedding("foo", [0.1, 0.3])
        bar = Embedding("bar", [0.7, 0.2])

        foo + bar
        ```
        """
        copied = deepcopy(self)
        copied.name = f"({self.name} + {other.name})"
        copied.vector = self.vector + other.vector
        return copied

    def __sub__(self, other):
        """
        Subtract two embeddings.

        Usage:

        ```python
        from whatlies.embedding import Embedding

        foo = Embedding("foo", [0.1, 0.3])
        bar = Embedding("bar", [0.7, 0.2])

        foo - bar
        ```
        """
        copied = deepcopy(self)
        copied.name = f"({self.name} - {other.name})"
        copied.vector = self.vector - other.vector
        return copied

    def __gt__(self, other):
        """
        Measures the size of one embedding to another one.

        Usage:

        ```python
        from whatlies.embedding import Embedding

        foo = Embedding("foo", [0.1, 0.3])
        bar = Embedding("bar", [0.7, 0.2])

        foo > bar
        ```
        """
        return (self.vector.dot(other.vector)) / (other.vector.dot(other.vector))

    def __rshift__(self, other):
        """
        Maps an embedding unto another one.

        Usage:

        ```python
        from whatlies.embedding import Embedding

        foo = Embedding("foo", [0.1, 0.3])
        bar = Embedding("bar", [0.7, 0.2])

        foo >> bar
        ```
        """
        copied = deepcopy(self)
        new_vec = (
            (self.vector.dot(other.vector))
            / (other.vector.dot(other.vector))
            * other.vector
        )
        copied.name = f"({self.name} >> {other.name})"
        copied.vector = new_vec
        return copied

    def __or__(self, other):
        """
        Makes one embedding orthogonal to the other one.

        Usage:

        ```python
        from whatlies.embedding import Embedding

        foo = Embedding("foo", [0.1, 0.3])
        bar = Embedding("bar", [0.7, 0.2])

        foo | bar
        ```
        """
        copied = deepcopy(self)
        copied.name = f"({self.name} | {other.name})"
        copied.vector = self.vector - (self >> other).vector
        return copied

    def __repr__(self):
        return f"Emb[{self.name}]"

    def __str__(self):
        return self.name

    @property
    def norm(self):
        """Gives the norm of the vector of the embedding"""
        return np.linalg.norm(self.vector)

    def distance(self, other, metric: str = "cosine"):
        """
        Calculates the vector distance between two embeddings.

        Arguments:
            other: the other embedding you're comparing against
            metric: the distance metric to use, the list of valid options can be found [here](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html)

        **Usage**

        ```python
        from whatlies.embedding import Embedding

        foo = Embedding("foo", [1.0, 0.0])
        bar = Embedding("bar", [0.0, 0.5])

        foo.distance(bar)
        foo.distance(bar, metric="euclidean")
        foo.distance(bar, metric="cosine")
        ```
        """
        return pairwise_distances([self.vector], [other.vector], metric=metric)[0][0]

    def plot(
        self,
        kind: str = "scatter",
        x_axis: Union[str, "Embedding"] = None,
        y_axis: Union[str, "Embedding"] = None,
        color: str = None,
        show_ops: bool = False,
        annot: bool = False,
        axis_option: Optional[str] = None,
    ):
        """
        Handles the logic to perform a 2d plot in matplotlib.

        Arguments:
            kind: what kind of plot to make, can be `scatter`, `arrow` or `text`
            x_axis: the x-axis to be used, must be given when dim > 2
            y_axis: the y-axis to be used, must be given when dim > 2
            color: the color of the dots
            show_ops: setting to also show the applied operations, only works for `text`
            annot: should the points be annotated
            axis_option: a string which is passed as `option` argument to `matplotlib.pyplot.axis` in order to control
                axis properties (e.g. using `'equal'` make circles shown circular in the plot). This might be useful
                for preserving geometric relationships (e.g. orthogonality) in the generated plot. See `matplotlib.pyplot.axis`
                [documentation](https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.axis.html#matplotlib-pyplot-axis)
                for possible values and their description.

        **Usage**
        ```python
        from whatlies.embedding import Embedding

        foo = Embedding("foo", [0.1, 0.3])
        bar = Embedding("bar", [0.7, 0.2])

        foo.plot(kind="arrow", annot=True)
        bar.plot(kind="arrow", annot=True)
        ```
        """
        if len(self.vector) == 2:
            handle_2d_plot(
                self,
                kind=kind,
                color=color,
                show_operations=show_ops,
                xlabel=x_axis,
                ylabel=y_axis,
                annot=annot,
                axis_option=axis_option,
            )
            return self
        x_val = self > x_axis
        y_val = self > y_axis
        intermediate = Embedding(name=self.name, vector=[x_val, y_val], orig=self.orig)
        handle_2d_plot(
            intermediate,
            kind=kind,
            color=color,
            xlabel=x_axis.name,
            ylabel=y_axis.name,
            show_operations=show_ops,
            annot=annot,
            axis_option=axis_option,
        )
        return self
