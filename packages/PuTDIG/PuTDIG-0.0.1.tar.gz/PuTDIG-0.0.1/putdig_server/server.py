#!/usr/bin/env python3
from flask import Flask, render_template, url_for, redirect, request, session
from dataclasses import asdict
from pathlib import Path
import json
import tempfile
import secrets
from contextlib import redirect_stdout
import io
from putdig.common import SupMCUModuleTelemetrySet, parse_bus_telemetry, \
    parse_bus_telemetry_definition, validate_value, discover_bus_telemetry, \
    compare_versions

try:
    from pumpkin_supmcu.i2cdriver import I2CDriverMaster
except ImportError:
    I2CDriverMaster = None
try:
    from pumpkin_supmcu.linux import I2CLinuxMaster
except ImportError:
    I2CLinuxMaster = None
try:
    from pumpkin_supmcu.kubos import I2CKubosMaster
except ImportError:
    I2CKubosMaster = None

from pumpkin_supmcu.supmcu import SupMCUSerialMaster, set_values, get_version_string, \
    DataType
import os
import sys


def get_possible_templates_path():
    """
    Gets the possible paths that the templates/statics folder could be at, if they don't exist, then
    this returns None, None

    :return: Possible paths of the templates/statics folder, or None, None if part of setup packages.
    """
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'templates'), os.path.join(sys._MEIPASS, 'static')

    elif Path("../dist/static").is_dir():
        return "../dist/static", "../dist"
    else:
        # We're in package installed from setup to
        import pkg_resources
        td_path = Path(pkg_resources.resource_filename("putdig_server", "dist"))
        sf = str(td_path / "static")
        tf = str(td_path)
        return sf, tf


static_folder, template_folder = get_possible_templates_path()
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.secret_key = secrets.token_urlsafe(16)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == "json"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/edit")
def edit():
    if 'telemetry_data' not in session:
        return redirect(url_for("index"))
    return render_template("edit.html")


@app.route("/edit/device", methods=["POST"])
def edit_device():
    if request.json['port'] == '':
        return ('', 400)
    type = request.json['type'].lower()
    port = request.json['port']
    try:
        if type == "i2c driver":
            i2c_master = I2CDriverMaster(port)
        elif type == "aardvark":
            return ("Aardvark I2C controller is currently not implemented", 200)
        elif type == "linux":
            i2c_master = I2CLinuxMaster(int(port))
        elif type == "kubos":
            i2c_master = I2CKubosMaster(int(port))
        telemetry_def = discover_bus_telemetry(i2c_master)
        session['telemetry_data'] = [asdict(SupMCUModuleTelemetrySet.from_definition(t_def)) for t_def in telemetry_def]
        return ('', 204)
    except Exception as e:
        return (str(e), 200)


@app.route("/edit/upload", methods=["POST"])
def edit_upload():
    f = request.files['file']
    if f.filename == "":
        return redirect(url_for("index"))
    if f and allowed_file(f.filename):
        try:
            module_defs = parse_bus_telemetry_definition(json.load(f))
            modules = [SupMCUModuleTelemetrySet.from_definition(mod_def) for mod_def in module_defs]
            session['telemetry_data'] = [asdict(mod) for mod in modules]
        except KeyError:
            modules = parse_bus_telemetry(json.load(f))
            session['telemetry_data'] = [asdict(mod) for mod in modules]
        finally:
            return ('', 204)


@app.route("/edit/validate", methods=["POST"])
def validate():
    if 'telemetry_data' not in session:
        return redirect(url_for("index"))
    msg = ''
    request.json['type'] = DataType(request.json['type'])
    f = io.StringIO()
    with redirect_stdout(f):
        val = validate_value(*request.json.values())
    msg = f.getvalue()
    return {
        "valid": val is not False,
        "value": val,
        "msg": msg
    }


@app.route("/edit/inject", methods=["POST"])
def inject():
    if 'telemetry_data' not in session:
        return redirect(url_for("index"))

    if request.json['port'] == '':
        return ('', 400)
    type = request.json['type'].lower()
    port = request.json['port']
    modules = parse_bus_telemetry(request.json['data'])
    try:
        if type == "i2c driver":
            master = I2CDriverMaster(port)
        elif type == "aardvark":
            return ("Aardvark I2C controller is currently not implemented", 200)
        elif type == "linux":
            master = I2CLinuxMaster(int(port))
        elif type == "serial":
            master = SupMCUSerialMaster([mod.cmd_name for mod in modules], port.split(','))
        elif type == "kubos":
            master = I2CKubosMaster(int(port))
        if not isinstance(master, SupMCUSerialMaster):
            valid_addresses = master.get_bus_devices()
            addresses = [mod.address for mod in modules]
            for addr in addresses:
                if addr not in valid_addresses:
                    raise IndexError("Modules to inject were not found on the I2C bus")
        for mod in modules:
            version = get_version_string(master, mod.address, mod.cmd_name)
            if compare_versions(version, mod.version):
                for telem in mod.module_telemetry:
                    if telem.simulatable:
                        set_values(master, mod.address, mod.cmd_name, telem.idx, telem.sup_telemetry.items)
            else:
                raise ValueError(f"Module version mismatch.  Expected value '{mod.version}' != '{version}'")
        return ('', 204)
    except Exception as e:
        return (str(e), 200)


def main():
    from waitress import serve
    serve(app)


if __name__ == "__main__":
    main()
