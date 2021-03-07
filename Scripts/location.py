# Program to read lat/lon of customers and represent them on a map surface.

import random
import pandas as pd
import pydeck as pdk
from sklearn.datasets import make_blobs

LATITUDE, LONGITUDE = 6.221153, 10.679615  # Map focus center
# 6.224683, 10.663074


def get_data():
    data = pd.DataFrame(
        make_blobs(n_samples=100, centers=[
            [6.221153, 10.679615]], n_features=2, cluster_std=0.05, random_state=0)
    )
    data.columns = ['lat', 'lng']

    return data


def scatterplot_map(*args, **kwargs):
    """Plots using mapbox. There are two maps
    The columns should be labelled as "lng", "lat"
    And an optional tooltip name addr
    """
    colors = kwargs.get('fill_colors', _generate_colors(len(args))[0])
    layers = [_layer(df, fill_color=color) for df, color in zip(args, colors)]
    view_state = _view()

    return pdk.Deck(
        map_style='light',
        layers=layers,
        initial_view_state=view_state,
        # tooltip={"text": "{addr}"}
    )


def _layer(df, position=["lng", "lat"], fill_color=[242, 242, 242]):
    """Creates a map layer for a given dataframe"""
    # Define a layer to display on a map
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        pickable=True,
        opacity=0.9,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=4,
        radius_max_pixels=50,
        line_width_min_pixels=1,
        get_position=position,
        get_fill_color=fill_color,  # [255, 140, 0],#[180, 0, 200, 140]
        get_line_color=fill_color
    )
    return layer


def _view(latitude=LATITUDE, longitude=LONGITUDE):
    """Set the viewport location"""
    return pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=10,
        min_zoom=5,
        max_zoom=15,
        bearing=0,
        pitch=0
    )


def _generate_colors(n):
    """Generates n colors that are equally spaced

    Args:
        n (int): number of colors required

    Returns:
        list: list of list. One of rgb colors and other hex codes
    """
    rgb_values = []
    hex_values = []
    r = int(random.random() * 256)
    g = int(random.random() * 256)
    b = int(random.random() * 256)
    step = 256 / n
    for _ in range(n):
        r += step
        g += step
        b += step
        r = int(r) % 256
        g = int(g) % 256
        b = int(b) % 256
        r_hex = hex(r)[2:]
        g_hex = hex(g)[2:]
        b_hex = hex(b)[2:]
        hex_values.append('#' + r_hex + g_hex + b_hex)
        rgb_values.append((r, g, b))

    return rgb_values, hex_values


if __name__ == '__main__':
    events_locations = get_data()  # Customer location
    face_location = pd.DataFrame(
        {'lat': [6.224683], 'lng': [10.663074]})  # Office Center
    r = scatterplot_map(events_locations, face_location)
    r.to_html("kumbo.html")
