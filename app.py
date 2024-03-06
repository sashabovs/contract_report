#!/usr/bin/env python3

import json

import flask
import psycopg
from psycopg.rows import dict_row
from flask import request

import bcrypt

import jwt

app = flask.Flask(__name__, static_url_path="", static_folder="static")

routes = []
JWT_SECRET = "secret"

@app.route("/")
def index():
    return app.send_static_file("index.html")

def get_reader_connection_string():
    return "host=localhost port=5432 dbname=contract_report user=contract_report_reader password=123"

def get_writer_connection_string():
    return "host=localhost port=5432 dbname=contract_report user=contract_report_writer password=123"

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt()).decode()

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())

@app.route("/load-templates")
def load_templates():
    with psycopg.connect(get_reader_connection_string(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM contract_report.contract_templates")
            rows = cur.fetchall()

    return json.dumps(rows)

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    with psycopg.connect(get_reader_connection_string(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("select password, role from contract_report.users where login=%(login)s",{'login':data['login']})

            rows = cur.fetchall()
            if not rows:
                return flask.Response(
                    f"Login {data['login']} is not found",
                    status=401,
                    )

            if not check_password(data['password'], rows[0]['password']):
                return flask.Response(
                    f"Incorrect password for {data['login']}",
                    status=401,
                )

            role = rows[0]['role']

    encoded = jwt.encode({"login": data["login"], "role": role}, JWT_SECRET, algorithm="HS256")
    return {"token": encoded}


# @app.route("/tiles/<int:z>/<int:x>/<int:y>.mvt")
# def tiles(z, x, y):
#     with pymbtiles.MBtiles("/home/bovsunov/work/check_routes/geojsons/out.mbtiles") as src:
#         y = (1 << z) - 1 - y
#         tile_data = src.read_tile(z, x, y)
#         if tile_data != None:
#             resp = flask.make_response(tile_data, 200)
#             resp.headers["Content-Type"] = "application/x-protobuf"
#             return resp
#         else:
#             resp = flask.make_response("", 404)
#             return resp
#
#
# @app.route("/trace/<int:trace_num>")
# def get_trace(trace_num):
#     id = routes[trace_num]
#     # with open(f"/home/bovsunov/work/check_routes/orbis_route_illegal_on_genesis_map/{id}_route.kml") as f:
#     #     return f.read()
#     with open(
#         f"/home/bovsunov/work/check_routes/orbis_route_illegal_on_genesis_map_reconstruct/{id}_search_0.kml"
#     ) as f:
#         doc = f.read()
#         k = kml.KML()
#         k.from_string(doc.encode("utf-8"))
#
#         res = {"type": "FeatureCollection", "features": []}
#
#         # list with the points folder and with links
#         data = list(list(k.features())[0].features())
#         links = data[1:]
#
#         geoFeatures = []
#         styles_dict = {}
#
#         styles = list(list(k.features())[0].styles())
#         for style in styles:
#             sub_styles = list(style.styles())
#             # st = {'id': f'#{style.id}'}
#
#             style_key = f"#{style.id}"
#             styles_dict[style_key] = {}
#             for sub_style in sub_styles:
#                 color = f"#{sub_style.color[6:8]}{sub_style.color[4:6]}{sub_style.color[2:4]}"
#                 style_type = type(sub_style).__name__
#                 styles_dict[style_key][style_type] = {"color": color}
#             # res['styles'].append(st)
#
#         for link in links:
#             descr = link.description
#             p1, p2 = link.geometry.geoms
#             x1, y1 = p1.x, p1.y
#             x2, y2 = p2.x, p2.y
#             name = link.name
#             style_url = link.styleUrl
#             timestamp = link.timeStamp
#             # res['links'].append({'descr': descr, 'points': [[y1, x1], [y2, x2]], 'name': name, 'style': style_url, 'time': timestamp})
#             geoFeatures.append(
#                 geojson.Feature(
#                     geometry=geojson.LineString([(x1, y1), (x2, y2)]),
#                     properties={
#                         "name": name,
#                         "descr": descr,
#                         "time": timestamp.isoformat(),
#                         "style": styles_dict[style_url]["LineStyle"],
#                     },
#                 )
#             )
#
#         supporting_points = list(data[0].features())
#         for point in supporting_points:
#             x = point.geometry.x
#             y = point.geometry.y
#             name = point.name
#             style_url = point.styleUrl
#             timestamp = point.timeStamp
#             # res['points'].append({'point': [y, x], 'name': name, 'style': style_url, 'time': timestamp})
#             geoFeatures.append(
#                 geojson.Feature(
#                     geometry=geojson.Point((x, y)),
#                     properties={
#                         "name": name,
#                         "time": timestamp.isoformat(),
#                         "style": styles_dict[style_url]["IconStyle"],
#                     },
#                 )
#             )
#
#         fc = geojson.FeatureCollection(geoFeatures)
#         print(f"finished: {trace_num}")
#
#         res = geojson.dumps(fc, sort_keys=True, indent=4)
#         output_file = pathlib.Path(f"/home/bovsunov/work/check_routes/geojsons/{id}.geojson")
#         output_file.parent.mkdir(exist_ok=True, parents=True)
#         output_file.write_text(res)
#
#         return res
