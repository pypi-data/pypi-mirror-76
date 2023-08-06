import cachey
import uvicorn
import xarray as xr
from fastapi import FastAPI, HTTPException

from .dependencies import get_cache, get_dataset, get_dataset_ids
from .routers import base_router, common_router, dataset_collection_router, zarr_router
from .utils.api import (
    SingleDatasetOpenAPIOverrider,
    check_route_conflicts,
    normalize_app_routers,
    normalize_datasets,
)


def _dataset_from_collection_getter(datasets):
    """Used to override the get_dataset FastAPI dependency in case where
    a collection of datasets is being served.

    """

    def get_dataset(dataset_id: str):
        if dataset_id not in datasets:
            raise HTTPException(status_code=404, detail=f"Dataset '{dataset_id}' not found")

        return datasets[dataset_id]

    return get_dataset


def _dataset_unique_getter(dataset):
    """Used to override the get_dataset FastAPI dependency in case where
    only one dataset is being served, e.g., via the 'rest' accessor.

    """

    def get_dataset():
        return dataset

    return get_dataset


def _set_app_routers(dataset_routers=None, dataset_route_prefix=''):

    app_routers = []

    # top-level api endpoints
    app_routers.append((common_router, {}))

    if dataset_route_prefix:
        app_routers.append((dataset_collection_router, {'tags': ['info']}))

    # dataset-specifc api endpoints
    if dataset_routers is None:
        dataset_routers = [
            (base_router, {'tags': ['info']}),
            (zarr_router, {'tags': ['zarr']}),
        ]

    app_routers += normalize_app_routers(dataset_routers, dataset_route_prefix)

    check_route_conflicts(app_routers)

    return app_routers


class Rest:
    """Used to publish one or more Xarray Datasets via a REST API (FastAPI application).

    To publish a single dataset via its own FastAPI application, you might
    want to use the :attr:`xarray.Dataset.rest` accessor instead for more convenience.
    It provides the same interface than this class.

    Parameters
    ----------
    datasets : :class:`xarray.Dataset` or dict
        A single :class:`xarray.Dataset` object or a mapping of datasets objects
        to be served. If a mapping is given, keys are used as dataset ids and
        are converted to strings. See also the notes below.
    routers : list, optional
        A list of dataset-specific :class:`fastapi.APIRouter` instances to
        include in the fastAPI application. If None, the default routers will be
        included.
        The items of the list may also be tuples with the following format:
        ``[(router1, {'prefix': '/foo', 'tags': ['foo', 'bar']})]``, where
        the 1st tuple element is a :class:`fastapi.APIRouter` instance and the
        2nd element is a dictionary that is used to pass keyword arguments to
        :meth:`fastapi.FastAPI.include_router`.
    cache_kws : dict, optional
        Dictionary of keyword arguments to be passed to
        :meth:`cachey.Cache.__init__()`.
        By default, the cache size is set to 1MB, but this can be changed with
        ``available_bytes``.
    app_kws : dict, optional
        Dictionary of keyword arguments to be passed to
        :meth:`fastapi.FastAPI.__init__()`.

    Notes
    -----
    The urls of the application's API endpoints differ whether a single dataset
    or a mapping (collection) of datasets is given. In the latter case, all
    dataset-specific endpoint urls have the prefix ``/datasets/{dataset_id}``,
    where ``{dataset_id}`` corresponds to the keys of the mapping (converted to
    strings). Still in the latter case, the endpoint ``/datasets`` is added and returns
    the list of all dataset ids.

    """

    def __init__(self, datasets, routers=None, cache_kws=None, app_kws=None):

        self._datasets = normalize_datasets(datasets)

        if not self._datasets:
            # publish single dataset
            self._get_dataset_func = _dataset_unique_getter(datasets)
            dataset_route_prefix = ''
        else:
            self._get_dataset_func = _dataset_from_collection_getter(self._datasets)
            dataset_route_prefix = '/datasets/{dataset_id}'

        self._app_routers = _set_app_routers(routers, dataset_route_prefix)

        self._app = None
        self._app_kws = {}
        if app_kws is not None:
            self._app_kws.update(app_kws)

        self._cache = None
        self._cache_kws = {'available_bytes': 1e6}
        if cache_kws is not None:
            self._cache_kws.update(cache_kws)

    @property
    def cache(self) -> cachey.Cache:
        """Returns the :class:`cachey.Cache` instance used by the FastAPI application."""

        if self._cache is None:
            self._cache = cachey.Cache(**self._cache_kws)
        return self._cache

    def _init_app(self):
        """Initiate the FastAPI application."""

        self._app = FastAPI(**self._app_kws)

        for rt, kwargs in self._app_routers:
            self._app.include_router(rt, **kwargs)

        self._app.dependency_overrides[get_dataset_ids] = lambda: list(self._datasets)
        self._app.dependency_overrides[get_dataset] = self._get_dataset_func
        self._app.dependency_overrides[get_cache] = lambda: self.cache

        if not self._datasets:
            # fix openapi spec for single dataset
            self._app.openapi = SingleDatasetOpenAPIOverrider(self._app).openapi

        return self._app

    @property
    def app(self) -> FastAPI:
        """Returns the :class:`fastapi.FastAPI` application instance."""
        if self._app is None:
            self._app = self._init_app()
        return self._app

    def serve(self, host='0.0.0.0', port=9000, log_level='debug', **kwargs):
        """Serve this FastAPI application via :func:`uvicorn.run`.

        Parameters
        ----------
        host : str
            Bind socket to this host.
        port : int
            Bind socket to this port.
        log_level : str
            App logging level, valid options are
            {'critical', 'error', 'warning', 'info', 'debug', 'trace'}.
        **kwargs :
            Additional arguments to be passed to :func:`uvicorn.run`.

        Notes
        -----
        This method is blocking and does not return.

        """
        uvicorn.run(self.app, host=host, port=port, log_level=log_level, **kwargs)


@xr.register_dataset_accessor('rest')
class RestAccessor:
    """REST API Accessor for serving one dataset in its
    dedicated FastAPI application.

    """

    def __init__(self, xarray_obj):

        self._obj = xarray_obj
        self._rest = None

        self._initialized = False

    def _get_rest_obj(self):
        if self._rest is None:
            self._rest = Rest(self._obj)

        return self._rest

    def __call__(self, **kwargs):
        """Initialize this accessor by setting optional configuration values.

        Parameters
        ----------
        **kwargs
            Arguments passed to :func:`xpublish.Rest.__init__`.

        Notes
        -----
        This method can only be invoked once.

        """
        if self._initialized:
            raise RuntimeError('This accessor has already been initialized')
        self._initialized = True

        self._rest = Rest(self._obj, **kwargs)

        return self

    @property
    def cache(self) -> cachey.Cache:
        """Returns the :class:`cachey.Cache` instance used by the FastAPI application."""

        return self._get_rest_obj().cache

    @property
    def app(self) -> FastAPI:
        """Returns the :class:`fastapi.FastAPI` application instance."""

        return self._get_rest_obj().app

    def serve(self, **kwargs):
        """Serve this FastAPI application via :func:`uvicorn.run`.

        Parameters
        ----------
        **kwargs :
            Arguments passed to :func:`xpublish.Rest.serve`.

        Notes
        -----
        This method is blocking and does not return.

        """
        self._get_rest_obj().serve(**kwargs)
