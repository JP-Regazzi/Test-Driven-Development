import connexion
import six
from flask import jsonify, make_response
from swagger_server import util

# In-memory "database" for cities.
# Keys are city initials, values are city names.
cities_data = {
    "PAR": "Paris"
}


def cities_city_code_delete(city_code):  # noqa: E501
    """DeleteCity

    :param city_code: City code to delete
    :type city_code: str
    :rtype: object
    """
    if city_code in cities_data:
        del cities_data[city_code]
        return make_response(jsonify({ "true": f"City deleted {city_code}" }), 200)
    else:
        return make_response(jsonify({ "error": f"City {city_code} not found" }), 404)


import json

def cities_city_code_patch(city_code, body=None):  # noqa: E501
    """UpdateCity"""
    try:
        if isinstance(body, str):
            data = json.loads(body)  # parse string to dict
        else:
            data = body or {}
    except json.JSONDecodeError:
        return make_response(jsonify({"error": "Invalid JSON string"}), 400)

    if city_code not in cities_data:
        return make_response(jsonify({"error": f"City {city_code} not found"}), 404)

    new_code = data.get("CityInitials", city_code)
    new_name = data.get("CityName", cities_data[city_code])

    if new_code != city_code:
        del cities_data[city_code]
    cities_data[new_code] = new_name

    return make_response(jsonify({
        "CityInitials": new_code,
        "CityName": new_name
    }), 200)



def cities_get(city_code=None):  # noqa: E501
    """GetCityByCode

    :param city_code: Optional query parameter to filter by city code
    :type city_code: str
    :rtype: object
    """
    # If a city code is provided, return that city if it exists.
    if city_code:
        if city_code in cities_data:
            city = {"CityInitials": city_code, "CityName": cities_data[city_code]}
            return make_response(jsonify([city]), 200)
        else:
            return make_response(jsonify([]), 200)
    else:
        # If no city code is provided, return all cities.
        all_cities = [{"CityInitials": code, "CityName": name} for code, name in cities_data.items()]
        return make_response(jsonify(all_cities), 200)


def cities_post(body=None):  # noqa: E501
    """AddCity

    :param body: City object to add
    :type body: dict | bytes
    :rtype: object
    """
    if not connexion.request.is_json:
        return make_response(jsonify({"error": "Request body must be JSON"}), 400)
    
    data = connexion.request.get_json()
    # Expecting keys: CityInitials and CityName
    city_initials = data.get("CityInitials")
    city_name = data.get("CityName")
    
    if not city_initials or not city_name:
        return make_response(jsonify({"error": "Both 'CityInitials' and 'CityName' are required"}), 400)
    
    # Add the new city.
    cities_data[city_initials] = city_name
    new_city = {"CityInitials": city_initials, "CityName": city_name}
    return make_response(jsonify(new_city), 201)
