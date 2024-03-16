#!/usr/bin/env python3
import flask
import jwt


JWT_SECRET = "secret"

def get_role():
    token = flask.request.headers.get("Token")
    if not token:
        raise RuntimeError("Access token is empty")

    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    role = decoded_token.get("role")
    if not role:
        raise RuntimeError("Access token doesnt contain role")

    return role

def get_cathedra():
    token = flask.request.headers.get("Token")
    if not token:
        raise RuntimeError("Access token is empty")

    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    cathedra = decoded_token.get("cathedra_id")
    if not cathedra:
        return None

    return cathedra


def check_role(valid_role, role):
    if role not in [r.value for r in valid_role]:
        raise RuntimeError("Insufficient rights")

