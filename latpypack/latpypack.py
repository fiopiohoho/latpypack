"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps

class Map(ipyleaflet.Map):
    """This is the map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): _The ipyleaflet.Map class.
    """
    def __init__(self, center=[20,0], zoom=2, **kwargs):
        """Initialize the map
        """
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        if "add_layer_control" not in kwargs:
            layer_control_flag = True
        else:
            layer_control_flag = kwargs["add_layer_control"]
        kwargs.pop("add_layer_control", None)

        super().__init__(center=center, zoom=zoom, **kwargs)
        if layer_control_flag:
            self.add_layers_control()

        # self.add_toolbar()

    def add_tile_layer(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add(layer)
        return layer
    
    def add_basemap(self, name, **kwargs):
        """Adds a basemap to the current map.

        This method allows adding a basemap either by specifying a predefined basemap name
        or by directly providing a tile layer object. If a string is provided, it will
        look up the corresponding basemap URL and add it as a tile layer. If a tile layer
        object is provided, it will be added directly to the map.

        Args:
            name (str or object): The name of the predefined basemap (as a string) or a
                tile layer object to be added directly.
            **kwargs: Additional keyword arguments to pass to the underlying tile layer
                or basemap configuration.

        Example:
            >>> map.add_basemap("OpenStreetMap")  # Adds OpenStreetMap basemap
            >>> map.add_basemap(custom_tile_layer)  # Adds a custom tile layer
        """       
        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name)
        else:
            self.add(name)  

    def add_geojson(self, data, name="geojson", **kwargs):
        """add a GeoJSON layer to the map.

        Args:
            data (str | dict): The GeoJSON data as a string or dictionary.
            name (str, optional): The name of the layer. Defaults to "geojson".
        Returns:
            layer : The GeoJSON layer that was added to the map.
        """
        import json

        if isinstance(data, str):
            with open(data) as f:
                data = json.load(f)

        if "style" not in kwargs:
            kwargs["style"] = {"color": "blue", "weight": 1, "fillOpacity": 0}

        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {"fillColor": "#ff0000", "fillOpacity": 0.5}
          
        layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add(layer)
        return layer
    
    def add_layers_control(self, position="topright"):
        """Adds a layers control to the map.

        Args:
            position (str, optional): The position of the layers control. Defaults to "topright".
        """
        self.add_control(ipyleaflet.LayersControl(position=position))

    def add_shp(self, data, name="shp", **kwargs):
        """Adds a shapefile to the current object by converting it to GeoJSON.

        Args:
            data (str | shapefile.reader): The path to the shapefile or a shapefile reader object.
            name (str, optional): The name of the layer to be added. Defaults to "shp".
        """

        import shapefile
        import json

        if isinstance(data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__

        self.add_geojson(data, name, **kwargs)