from .weather_tool import weather_tool
from .flight_tool import flight_tool
from .places_tool import places_tool

from vertexai.generative_models import Tool, FunctionDeclaration

all_tools = [
    Tool(
        function_declarations=[
            FunctionDeclaration.from_func(weather_tool),
            FunctionDeclaration.from_func(flight_tool),
            FunctionDeclaration.from_func(places_tool),
        ]
    )
]